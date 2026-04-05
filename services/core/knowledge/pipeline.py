"""
Knowledge Pipeline — Document Ingestion, Embedding, and RAG Retrieval

Ingests documents (PDF, DOCX, TXT, URLs), chunks text, generates embeddings
via Vertex AI, stores in Qdrant vector store (user-scoped collections).
"""
import logging
import hashlib
import re
from typing import Optional, List, Dict, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.config import settings
from services.core.db.models import KnowledgeDocument

logger = logging.getLogger(__name__)

# Embedding model via Vertex AI
EMBEDDING_MODEL = "text-embedding-005"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64


class KnowledgePipeline:
    """Processes documents → chunks → embeddings → Qdrant"""

    def __init__(self):
        self._qdrant = None

    def _get_qdrant(self):
        if self._qdrant is None:
            try:
                from qdrant_client import QdrantClient
                self._qdrant = QdrantClient(url=settings.QDRANT_URL)
            except Exception as e:
                logger.error("Qdrant connection failed: %s", e)
        return self._qdrant

    def _collection_name(self, user_id: str) -> str:
        return f"guild_kb_{user_id.replace('-', '_')}"

    async def ingest_document(
        self,
        db: AsyncSession,
        user_id: str,
        filename: str,
        content: str,
        content_type: str = "text",
    ) -> KnowledgeDocument:
        """
        Process a document for the knowledge base:
        1. Chunk into semantic segments
        2. Generate embeddings via Vertex AI
        3. Store in Qdrant with user-scoped collection
        4. Record in knowledge_documents table
        """
        chunks = self._chunk_text(content)
        embeddings = await self._generate_embeddings(chunks)

        # Ensure Qdrant collection exists
        collection = self._collection_name(user_id)
        self._ensure_collection(collection, dim=len(embeddings[0]) if embeddings else 768)

        # Upsert to Qdrant
        doc_id = hashlib.md5(f"{user_id}:{filename}".encode()).hexdigest()
        self._upsert_vectors(collection, doc_id, chunks, embeddings, {
            "user_id": user_id, "filename": filename, "content_type": content_type,
        })

        # Record in DB
        doc = KnowledgeDocument(
            user_id=user_id,
            filename=filename,
            content_type=content_type,
            chunk_count=len(chunks),
            embedded_at=datetime.utcnow(),
            doc_metadata={"chunk_size": CHUNK_SIZE, "model": EMBEDDING_MODEL},
        )
        db.add(doc)
        await db.commit()
        await db.refresh(doc)

        logger.info("Ingested '%s' → %d chunks for user %s", filename, len(chunks), user_id)
        return doc

    async def ingest_url(self, db: AsyncSession, user_id: str, url: str) -> KnowledgeDocument:
        """Scrape and ingest a web page."""
        import httpx
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            text = self._html_to_text(resp.text)

        return await self.ingest_document(db, user_id, url, text, "url")

    async def ingest_business_website(self, db: AsyncSession, user_id: str, website_url: str) -> dict:
        """
        Onboarding helper: scrape user's website to auto-populate identity.
        Returns extracted fields.
        """
        import httpx
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get(website_url)
            resp.raise_for_status()
            text = self._html_to_text(resp.text)

        # Also ingest into knowledge base
        await self.ingest_document(db, user_id, website_url, text, "website")

        # Use LLM to extract business identity fields
        from services.core.llm import default_llm, ModelTier
        import json

        prompt = f"""Extract business information from this website content:

{text[:3000]}

Return JSON with any fields you can identify:
{{"business_name": "", "niche": "", "industry": "", "target_audience": "",
  "brand_story": "", "pricing_strategy": "", "marketing_channels": []}}"""

        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.2, tier=ModelTier.FLASH)
            return json.loads(res.strip().strip('`').replace('json\n', '').strip())
        except Exception:
            return {"website_ingested": True, "auto_extract_failed": True}

    async def query(
        self,
        user_id: str,
        query_text: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Semantic search across user's knowledge base."""
        embeddings = await self._generate_embeddings([query_text])
        if not embeddings:
            return []

        collection = self._collection_name(user_id)
        qdrant = self._get_qdrant()
        if not qdrant:
            return []

        try:
            from qdrant_client.models import models
            results = qdrant.query_points(
                collection_name=collection,
                query=embeddings[0],
                limit=top_k,
            )
            return [
                {
                    "text": point.payload.get("text", ""),
                    "filename": point.payload.get("filename", ""),
                    "score": point.score,
                }
                for point in results.points
            ]
        except Exception as e:
            logger.error("Qdrant query failed: %s", e)
            return []

    # ── Internal ──

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), CHUNK_SIZE - CHUNK_OVERLAP):
            chunk = " ".join(words[i:i + CHUNK_SIZE])
            if chunk.strip():
                chunks.append(chunk)
        return chunks or [text[:2000]]

    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings via Vertex AI."""
        try:
            from vertexai.language_models import TextEmbeddingModel
            import asyncio

            model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)
            loop = asyncio.get_event_loop()

            # Batch in groups of 5
            all_embeddings = []
            for i in range(0, len(texts), 5):
                batch = texts[i:i + 5]
                result = await loop.run_in_executor(
                    None, lambda b=batch: model.get_embeddings(b)
                )
                all_embeddings.extend([e.values for e in result])

            return all_embeddings
        except Exception as e:
            logger.error("Embedding generation failed: %s", e)
            return []

    def _ensure_collection(self, collection: str, dim: int = 768):
        """Create Qdrant collection if it doesn't exist."""
        qdrant = self._get_qdrant()
        if not qdrant:
            return
        try:
            from qdrant_client.models import models
            qdrant.create_collection(
                collection_name=collection,
                vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE),
            )
        except Exception:
            pass  # Already exists

    def _upsert_vectors(self, collection: str, doc_id: str,
                        chunks: List[str], embeddings: List[List[float]], meta: dict):
        """Upsert chunk vectors to Qdrant."""
        qdrant = self._get_qdrant()
        if not qdrant or not embeddings:
            return
        try:
            from qdrant_client.models import models
            points = []
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                point_id = hashlib.md5(f"{doc_id}:{i}".encode()).hexdigest()
                # Convert hex string to int for Qdrant
                point_id_int = int(point_id[:16], 16)
                points.append(models.PointStruct(
                    id=point_id_int,
                    vector=emb,
                    payload={"text": chunk, "chunk_index": i, **meta},
                ))
            qdrant.upsert(collection_name=collection, points=points)
        except Exception as e:
            logger.error("Qdrant upsert failed: %s", e)

    def _html_to_text(self, html: str) -> str:
        """Simple HTML to text conversion."""
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


# Global
knowledge_pipeline = KnowledgePipeline()
