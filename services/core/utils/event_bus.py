from typing import List, Optional, Callable
from collections import deque
import threading
import json
import os
import asyncio
try:
    import redis
except ImportError:
    redis = None

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from services.core.db.models import AgentEventRecord
from services.core.agents.models import AgentEvent
from services.core.logging import logger

class EventBus:
    """
    Singleton Event Bus for collecting real-time agent activity.
    Stores a rolling buffer of events in memory, Redis, and permanently in PostgreSQL.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
                cls._instance._init()
            return cls._instance

    def __init__(self):
        # Explicitly define attributes to help linters and ensured they're initialized
        if not hasattr(self, '_initialized'):
            self._buffer = deque(maxlen=1000)
            self._subscribers = []
            self._counter = 0
            
            # Redis initialization
            self.redis_client = None
            if redis:
                redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
                try:
                    self.redis_client = redis.from_url(redis_url, decode_responses=True)
                    self.redis_client.ping()
                    logger.info(f"EventBus: Connected to Redis at {redis_url}")
                except Exception as e:
                    logger.warning(f"EventBus: Redis connection failed, falling back to memory/DB: {e}")
                    self.redis_client = None
            
            self._initialized = True

    def _init(self):
        pass

    async def emit(self, event: AgentEvent, db: Optional[AsyncSession] = None):
        """Add an event to the buffer (Redis/Memory) and save to DB."""
        self._counter += 1
        if not event.id:
            event.id = f"evt-{self._counter}"
        
        # Store in Redis if available
        if self.redis_client:
            try:
                event_json = event.model_dump_json() if hasattr(event, 'model_dump_json') else json.dumps(event.dict())
                self.redis_client.lpush("agent_events", event_json)
                self.redis_client.ltrim("agent_events", 0, 999) # Keep last 1000
            except Exception as e:
                logger.error(f"EventBus: Redis push error: {e}")
        
        # Always keep in local buffer for fast access and fallback
        self._buffer.append(event)
        
        # Persist to PostgreSQL if db session is provided
        if db:
            try:
                record = AgentEventRecord(
                    id=event.id,
                    agent_id=event.agent_id,
                    workflow_name=event.workflow_name,
                    event_type=event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
                    description=event.description,
                    how=event.how,
                    why=event.why,
                    timestamp=event.timestamp,
                    data_json=event.data if isinstance(event.data, dict) else {},
                    progress=getattr(event, "progress", 0.0)
                )
                db.add(record)
                await db.commit()
            except Exception as e:
                logger.error(f"EventBus: DB save error: {e}")
                
        logger.debug(f"EventBus: Emitted {event.event_type} for {event.agent_id}")
        
        for subscriber in self._subscribers:
            try:
                if asyncio.iscoroutinefunction(subscriber):
                    await subscriber(event)
                else:
                    subscriber(event)
            except Exception as e:
                logger.error(f"EventBus: Subscriber error: {e}")

    async def get_events(self, db: Optional[AsyncSession] = None, since_id: Optional[str] = None, limit: int = 50) -> List[AgentEvent]:
        """Retrieve historical events from DB, Redis, or Memory buffer."""
        
        # Try DB first for complete history if session provided
        if db:
            try:
                stmt = select(AgentEventRecord).order_by(AgentEventRecord.timestamp.desc()).limit(limit)
                result = await db.execute(stmt)
                records = result.scalars().all()
                events = []
                for r in reversed(records):
                    events.append(AgentEvent(
                        id=r.id,
                        agent_id=r.agent_id,
                        workflow_name=r.workflow_name,
                        event_type=r.event_type,
                        description=r.description,
                        how=r.how,
                        why=r.why,
                        timestamp=r.timestamp,
                        data=r.data_json
                    ))
                return events
            except Exception as e:
                logger.warning(f"EventBus: DB retrieval error, falling back to Redis/Memory: {e}")

        # Try Redis next
        if self.redis_client:
            try:
                raw_events = self.redis_client.lrange("agent_events", 0, limit - 1)
                events = [AgentEvent.parse_raw(e) if hasattr(AgentEvent, 'parse_raw') else AgentEvent(**json.loads(e)) for e in raw_events]
                events.reverse()
                
                if since_id:
                    found_idx = -1
                    for i, e in enumerate(events):
                        if e.id == since_id:
                            found_idx = i
                            break
                    if found_idx != -1:
                        events = events[found_idx + 1:]
                return events
            except Exception as e:
                logger.warning(f"EventBus: Redis retrieval error, falling back to memory: {e}")

        # Fallback to in-memory buffer
        events_list = list(self._buffer)
        
        if since_id:
            found_idx = -1
            for i, e in enumerate(events_list):
                if e.id == since_id:
                    found_idx = i
                    break
            if found_idx != -1:
                events_list = events_list[found_idx + 1:]
        
        return events_list[-limit:] if limit > 0 else []

event_bus = EventBus()
