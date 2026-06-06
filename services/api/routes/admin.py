"""
Admin Vault API Routes

CRUD and search endpoints for the global Admin Knowledge Vault.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any

from services.core.db.base import get_db
from services.core.db.models import UserAccount
from services.api.middleware.admin import require_admin
from services.core.knowledge.admin_vault import admin_vault_pipeline

router = APIRouter()

class UploadKnowledgeRequest(BaseModel):
    title: str
    filename: str
    content: str
    category: str
    tags: Optional[List[str]] = []
    description: Optional[str] = None
    source_url: Optional[str] = None

class AdminKnowledgeResponse(BaseModel):
    id: str
    uploaded_by: str
    title: str
    filename: str
    category: str
    tags: list
    description: Optional[str]
    source_url: Optional[str]
    is_embedded: bool
    chunk_count: int
    is_active: bool

    model_config = {"from_attributes": True}

@router.post("/vault/upload", response_model=AdminKnowledgeResponse)
async def upload_knowledge(
    request: UploadKnowledgeRequest,
    current_admin: UserAccount = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Upload new knowledge into the global vault."""
    try:
        doc = await admin_vault_pipeline.ingest_document(
            db=db,
            uploaded_by=current_admin.id,
            filename=request.filename,
            content=request.content,
            category=request.category,
            tags=request.tags,
            description=request.description,
            source_url=request.source_url,
        )
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vault/", response_model=List[AdminKnowledgeResponse])
async def list_knowledge(
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_admin: UserAccount = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all knowledge documents, optionally filtered."""
    docs = await admin_vault_pipeline.list_documents(db, category=category, search=search)
    return docs

@router.post("/vault/{doc_id}/toggle", response_model=AdminKnowledgeResponse)
async def toggle_knowledge(
    doc_id: str,
    current_admin: UserAccount = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Toggle a document's active status."""
    doc = await admin_vault_pipeline.toggle_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/vault/{doc_id}")
async def delete_knowledge(
    doc_id: str,
    current_admin: UserAccount = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Permanently delete a document from DB and Qdrant."""
    success = await admin_vault_pipeline.delete_document(db, doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "deleted"}

@router.get("/vault/categories", response_model=List[str])
async def list_categories(
    current_admin: UserAccount = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all unique categories in the vault."""
    return await admin_vault_pipeline.get_categories(db)
