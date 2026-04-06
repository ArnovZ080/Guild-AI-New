"""Dashboard API Routes — CEO snapshot migrated from v1"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from services.core.db.base import get_db
from services.core.db.models import (
    UserAccount, ContentItem, Contact, Goal, TokenUsage,
    WorkflowExecution, CalendarEvent,
)
from services.api.middleware.auth import get_current_user

router = APIRouter()


@router.get("/snapshot")
async def dashboard_snapshot(
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    """Returns a comprehensive growth dashboard snapshot."""
    uid = current_user.id
    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    content_total = (await db.execute(
        select(func.count(ContentItem.id)).where(ContentItem.user_id == uid)
    )).scalar() or 0

    content_published = (await db.execute(
        select(func.count(ContentItem.id)).where(
            ContentItem.user_id == uid, ContentItem.status == "published"
        )
    )).scalar() or 0

    contacts_total = (await db.execute(
        select(func.count(Contact.id)).where(Contact.user_id == uid)
    )).scalar() or 0

    goals_active = (await db.execute(
        select(func.count(Goal.id)).where(Goal.user_id == uid, Goal.status == "active")
    )).scalar() or 0

    tokens_month = (await db.execute(
        select(func.sum(TokenUsage.total_tokens)).where(
            TokenUsage.user_id == uid,
            TokenUsage.created_at >= start_of_month,
        )
    )).scalar() or 0

    return {
        "user_tier": current_user.tier,
        "content_total": content_total,
        "content_published": content_published,
        "contacts_total": contacts_total,
        "goals_active": goals_active,
        "tokens_used_this_month": tokens_month,
    }
