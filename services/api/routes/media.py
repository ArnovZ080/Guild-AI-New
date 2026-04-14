"""
Media Library API Routes

POST   /api/media/upload         — Upload one or more images/videos
GET    /api/media/               — List user's media assets (with filters)
GET    /api/media/search         — Semantic search ("candle on wooden table")
DELETE /api/media/{id}           — Delete an asset
PUT    /api/media/{id}           — Update tags, category, alt_text
POST   /api/media/{id}/enhance   — AI-enhance an image (stub)
"""
from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException
from typing import List, Optional
import uuid

from services.api.middleware.auth import get_current_user
from services.core.media_library.processor import media_processor
from services.core.storage import storage
from services.core.db.base import AsyncSessionLocal
from services.core.db.models import MediaAsset
from services.core.config import settings
from sqlalchemy import select, desc

router = APIRouter(prefix="/api/media", tags=["Media Library"])


@router.post("/upload")
async def upload_media(
    files: List[UploadFile] = File(...),
    category: Optional[str] = Query(None),
    user=Depends(get_current_user),
):
    """Upload one or more media files. Each is processed (thumbnail, AI analysis, embedding)."""
    results = []

    for file in files:
        # Validate file type
        allowed = settings.ALLOWED_IMAGE_TYPES + settings.ALLOWED_VIDEO_TYPES
        if file.content_type not in allowed:
            results.append({
                "filename": file.filename,
                "error": f"Unsupported file type: {file.content_type}",
            })
            continue

        # Validate size
        contents = await file.read()
        if len(contents) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            results.append({
                "filename": file.filename,
                "error": f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit",
            })
            continue

        # Process (thumbnail, AI vision, embedding)
        metadata = await media_processor.process_upload(
            file_bytes=contents,
            filename=file.filename,
            mime_type=file.content_type,
            user_id=user.id,
        )

        # Save to DB
        async with AsyncSessionLocal() as db:
            asset = MediaAsset(
                id=str(uuid.uuid4()),
                user_id=user.id,
                filename=metadata["storage_url"].split("/")[-1],
                original_filename=file.filename,
                mime_type=file.content_type,
                file_size=len(contents),
                storage_url=metadata["storage_url"],
                thumbnail_url=metadata.get("thumbnail_url"),
                ai_description=metadata.get("ai_description", ""),
                ai_tags=metadata.get("ai_tags", []),
                ai_colors=metadata.get("ai_colors", []),
                ai_embedding_id=metadata.get("ai_embedding_id"),
                category=category,
                width=metadata.get("width"),
                height=metadata.get("height"),
            )
            db.add(asset)
            await db.commit()
            await db.refresh(asset)

            results.append({
                "id": asset.id,
                "filename": asset.original_filename,
                "storage_url": asset.storage_url,
                "thumbnail_url": asset.thumbnail_url,
                "ai_description": asset.ai_description,
                "ai_tags": asset.ai_tags,
                "category": asset.category,
            })

    return {"uploaded": results}


@router.get("/")
async def list_media(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    user=Depends(get_current_user),
):
    """List user's media assets with optional filtering."""
    async with AsyncSessionLocal() as db:
        query = select(MediaAsset).where(MediaAsset.user_id == user.id)

        if category:
            query = query.where(MediaAsset.category == category)

        query = query.order_by(desc(MediaAsset.created_at)).limit(limit).offset(offset)
        result = await db.execute(query)
        assets = result.scalars().all()

        return {
            "assets": [
                {
                    "id": a.id,
                    "filename": a.original_filename,
                    "storage_url": a.storage_url,
                    "thumbnail_url": a.thumbnail_url,
                    "ai_description": a.ai_description,
                    "ai_tags": a.ai_tags,
                    "ai_colors": a.ai_colors,
                    "category": a.category,
                    "user_tags": a.user_tags,
                    "alt_text": a.alt_text,
                    "width": a.width,
                    "height": a.height,
                    "file_size": a.file_size,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                }
                for a in assets
            ],
            "total": len(assets),
        }


