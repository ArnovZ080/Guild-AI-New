"""
Business Identity Manager — v2.0

DB-backed, user-scoped. Supports progressive onboarding with completion tracking.
Full schema: ICP, brand voice, brand visual, competitors, goals, challenges.
"""
import logging
from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.models import BusinessIdentity
from services.core.db.base import AsyncSessionLocal

logger = logging.getLogger(__name__)

# Fields and their weight for completion percentage
_FIELDS = {
    "business_name": 10,
    "niche": 5,
    "industry": 5,
    "target_audience": 10,
    "icp": 15,
    "brand_voice": 10,
    "brand_visual": 5,
    "brand_story": 5,
    "competitors": 5,
    "pricing_strategy": 5,
    "marketing_channels": 5,
    "content_preferences": 5,
    "goals_3month": 10,
    "goals_12month": 5,
}


def _compute_completion(identity: BusinessIdentity) -> float:
    """Calculate completion percentage based on filled fields."""
    total_weight = sum(_FIELDS.values())
    filled_weight = 0
    for field, weight in _FIELDS.items():
        val = getattr(identity, field, None)
        if val:
            if isinstance(val, (dict, list)):
                if len(val) > 0:
                    filled_weight += weight
            elif isinstance(val, str) and val.strip():
                filled_weight += weight
    return round((filled_weight / total_weight) * 100, 1)


class BusinessIdentityManager:
    """Manages the persistent business profile per user via PostgreSQL."""

    @classmethod
    async def get(
        cls, db: Optional[AsyncSession], user_id: str
    ) -> Optional[BusinessIdentity]:
        """Get the business identity for a user."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
        try:
            result = await db.execute(
                select(BusinessIdentity).where(BusinessIdentity.user_id == user_id)
            )
            return result.scalars().first()
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def create_or_update(
        cls,
        db: AsyncSession,
        user_id: str,
        data: Dict[str, Any],
    ) -> BusinessIdentity:
        """
        Create or incrementally update the business identity.

        Accepts a dict of field names → values. Only updates provided fields.
        Recalculates completion_percentage after every update.
        """
        result = await db.execute(
            select(BusinessIdentity).where(BusinessIdentity.user_id == user_id)
        )
        identity = result.scalars().first()

        if not identity:
            identity = BusinessIdentity(user_id=user_id)
            db.add(identity)

        # Update only provided fields
        for key, value in data.items():
            if hasattr(identity, key) and key not in ("id", "user_id", "created_at"):
                setattr(identity, key, value)

        identity.completion_percentage = _compute_completion(identity)
        await db.commit()
        await db.refresh(identity)

        logger.info(
            "Business Identity updated for user %s (%.1f%% complete)",
            user_id,
            identity.completion_percentage,
        )
        return identity

    @classmethod
    async def get_context_prompt(
        cls, db: Optional[AsyncSession], user_id: str
    ) -> str:
        """
        Generate a rich context prompt for agent injection.

        Includes all known business info: ICP, brand voice, competitors, goals.
        """
        identity = await cls.get(db, user_id)
        if not identity:
            return (
                "## Business Context\n"
                "No business profile available. Proceed with generic professional output.\n"
            )

        sections = ["## Business Context"]

        if identity.business_name:
            sections.append(f"**Business:** {identity.business_name}")
        if identity.niche:
            sections.append(f"**Niche:** {identity.niche}")
        if identity.industry:
            sections.append(f"**Industry:** {identity.industry}")

        if identity.brand_voice and isinstance(identity.brand_voice, dict):
            bv = identity.brand_voice
            sections.append("\n### Brand Voice")
            for k, v in bv.items():
                sections.append(f"- **{k}:** {v}")

        if identity.target_audience:
            sections.append(f"\n### Target Audience\n{identity.target_audience}")

        if identity.icp and isinstance(identity.icp, dict):
            sections.append("\n### Ideal Customer Profile (ICP)")
            for k, v in identity.icp.items():
                sections.append(f"- **{k}:** {v}")

        if identity.competitors and isinstance(identity.competitors, list):
            sections.append(f"\n### Competitors\n{', '.join(str(c) for c in identity.competitors)}")

        if identity.brand_story:
            sections.append(f"\n### Brand Story\n{identity.brand_story}")

        if identity.goals_3month:
            sections.append(f"\n### Goals (3-Month)\n{identity.goals_3month}")
        if identity.goals_12month:
            sections.append(f"\n### Goals (12-Month)\n{identity.goals_12month}")

        if identity.content_preferences and isinstance(identity.content_preferences, dict):
            sections.append("\n### Content Preferences")
            for k, v in identity.content_preferences.items():
                sections.append(f"- **{k}:** {v}")

        if identity.challenges and isinstance(identity.challenges, list):
            sections.append(f"\n### Key Challenges\n{', '.join(str(c) for c in identity.challenges)}")

        return "\n".join(sections)


# Global access
identity_manager = BusinessIdentityManager()
