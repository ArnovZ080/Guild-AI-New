from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, List, Any, Optional
import os
import uuid
from datetime import datetime

from services.core.agents.identity import BusinessIdentityManager
from services.core.agents.models import BusinessIdentity as PydanticBusinessIdentity, KnowledgeSource
from services.core.logging import logger
from services.core.db.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from services.api.middleware.auth import get_current_user
from services.core.db.models import UserAccount, KnowledgeDocument
from services.core.tools.document_processor import document_processor

router = APIRouter(prefix="/identity", tags=["identity"])

@router.get("/")
async def get_identity(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    """Retrieve the persistent business identity."""
    try:
        identity = await BusinessIdentityManager.get(db, current_user.id)
        if not identity:
            # Return empty skeleton
            return {
                "business_name": "", "niche": "", "industry": "", "target_audience": "",
                "icp": {}, "brand_voice": "", "brand_visual": "", "brand_story": "",
                "competitors": [], "pricing_strategy": "", "marketing_channels": [],
                "content_preferences": [], "goals_3month": "", "goals_12month": "",
                "challenges": "", "completion_percentage": 0.0, "user_name": current_user.name
            }
            
        from services.core.agents.identity import _compute_completion
        completion = _compute_completion(identity)

        return {
            "business_name": identity.business_name,
            "niche": identity.niche,
            "industry": identity.industry,
            "target_audience": identity.target_audience,
            "icp": identity.icp,
            "brand_voice": identity.brand_voice,
            "brand_visual": identity.brand_visual,
            "brand_story": identity.brand_story,
            "competitors": identity.competitors,
            "pricing_strategy": identity.pricing_strategy,
            "marketing_channels": identity.marketing_channels,
            "content_preferences": identity.content_preferences,
            "goals_3month": identity.goals_3month,
            "goals_12month": identity.goals_12month,
            "challenges": identity.challenges,
            "completion_percentage": completion,
            "user_name": current_user.name
        }
    except Exception as e:
        logger.error(f"Failed to retrieve identity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def update_identity(identity: dict, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    """Update or initialize the persistent business identity."""
    try:
        # Separate user name update from identity updates
        user_name = identity.pop('user_name', None)
        if user_name is not None:
            current_user.name = user_name
            db.add(current_user)
            
        updated = await BusinessIdentityManager.create_or_update(db, current_user.id, identity)
        return updated
    except Exception as e:
        logger.error(f"Failed to save identity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/document")
async def get_documents(
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    """Retrieve all uploaded knowledge base documents."""
    try:
        from sqlalchemy import select
        from services.core.db.models import KnowledgeDocument
        stmt = select(KnowledgeDocument).where(KnowledgeDocument.user_id == current_user.id).order_by(KnowledgeDocument.embedded_at.desc())
        result = await db.execute(stmt)
        docs = result.scalars().all()
        return [
            {
                "id": doc.id,
                "name": doc.filename,
                "size": doc.doc_metadata.get("size", 0) if doc.doc_metadata else 0,
                "uploaded": doc.embedded_at.isoformat() if doc.embedded_at else None
            } for doc in docs
        ]
    except Exception as e:
        logger.error(f"Failed to get documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/document", response_model=KnowledgeSource)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    """Upload and process a business document to the knowledge base."""
    temp_path = None
    try:
        import tempfile
        # 1. Save uploaded file to temp location
        temp_dir = os.path.join(tempfile.gettempdir(), "guild_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        
        with open(temp_path, "wb") as f:
            f.write(await file.read())
            
        # 2. Process with DocumentProcessor
        result = document_processor.process_document(temp_path)
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=400, detail=result.get("error", "Unknown processing error"))
            
        # 3. Create KnowledgeSource entry
        new_source = KnowledgeSource(
            id=str(uuid.uuid4()),
            type="file",
            name=file.filename,
            content_preview=result["content"][:500] + "...", # Store a preview
            indexed_at=datetime.now().isoformat()
        )
        
        # 4. Update Identity Knowledge Base (Database)
        doc = KnowledgeDocument(
            id=new_source.id,
            user_id=current_user.id,
            filename=file.filename,
            content_type="document",
            chunk_count=len(result.get("chunks", [])),
            embedded_at=datetime.now(),
            doc_metadata={"preview": new_source.content_preview}
        )
        db.add(doc)
        await db.commit()
        
        return new_source
        
    except Exception as e:
        logger.error(f"Failed to process document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