@router.get("/search")
async def search_media(
    q: str = Query(..., description="Natural language search, e.g. 'candle on wooden table'"),
    limit: int = 10,
    user=Depends(get_current_user),
):
    """Semantic search across user's media using AI descriptions and Qdrant embeddings."""
    from services.core.knowledge.pipeline import KnowledgePipeline

    pipeline = KnowledgePipeline()
    collection = f"guild_media_{user.id.replace('-', '_')}"

    # Generate embedding for query
    embeddings = await pipeline._generate_embeddings([q])
    if not embeddings:
        return {"results": []}

    qdrant = pipeline._get_qdrant()
    if not qdrant:
        return {"results": []}

    try:
        results = qdrant.query_points(
            collection_name=collection,
            query=embeddings[0],
            limit=limit,
        )
        embedding_ids = [str(point.id) for point in results.points]
        scores = {str(point.id): point.score for point in results.points}
    except Exception:
        return {"results": []}

    # Match embedding results back to MediaAsset records
    if not embedding_ids:
        return {"results": []}

    async with AsyncSessionLocal() as db:
        query = select(MediaAsset).where(
            MediaAsset.user_id == user.id,
            MediaAsset.ai_embedding_id.in_(embedding_ids),
        )
        result = await db.execute(query)
        assets = result.scalars().all()

        return {
            "results": [
                {
                    "id": a.id,
                    "filename": a.original_filename,
                    "storage_url": a.storage_url,
                    "thumbnail_url": a.thumbnail_url,
                    "ai_description": a.ai_description,
                    "ai_tags": a.ai_tags,
                    "score": scores.get(a.ai_embedding_id, 0),
                }
                for a in assets
            ],
        }


@router.delete("/{asset_id}")
async def delete_media(asset_id: str, user=Depends(get_current_user)):
    """Delete a media asset and its stored file."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(MediaAsset).where(
                MediaAsset.id == asset_id,
                MediaAsset.user_id == user.id,
            )
        )
        asset = result.scalar_one_or_none()
        if not asset:
            raise HTTPException(404, "Asset not found")

        # Delete files from storage
        await storage.delete(asset.storage_url)
        if asset.thumbnail_url:
            await storage.delete(asset.thumbnail_url)

        await db.delete(asset)
        await db.commit()
        return {"deleted": True}


@router.put("/{asset_id}")
async def update_media(asset_id: str, updates: dict, user=Depends(get_current_user)):
    """Update category, tags, or alt_text on a media asset."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(MediaAsset).where(
                MediaAsset.id == asset_id,
                MediaAsset.user_id == user.id,
            )
        )
        asset = result.scalar_one_or_none()
        if not asset:
            raise HTTPException(404, "Asset not found")

        if "category" in updates:
            asset.category = updates["category"]
        if "user_tags" in updates:
            asset.user_tags = updates["user_tags"]
        if "alt_text" in updates:
            asset.alt_text = updates["alt_text"]

        await db.commit()
        return {"updated": True}


@router.post("/{asset_id}/enhance")
async def enhance_media(asset_id: str, instructions: dict, user=Depends(get_current_user)):
    """
    AI-enhance a media asset.
    instructions: {"action": "change_background", "prompt": "modern kitchen"}
    instructions: {"action": "resize", "platform": "instagram_story"}
    instructions: {"action": "add_text", "text": "Spring Collection", "position": "bottom"}
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(MediaAsset).where(
                MediaAsset.id == asset_id,
                MediaAsset.user_id == user.id,
            )
        )
        asset = result.scalar_one_or_none()
        if not asset:
            raise HTTPException(404, "Asset not found")

    # TODO: Route to Imagen 3 editing API based on action type
    # Imagen 3 supports inpainting/outpainting with text prompts
    # This generates a NEW MediaAsset based on the original

    return {
        "status": "enhancement_queued",
        "original_id": asset_id,
        "action": instructions.get("action"),
    }
