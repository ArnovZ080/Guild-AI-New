"""
Auth API Routes

POST /api/auth/verify   — Verify Firebase token and return user profile
POST /api/auth/register — Create user record in PostgreSQL after Firebase signup
GET  /api/auth/me       — Get current user profile
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from services.core.db.base import get_db
from services.core.db.models import UserAccount, BusinessIdentity
from services.api.middleware.auth import get_current_user, verify_firebase_token

router = APIRouter()


class RegisterRequest(BaseModel):
    firebase_token: str
    email: EmailStr
    name: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    subscription_tier: str
    is_active: bool
    has_business_identity: bool

    model_config = {"from_attributes": True}


@router.post("/register", response_model=UserResponse)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a user record in PostgreSQL after Firebase signup.
    Called once after the frontend creates a Firebase account.
    """
    # Verify the Firebase token
    claims = await verify_firebase_token(request.firebase_token)
    if not claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token",
        )

    firebase_uid = claims.get("uid")

    # Check if already registered
    result = await db.execute(
        select(UserAccount).where(UserAccount.firebase_uid == firebase_uid)
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )

    # Create user
    user = UserAccount(
        firebase_uid=firebase_uid,
        email=request.email,
        name=request.name,
        subscription_tier="free",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        subscription_tier=user.subscription_tier,
        is_active=user.is_active,
        has_business_identity=False,
    )


@router.post("/verify", response_model=UserResponse)
async def verify_token(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Verify a Firebase token and return the user profile."""
    claims = await verify_firebase_token(request.firebase_token)
    if not claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token",
        )

    firebase_uid = claims.get("uid")
    result = await db.execute(
        select(UserAccount).where(UserAccount.firebase_uid == firebase_uid)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered",
        )

    # Check if they have a business identity
    bi_result = await db.execute(
        select(BusinessIdentity).where(BusinessIdentity.user_id == user.id)
    )
    has_bi = bi_result.scalars().first() is not None

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        subscription_tier=user.subscription_tier,
        is_active=user.is_active,
        has_business_identity=has_bi,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserAccount = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current authenticated user's profile."""
    bi_result = await db.execute(
        select(BusinessIdentity).where(BusinessIdentity.user_id == current_user.id)
    )
    has_bi = bi_result.scalars().first() is not None

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        subscription_tier=current_user.subscription_tier,
        is_active=current_user.is_active,
        has_business_identity=has_bi,
    )
