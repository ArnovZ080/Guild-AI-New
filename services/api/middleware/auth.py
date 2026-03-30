"""
Firebase Authentication Middleware

Verifies Firebase JWT tokens and extracts user identity.
"""
import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.base import get_db
from services.core.db.models import UserAccount
from services.core.config import settings

logger = logging.getLogger(__name__)

# Firebase Admin SDK initialization
_firebase_app = None


def _init_firebase():
    """Initialize Firebase Admin SDK (lazy, once)."""
    global _firebase_app
    if _firebase_app is not None:
        return

    try:
        import firebase_admin
        from firebase_admin import credentials

        # Use Application Default Credentials (ADC) on GCP
        # Locally, set GOOGLE_APPLICATION_CREDENTIALS env var
        _firebase_app = firebase_admin.initialize_app()
        logger.info("Firebase Admin SDK initialized (project: %s).", settings.FIREBASE_PROJECT_ID)
    except Exception as e:
        logger.warning("Firebase Admin SDK init failed: %s. Auth will use dev mode.", e)


_init_firebase()

security = HTTPBearer(auto_error=False)


async def verify_firebase_token(
    token: str,
) -> Optional[dict]:
    """
    Verify a Firebase ID token and return the decoded claims.
    Returns None if verification fails.
    """
    try:
        from firebase_admin import auth as firebase_auth
        decoded = firebase_auth.verify_id_token(token)
        return decoded
    except Exception as e:
        logger.warning("Firebase token verification failed: %s", e)
        return None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> UserAccount:
    """
    FastAPI dependency — resolves the current authenticated user.

    Verifies the Firebase JWT, looks up the user in PostgreSQL.
    Raises 401 if unauthenticated.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = credentials.credentials
    claims = await verify_firebase_token(token)

    if not claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    firebase_uid = claims.get("uid")
    if not firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
        )

    # Look up user in DB
    result = await db.execute(
        select(UserAccount).where(UserAccount.firebase_uid == firebase_uid)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Complete registration first.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated",
        )

    return user
