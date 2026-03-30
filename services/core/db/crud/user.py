from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from services.core.db.models import UserAccount
from services.core.security.jwt import get_password_hash

async def get_user(db: AsyncSession, user_id: str) -> Optional[UserAccount]:
    result = await db.execute(select(UserAccount).filter(UserAccount.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserAccount]:
    result = await db.execute(select(UserAccount).filter(UserAccount.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, email: str, password: str, tier: str = "free") -> UserAccount:
    hashed_password = get_password_hash(password)
    db_user = UserAccount(email=email, hashed_password=hashed_password, tier=tier)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
