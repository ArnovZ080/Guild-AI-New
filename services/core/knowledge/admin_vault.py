"""
Admin Vault Pipeline — Global Knowledge Base
Ingests, chunks, embeds, and stores global admin knowledge in Qdrant.
"""
import logging
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from services.core.config import settings
from services.core.db.models import AdminKnowledge
from services.core.knowledge.pipeline import knowledge_pipeline

logger = logging.getLogger(__name__)

GLOBAL_COLLECTION = "admin_knowledge"

class AdminVaultPipeline:
    """Manages the global Admin Knowledge Base."""

    async def ingest_document(
        self,
        db: AsyncSession,
        uploaded_by: str,
        filename: str,
        content: str,
        category: str,
        tags: List[str] = None,
        description: str = None,
        source_url: str = None,
    ) -> AdminKnowledge:
        """
        Ingest admin knowledge into DB and Qdrant.
        """
        # Chunk and embed
        chunks = knowledge_pipeline._chunk_text(content)
        embeddings = await knowledge_pipeline._generate_embeddings(chunks)
        
        # Ensure collection exists
        knowledge_pipeline._ensure_collection(GLOBAL_COLLECTION, dim=len(embeddings[0]) if embeddings else 768)

        # Record in DB
        doc = AdminKnowledge(
            uploaded_by=uploaded_by,
            title=filename,
            filename=filename,
            content=content,
            content_type="text/markdown",
            category=category,
            tags=tags or [],
            description=description,
            source_url=source_url,
            chunk_count=len(chunks),
            is_embedded=True,
            is_active=True,
        )
        db.add(doc)
        await db.flush()  # To get doc.id
        
        # Upsert to Qdrant
        embedding_ids = []
        qdrant = knowledge_pipeline._get_qdrant()
        if qdrant and embeddings:
            from qdrant_client.models import models
            points = []
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                # Qdrant requires int or UUID string.
                # md5(doc_id:i) to hex, truncate to 16, convert to int
                point_id_str = hashlib.md5(f"{doc.id}:{i}".encode()).hexdigest()
                point_id_int = int(point_id_str[:16], 16)
                embedding_ids.append(point_id_int)
                
                points.append(models.PointStruct(
                    id=point_id_int,
                    vector=emb,
                    payload={
                        "doc_id": doc.id,
                        "text": chunk,
                        "chunk_index": i,
                        "filename": filename,
                        "category": category,
                    },
                ))
            try:
                qdrant.upsert(collection_name=GLOBAL_COLLECTION, points=points)
                doc.embedding_ids = embedding_ids
                doc.is_embedded = True
            except Exception as e:
                logger.error("Failed to upsert admin knowledge to Qdrant: %s", e)
                doc.is_embedded = False

        await db.commit()
        await db.refresh(doc)
        
        logger.info(f"Admin ingested '{filename}' -> {len(chunks)} chunks.")
        return doc

    async def query(self, query_text: str, top_k: int = 3, category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query the global admin vault."""
        embeddings = await knowledge_pipeline._generate_embeddings([query_text])
        if not embeddings:
            return []

        qdrant = knowledge_pipeline._get_qdrant()
        if not qdrant:
            return []

        try:
            from qdrant_client.models import models
            query_filter = None
            if category_filter:
                query_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="category",
                            match=models.MatchValue(value=category_filter)
                        )
                    ]
                )
                
            results = qdrant.query_points(
                collection_name=GLOBAL_COLLECTION,
                query=embeddings[0],
                query_filter=query_filter,
                limit=top_k,
            )
            return [
                {
                    "text": point.payload.get("text", ""),
                    "filename": point.payload.get("filename", ""),
                    "category": point.payload.get("category", ""),
                    "score": point.score,
                }
                for point in results.points
            ]
        except Exception as e:
            logger.error("Admin Qdrant query failed: %s", e)
            return []

    async def list_documents(self, db: AsyncSession, category: Optional[str] = None, search: Optional[str] = None) -> List[AdminKnowledge]:
        stmt = select(AdminKnowledge)
        if category:
            stmt = stmt.where(AdminKnowledge.category == category)
        if search:
            stmt = stmt.where(AdminKnowledge.title.ilike(f"%{search}%"))
        stmt = stmt.order_by(AdminKnowledge.created_at.desc())
        res = await db.execute(stmt)
        return list(res.scalars().all())

    async def toggle_document(self, db: AsyncSession, doc_id: str) -> Optional[AdminKnowledge]:
        res = await db.execute(select(AdminKnowledge).where(AdminKnowledge.id == doc_id))
        doc = res.scalars().first()
        if not doc:
            return None
        
        doc.is_active = not doc.is_active
        await db.commit()
        await db.refresh(doc)
        return doc

    async def delete_document(self, db: AsyncSession, doc_id: str) -> bool:
        res = await db.execute(select(AdminKnowledge).where(AdminKnowledge.id == doc_id))
        doc = res.scalars().first()
        if not doc:
            return False
            
        # Delete from Qdrant
        qdrant = knowledge_pipeline._get_qdrant()
        if qdrant and doc.embedding_ids:
            try:
                from qdrant_client.models import models
                qdrant.delete(
                    collection_name=GLOBAL_COLLECTION,
                    points_selector=models.PointIdsList(
                        points=doc.embedding_ids
                    ),
                )
            except Exception as e:
                logger.error("Failed to delete admin points from Qdrant: %s", e)
                
        # Delete from DB
        await db.delete(doc)
        await db.commit()
        return True

    async def get_categories(self, db: AsyncSession) -> List[str]:
        stmt = select(AdminKnowledge.category).distinct()
        res = await db.execute(stmt)
        return [r for r in res.scalars().all()]

admin_vault_pipeline = AdminVaultPipeline()
