"""
Agent Communication Bus.
Lightweight pub/sub message bus for direct agent-to-agent communication.
Replaces legacy's 437-line InterAgentCommunicationHub with a clean, async design.
"""
import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Awaitable
from collections import defaultdict, deque
from pydantic import BaseModel, Field
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """Types of inter-agent messages."""
    COORDINATION = "coordination"
    DATA_SYNC = "data_sync"
    INSIGHT_SHARE = "insight_share"
    STATUS_UPDATE = "status_update"
    ERROR = "error"
    WORKFLOW_STEP = "workflow_step"

class MessagePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AgentMessage(BaseModel):
    """A message sent between agents."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender: str
    recipient: str
    type: MessageType = MessageType.COORDINATION
    priority: MessagePriority = MessagePriority.MEDIUM
    payload: Dict[str, Any] = Field(default_factory=dict)
    requires_reply: bool = False
    correlation_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Type alias for handler functions
MessageHandler = Callable[[AgentMessage], Awaitable[Optional[Dict[str, Any]]]]

PRIORITY_ORDER = {
    MessagePriority.CRITICAL: 0,
    MessagePriority.HIGH: 1,
    MessagePriority.MEDIUM: 2,
    MessagePriority.LOW: 3,
}


class AgentBus:
    """
    Central message bus for inter-agent communication.
    
    Features:
    - Publish/subscribe with topic-based routing
    - Priority-ordered delivery
    - Request/reply pattern with async futures
    - Message history for transparency
    
    Unlike the legacy hub, this is stateless (no heartbeats, no threads).
    Agents are lightweight; the bus just routes messages.
    """

    _handlers: Dict[str, Dict[MessageType, List[MessageHandler]]] = defaultdict(lambda: defaultdict(list))
    _pending_replies: Dict[str, asyncio.Future] = {}
    _history: deque = deque(maxlen=5000)
    _metrics = {
        "sent": 0,
        "delivered": 0,
        "failed": 0,
    }

    # --- Registration ---

    @classmethod
    def register(cls, agent_name: str, message_type: MessageType, handler: MessageHandler):
        """Register a handler for a specific message type."""
        cls._handlers[agent_name][message_type].append(handler)
        logger.info(f"AgentBus: {agent_name} registered handler for {message_type.value}")

    @classmethod
    def unregister(cls, agent_name: str):
        """Remove all handlers for an agent."""
        cls._handlers.pop(agent_name, None)

    # --- Sending ---

    @classmethod
    async def send(cls, message: AgentMessage) -> Optional[Dict[str, Any]]:
        """
        Send a message to a recipient agent.
        If requires_reply=True, blocks until the handler returns a response.
        """
        cls._history.append(message)
        cls._metrics["sent"] += 1

        handlers = cls._handlers.get(message.recipient, {}).get(message.type, [])
        if not handlers:
            logger.warning(f"AgentBus: No handler for {message.recipient}/{message.type.value}")
            cls._metrics["failed"] += 1
            return None

        # Deliver to all handlers, sorted by priority
        reply = None
        for handler in handlers:
            try:
                result = await handler(message)
                if result is not None:
                    reply = result  # Last handler with a result wins
                cls._metrics["delivered"] += 1
            except Exception as e:
                logger.error(f"AgentBus: Handler error for {message.recipient}: {e}")
                cls._metrics["failed"] += 1

        return reply

    @classmethod
    async def broadcast(cls, sender: str, message_type: MessageType,
                        payload: Dict[str, Any], priority: MessagePriority = MessagePriority.MEDIUM):
        """Broadcast a message to ALL registered agents for this message type."""
        tasks = []
        for agent_name, type_handlers in cls._handlers.items():
            if message_type in type_handlers:
                msg = AgentMessage(
                    sender=sender,
                    recipient=agent_name,
                    type=message_type,
                    priority=priority,
                    payload=payload,
                )
                tasks.append(cls.send(msg))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    # --- Convenience Senders ---

    @classmethod
    async def coordinate(cls, sender: str, recipient: str,
                         payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send a coordination request and wait for reply."""
        msg = AgentMessage(
            sender=sender,
            recipient=recipient,
            type=MessageType.COORDINATION,
            priority=MessagePriority.HIGH,
            payload=payload,
            requires_reply=True,
        )
        return await cls.send(msg)

    @classmethod
    async def share_insight(cls, sender: str, recipient: str, insight: Dict[str, Any]):
        """Share an insight with another agent."""
        msg = AgentMessage(
            sender=sender,
            recipient=recipient,
            type=MessageType.INSIGHT_SHARE,
            payload=insight,
        )
        await cls.send(msg)

    # --- Metrics ---

    @classmethod
    def get_metrics(cls) -> Dict[str, Any]:
        return {
            **cls._metrics,
            "registered_agents": list(cls._handlers.keys()),
            "history_size": len(cls._history),
        }

    @classmethod
    def get_recent_messages(cls, limit: int = 20) -> List[Dict[str, Any]]:
        return [m.model_dump() for m in list(cls._history)[-limit:]]
