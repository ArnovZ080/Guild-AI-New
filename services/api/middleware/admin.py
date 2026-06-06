"""
Admin Middleware

Provides dependency to enforce admin-only access for certain routes.
"""
from fastapi import Depends, HTTPException, status
from services.core.db.models import UserAccount
from services.api.middleware.auth import get_current_user

async def require_admin(current_user: UserAccount = Depends(get_current_user)) -> UserAccount:
    """Dependency that ensures the current user is an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )
    return current_user
