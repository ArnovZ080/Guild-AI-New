"""Subscription tier enforcement for content/video generation."""
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from services.core.db.base import get_db
from services.core.db.models import UserAccount, ContentItem
from services.api.middleware.auth import get_current_user

TIER_LIMITS = {
    "free": {"content_per_month": 10, "videos_per_month": 0, "max_platforms": 2},
    "starter": {"content_per_month": 50, "videos_per_month": 0, "max_platforms": 3},
    "growth": {"content_per_month": 200, "videos_per_month": 10, "max_platforms": 99},
    "scale": {"content_per_month": 500, "videos_per_month": 30, "max_platforms": 99},
}


async def enforce_content_limit(
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    """Dependency that checks whether the user has remaining content quota."""
    tier = current_user.tier or "free"
    limits = TIER_LIMITS.get(tier, TIER_LIMITS["free"])

    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    count = (await db.execute(
        select(func.count(ContentItem.id)).where(
            ContentItem.user_id == current_user.id,
            ContentItem.created_at >= start_of_month,
        )
    )).scalar() or 0

    if count >= limits["content_per_month"]:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Monthly content limit reached",
                "limit": limits["content_per_month"],
                "used": count,
                "tier": tier,
                "upgrade_url": "/pricing",
            },
        )
    return current_user
