"""
Media Asset Processor
- Generates thumbnails
- Gets AI description via Gemini Vision
- Extracts dominant colours
- Creates vector embedding for semantic search
"""
import io
import json
import base64
import hashlib
import logging
from typing import Dict, Any, List, Optional

from PIL import Image

from services.core.storage import storage
from services.core.config import settings

logger = logging.getLogger(__name__)


class MediaProcessor:

    async def process_upload(
        self,
        file_bytes: bytes,
        filename: str,
        mime_type: str,
        user_id: str,
    ) -> Dict[str, Any]:
        """
        Full processing pipeline for an uploaded image:
        1. Save original to storage
        2. Generate thumbnail (400px wide)
        3. Get AI description via Gemini Vision
        4. Extract AI tags and dominant colours
        5. Create vector embedding for semantic search in Qdrant

        Returns dict with all metadata for the MediaAsset record.
        """
        # 1. Save original
        storage_url = await storage.save(file_bytes, filename, mime_type, user_id)

        # 2. Generate thumbnail
        thumbnail_url = None
        if mime_type.startswith("image/"):
            thumbnail_url = await self._create_thumbnail(file_bytes, filename, user_id)

        # 3. Get dimensions
        width, height = None, None
        if mime_type.startswith("image/"):
            try:
                img = Image.open(io.BytesIO(file_bytes))
                width, height = img.size
            except Exception as e:
                logger.warning("Could not read image dimensions: %s", e)

        # 4. AI description + tags + colours via Gemini Vision
        ai_description = ""
        ai_tags = []
        ai_colors = []

        if mime_type.startswith("image/"):
            try:
                vision_result = await self._analyze_image(file_bytes, mime_type)
                ai_description = vision_result.get("description", "")
                ai_tags = vision_result.get("tags", [])
                ai_colors = vision_result.get("colors", [])
            except Exception as e:
                logger.warning("Vision analysis failed for %s: %s", filename, e)

        # 5. Create embedding in Qdrant for semantic search
        embedding_id = None
        if ai_description:
            try:
                embedding_id = await self._create_embedding(ai_description, user_id)
            except Exception as e:
                logger.warning("Embedding creation failed for %s: %s", filename, e)

        return {
            "storage_url": storage_url,
            "thumbnail_url": thumbnail_url,
            "ai_description": ai_description,
            "ai_tags": ai_tags,
            "ai_colors": ai_colors,
            "ai_embedding_id": embedding_id,
            "width": width,
            "height": height,
        }

    async def _create_thumbnail(self, file_bytes: bytes, filename: str, user_id: str) -> str:
        """Generate a 400px-wide thumbnail."""
        img = Image.open(io.BytesIO(file_bytes))
        img.thumbnail((400, 400))

        buf = io.BytesIO()
        # Convert RGBA to RGB for JPEG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(buf, format="JPEG", quality=85)
        thumb_bytes = buf.getvalue()

        thumb_name = f"thumb_{filename}"
        return await storage.save(thumb_bytes, thumb_name, "image/jpeg", user_id)

    async def _analyze_image(self, file_bytes: bytes, mime_type: str) -> Dict[str, Any]:
        """
        Use Gemini Vision to analyze the image.
        Returns description, tags, and dominant colours.
        """
        from vertexai.generative_models import GenerativeModel, Part

        model = GenerativeModel(settings.GEMINI_FLASH_MODEL)

        image_part = Part.from_data(data=file_bytes, mime_type=mime_type)

        prompt = """Analyze this image and return a JSON object with:
        {
            "description": "A detailed, natural description of what's in the image (2-3 sentences, describe the subject, setting, lighting, mood)",
            "tags": ["tag1", "tag2", ...],  // 5-10 relevant tags for searching
            "colors": ["#hex1", "#hex2", "#hex3"]  // 3-5 dominant hex colours
        }
        Return ONLY the JSON, no markdown fences."""

        response = await model.generate_content_async([image_part, prompt])

        try:
            result = json.loads(response.text.strip())
            return result
        except json.JSONDecodeError:
            return {"description": response.text.strip(), "tags": [], "colors": []}

    async def _create_embedding(self, description: str, user_id: str) -> Optional[str]:
        """Create a vector embedding in Qdrant for semantic image search."""
        from services.core.knowledge.pipeline import KnowledgePipeline

        pipeline = KnowledgePipeline()

        # Ensure the media collection exists
        collection = f"guild_media_{user_id.replace('-', '_')}"
        pipeline._ensure_collection(collection, dim=768)

        # Generate embedding
        embeddings = await pipeline._generate_embeddings([description])

        if embeddings:
            # Create a unique point ID
            point_id_hex = hashlib.md5(f"{user_id}:{description[:100]}".encode()).hexdigest()
            point_id_int = int(point_id_hex[:16], 16)

            qdrant = pipeline._get_qdrant()
            if qdrant:
                try:
                    from qdrant_client.models import models
                    qdrant.upsert(
                        collection_name=collection,
                        points=[models.PointStruct(
                            id=point_id_int,
                            vector=embeddings[0],
                            payload={
                                "text": description,
                                "type": "media_asset",
                                "user_id": user_id,
                            },
                        )],
                    )
                    return str(point_id_int)
                except Exception as e:
                    logger.error("Qdrant upsert for media failed: %s", e)

        return None


media_processor = MediaProcessor()
