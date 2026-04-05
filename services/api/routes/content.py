"""Content Pipeline API Routes"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.db.base import get_db
from services.core.db.models import UserAccount, ContentItem
from services.api.middleware.auth import get_current_user
from services.core.content_pipeline.engine import (
    content_generator, content_queue, content_publisher, content_scheduler)

router = APIRouter()


class GenerateRequest(BaseModel):
    content_type: str = "social"
    platform: str = "linkedin"
    topic: str = ""
    batch: bool = False
    week_start: Optional[str] = None


class EditRequest(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class BulkApproveRequest(BaseModel):
    content_item_ids: List[str]


class RejectRequest(BaseModel):
    feedback: str


class RegenerateRequest(BaseModel):
    feedback: str


@router.post("/generate")
async def generate_content(
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    if request.batch:
        ws = date.fromisoformat(request.week_start) if request.week_start else date.today()
        items = await content_generator.generate_weekly_content(db, current_user.id, ws)
        return {"generated": len(items), "items": [{"id": i.id, "title": i.title, "platform": i.platform} for i in items]}
    else:
        item = await content_generator.generate_single_content(
            db, current_user.id, request.content_type, request.platform, request.topic)
        return {"id": item.id, "title": item.title, "body": item.body, "status": item.status}


@router.get("/queue")
async def get_queue(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    items = await content_queue.get_pending_review(db, current_user.id)
    return {"items": [{"id": i.id, "title": i.title, "body": i.body, "platform": i.platform,
                       "content_type": i.content_type, "created_at": i.created_at.isoformat()} for i in items]}


@router.post("/{content_id}/approve")
async def approve_content(content_id: str, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    item = await content_queue.approve(db, content_id)
    return {"id": item.id, "status": item.status}


@router.post("/{content_id}/reject")
async def reject_content(content_id: str, request: RejectRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    item = await content_queue.reject(db, content_id, request.feedback)
    return {"id": item.id, "status": item.status}


@router.put("/{content_id}/edit")
async def edit_content(content_id: str, request: EditRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    item = await content_queue.edit(db, content_id, request.model_dump(exclude_none=True))
    return {"id": item.id, "status": item.status}


@router.post("/bulk-approve")
async def bulk_approve(request: BulkApproveRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    items = await content_queue.bulk_approve(db, request.content_item_ids)
    return {"approved": len(items)}


@router.get("/published")
async def get_published(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    from sqlalchemy import select
    result = await db.execute(
        select(ContentItem).where(ContentItem.user_id == current_user.id, ContentItem.status == "published")
        .order_by(ContentItem.published_at.desc()).limit(50))
    items = list(result.scalars().all())
    return {"items": [{"id": i.id, "title": i.title, "platform": i.platform,
                       "published_at": i.published_at.isoformat() if i.published_at else None} for i in items]}


@router.get("/performance")
async def get_performance(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    from sqlalchemy import select, func
    total = await db.execute(select(func.count(ContentItem.id)).where(ContentItem.user_id == current_user.id))
    published = await db.execute(select(func.count(ContentItem.id)).where(
        ContentItem.user_id == current_user.id, ContentItem.status == "published"))
    return {"total": total.scalar() or 0, "published": published.scalar() or 0}


@router.post("/{content_id}/regenerate")
async def regenerate(content_id: str, request: RegenerateRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    item = await content_generator.regenerate_content(db, content_id, request.feedback)
    return {"id": item.id, "title": item.title, "status": item.status}
