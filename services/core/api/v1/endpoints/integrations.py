from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.api import deps
from services.core.api.schemas import IntegrationConnectRequest
from services.core.db.models import UserAccount, IntegrationCredential

router = APIRouter()

@router.get("")
async def list_integrations(
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """List all connected integrations for the current user."""
    result = await db.execute(
        select(IntegrationCredential).where(IntegrationCredential.user_id == current_user.id)
    )
    creds = result.scalars().all()
    return {
        "integrations": [
            {
                "id": c.id,
                "platform": c.platform,
                "is_active": c.is_active,
                "created_at": str(c.created_at),
            }
            for c in creds
        ]
    }

@router.post("/connect")
async def connect_integration(
    request: IntegrationConnectRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """Connect a new integration (store encrypted credentials)."""
    cred = IntegrationCredential(
        user_id=current_user.id,
        platform=request.platform,
        credentials=request.credentials,
        is_active=True,
    )
    db.add(cred)
    await db.commit()
    await db.refresh(cred)
    return {"id": cred.id, "platform": cred.platform, "status": "connected"}

@router.delete("/{integration_id}")
async def disconnect_integration(
    integration_id: str,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """Disconnect an integration."""
    result = await db.execute(
        select(IntegrationCredential).where(
            IntegrationCredential.id == integration_id,
            IntegrationCredential.user_id == current_user.id
        )
    )
    cred = result.scalars().first()
    if not cred:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    cred.is_active = False
    await db.commit()
    return {"id": integration_id, "status": "disconnected"}
