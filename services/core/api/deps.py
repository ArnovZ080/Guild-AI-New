from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from pydantic import ValidationError

from services.core.db.base import AsyncSessionLocal
from services.core.db.models import UserAccount
from services.core.db.crud import user as crud_user
from services.core.security.jwt import SECRET_KEY, ALGORITHM, decode_access_token

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> UserAccount:
    try:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user ID"
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(
    current_user: UserAccount = Depends(get_current_user),
) -> UserAccount:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

TIER_LIMITS = {
    "free": 50000,       # 50k tokens
    "pro": 1000000,      # 1M tokens
    "enterprise": -1     # unlimited
}

from sqlalchemy import select, func
from datetime import datetime, timedelta
from services.core.db.models import LLMUsageRecord

async def check_tier_limits(
    current_user: UserAccount = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> UserAccount:
    """Check if the user has exceeded their LLM tier limits for the current month."""
    limit = TIER_LIMITS.get(current_user.tier, 0)
    if limit == -1:
        return current_user
        
    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    query = select(func.sum(LLMUsageRecord.total_tokens)).where(
        LLMUsageRecord.user_id == current_user.id,
        LLMUsageRecord.timestamp >= start_of_month
    )
    result = await db.execute(query)
    total_usage = result.scalar() or 0
    
    if total_usage >= limit:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Subscription tier limit exceeded. Used {total_usage} out of {limit} tokens."
        )
        
    return current_user
