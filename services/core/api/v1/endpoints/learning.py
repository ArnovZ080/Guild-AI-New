from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.api import deps
from services.core.db.models import UserAccount, AdaptiveLearningSignal, CustomerJourney

router = APIRouter()

# --- Learning / Preferences ---
@router.get("/preferences")
async def get_learning_preferences(
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """Get adaptive learning preferences for the current user."""
    result = await db.execute(
        select(AdaptiveLearningSignal).where(
            AdaptiveLearningSignal.user_id == current_user.id
        ).limit(100)
    )
    signals = result.scalars().all()
    return {
        "signals": [
            {
                "id": s.id,
                "signal_type": s.signal_type,
                "data": s.data,
                "created_at": str(s.created_at),
            }
            for s in signals
        ]
    }

# --- Customer Journeys ---
@router.get("/customers")
async def list_customer_journeys(
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """List customer journeys for the current user."""
    result = await db.execute(
        select(CustomerJourney).where(CustomerJourney.user_id == current_user.id)
    )
    journeys = result.scalars().all()
    return {
        "journeys": [
            {
                "id": j.id,
                "customer_email": j.customer_email,
                "segment": j.segment,
                "status": j.status,
            }
            for j in journeys
        ]
    }
