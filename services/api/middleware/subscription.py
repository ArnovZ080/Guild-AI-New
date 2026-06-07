from fastapi import Depends, HTTPException, status
from services.core.db.models import UserAccount
from services.api.middleware.auth import get_current_user
from datetime import datetime

async def check_subscription(current_user: UserAccount = Depends(get_current_user)):
    """
    Dependency to verify if a user has an active subscription or an active trial.
    Admin users bypass this check.
    """
    if current_user.is_admin:
        return current_user
        
    if current_user.subscription_status == "active":
        return current_user
        
    if current_user.trial_ends_at and current_user.trial_ends_at > datetime.utcnow():
        return current_user
        
    raise HTTPException(
        status_code=402,
        detail="trial_expired"
    )
