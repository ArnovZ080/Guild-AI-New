import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from services.core.db.models import AgentTrigger
from services.core.logging import logger
from services.core.agents.models import TaskStatus

class TriggerManager:
    """
    Manages autonomous, recurring triggers for agent tasks using PostgreSQL.
    """
    
    @classmethod
    async def create_trigger(
        cls, db: AsyncSession, user_id: str, name: str, description: str, 
        agent_id: str, intent: str, frequency: str
    ) -> AgentTrigger:
        now = datetime.utcnow()
        next_run = cls._calculate_next_run(now, frequency)
        
        trigger = AgentTrigger(
            user_id=user_id,
            name=name,
            description=description,
            agent_id=agent_id,
            intent=intent,
            frequency=frequency,
            next_run=next_run,
            metadata_json={}
        )
        
        db.add(trigger)
        await db.commit()
        await db.refresh(trigger)
        
        logger.info(f"TriggerManager: Created recurring trigger [{name}] ({frequency}) for user {user_id}")
        return trigger

    @classmethod
    def _calculate_next_run(cls, from_time: datetime, frequency: str) -> datetime:
        if frequency == "daily":
            return from_time + timedelta(days=1)
        elif frequency == "weekly":
            return from_time + timedelta(weeks=1)
        elif frequency == "monthly":
            # Simple 30-day month approximation for now
            return from_time + timedelta(days=30)
        else:
            return from_time + timedelta(days=1)

    @classmethod
    async def get_runnable_triggers(cls, db: AsyncSession, user_id: str) -> List[AgentTrigger]:
        now = datetime.utcnow()
        stmt = select(AgentTrigger).where(
            AgentTrigger.user_id == user_id,
            AgentTrigger.active == True,
            AgentTrigger.next_run <= now
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def mark_executed(cls, db: AsyncSession, trigger_id: str):
        stmt = select(AgentTrigger).where(AgentTrigger.id == trigger_id)
        result = await db.execute(stmt)
        trigger = result.scalar_one_or_none()
        
        if trigger:
            trigger.last_run = datetime.utcnow()
            trigger.next_run = cls._calculate_next_run(trigger.last_run, trigger.frequency)
            await db.commit()
            logger.info(f"TriggerManager: Trigger {trigger.name} executed. Next run scheduled for {trigger.next_run}")

