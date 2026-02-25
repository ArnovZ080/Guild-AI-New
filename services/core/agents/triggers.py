import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from services.core.logging import logger
from services.core.agents.models import TaskStatus

class TriggerSpec(BaseModel):
    id: str
    name: str
    description: str
    agent_id: str
    intent: str
    frequency: str  # "daily", "weekly", "monthly"
    last_run: Optional[datetime] = None
    next_run: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
    active: bool = True

class TriggerManager:
    """
    Manages autonomous, recurring triggers for agent tasks.
    """
    def __init__(self):
        self.triggers: Dict[str, TriggerSpec] = {}

    def create_trigger(self, name: str, description: str, agent_id: str, intent: str, frequency: str) -> TriggerSpec:
        trigger_id = str(uuid.uuid4())
        
        now = datetime.now()
        next_run = self._calculate_next_run(now, frequency)
        
        trigger = TriggerSpec(
            id=trigger_id,
            name=name,
            description=description,
            agent_id=agent_id,
            intent=intent,
            frequency=frequency,
            next_run=next_run
        )
        
        self.triggers[trigger_id] = trigger
        logger.info(f"Created recurring trigger: {name} ({frequency})")
        return trigger

    def _calculate_next_run(self, from_time: datetime, frequency: str) -> datetime:
        if frequency == "daily":
            return from_time + timedelta(days=1)
        elif frequency == "weekly":
            return from_time + timedelta(weeks=1)
        elif frequency == "monthly":
            # Simple 30-day month approximation for now
            return from_time + timedelta(days=30)
        else:
            return from_time + timedelta(days=1)

    def get_runnable_triggers(self) -> List[TriggerSpec]:
        now = datetime.now()
        runnable = []
        for trigger in self.triggers.values():
            if trigger.active and trigger.next_run <= now:
                runnable.append(trigger)
        return runnable

    def mark_executed(self, trigger_id: str):
        if trigger_id in self.triggers:
            trigger = self.triggers[trigger_id]
            trigger.last_run = datetime.now()
            trigger.next_run = self._calculate_next_run(trigger.last_run, trigger.frequency)
            logger.info(f"Trigger {trigger.name} executed. Next run scheduled for {trigger.next_run}")

# Global instance
trigger_manager = TriggerManager()
