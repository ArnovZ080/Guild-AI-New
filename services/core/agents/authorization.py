import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from services.core.db.models import AgentAuthorization
from services.core.logging import logger

class AuthorizationQueue:
    """
    Queue for human-in-the-loop authorization requests using PostgreSQL.
    """

    @classmethod
    async def create_request(
        cls, db: AsyncSession, user_id: str, task_id: str, agent_id: str, action_type: str, description: str, params: Dict[str, Any]
    ) -> AgentAuthorization:
        request = AgentAuthorization(
            user_id=user_id,
            task_id=task_id,
            agent_id=agent_id,
            action_type=action_type,
            description=description,
            params=params,
            status="pending"
        )
        db.add(request)
        await db.commit()
        await db.refresh(request)
        
        logger.info(f"AuthorizationQueue: Authorization required [{description}] (Type: {action_type}) for user {user_id}")
        return request

    @classmethod
    async def approve(cls, db: AsyncSession, request_id: str) -> bool:
        stmt = select(AgentAuthorization).where(AgentAuthorization.id == request_id)
        result = await db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if request and request.status == "pending":
            request.status = "approved"
            await db.commit()
            logger.info(f"AuthorizationQueue: Authorized [{request.description}]")
            return True
        return False

    @classmethod
    async def reject(cls, db: AsyncSession, request_id: str) -> bool:
        stmt = select(AgentAuthorization).where(AgentAuthorization.id == request_id)
        result = await db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if request and request.status == "pending":
            request.status = "rejected"
            await db.commit()
            logger.info(f"AuthorizationQueue: Rejected [{request.description}]")
            return True
        return False

    @classmethod
    async def list_pending(cls, db: AsyncSession, user_id: str) -> List[AgentAuthorization]:
        stmt = select(AgentAuthorization).where(
            AgentAuthorization.user_id == user_id,
            AgentAuthorization.status == "pending"
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())
