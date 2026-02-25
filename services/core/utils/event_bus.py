from typing import List, Optional, Callable
from collections import deque
import threading
import json
import os
try:
    import redis
except ImportError:
    redis = None

from services.core.agents.models import AgentEvent
from services.core.logging import logger

class EventBus:
    """
    Singleton Event Bus for collecting real-time agent activity.
    Stores a rolling buffer of events in memory.
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
                    logger.warning(f"EventBus: Redis connection failed, falling back to memory: {e}")
                    self.redis_client = None
            
            self._initialized = True

    def _init(self):
        # This was called by __new__ but we move logic to __init__-like behavior
        pass

    def emit(self, event: AgentEvent):
        """Add an event to the buffer (Redis or Memory) and notify subscribers."""
        self._counter += 1
        # Assign a serial ID if not present
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
        logger.debug(f"EventBus: Emitted {event.event_type} for {event.agent_id}")
        
        for subscriber in self._subscribers:
            try:
                subscriber(event)
            except Exception as e:
                logger.error(f"EventBus: Subscriber error: {e}")

    def get_events(self, since_id: Optional[str] = None, limit: int = 50) -> List[AgentEvent]:
        """Retrieve historical events from Redis or Memory buffer."""
        
        # Try Redis first for durability
        if self.redis_client:
            try:
                # Get raw events from Redis
                raw_events = self.redis_client.lrange("agent_events", 0, limit - 1)
                events = [AgentEvent.parse_raw(e) if hasattr(AgentEvent, 'parse_raw') else AgentEvent(**json.loads(e)) for e in raw_events]
                events.reverse() # We pushed (lpush), so reverse to get chronological
                
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
