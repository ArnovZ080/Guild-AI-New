"""
WebSocket Real-Time Events

Streams agent activity, content notifications, lead captures, and
approval requests to connected frontend clients.
"""
import logging
import json
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from services.core.utils.event_bus import event_bus

logger = logging.getLogger(__name__)

router = APIRouter()

# Active connections per user
_connections: Dict[str, Set[WebSocket]] = {}


async def broadcast_to_user(user_id: str, event: dict):
    """Send an event to all WebSocket connections for a user."""
    if user_id not in _connections:
        return
    dead = set()
    for ws in _connections[user_id]:
        try:
            await ws.send_json(event)
        except Exception:
            dead.add(ws)
    _connections[user_id] -= dead


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    Real-time event stream for a user:
    - agent_activity: started/thinking/completed/failed
    - content_published: new content went live
    - lead_captured: new engagement-based lead
    - approval_request: content awaiting review
    - milestone_reached: goal milestone hit
    - nurture_event: sequence step executed
    """
    await websocket.accept()

    # Register connection
    if user_id not in _connections:
        _connections[user_id] = set()
    _connections[user_id].add(websocket)

    logger.info("WebSocket connected: user=%s (total=%d)", user_id, len(_connections[user_id]))

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "Real-time events active",
            "user_id": user_id,
        })

        # Keep alive and listen for client messages
        while True:
            data = await websocket.receive_text()
            # Client can send pings or request specific data
            try:
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except json.JSONDecodeError:
                pass

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected: user=%s", user_id)
    finally:
        _connections.get(user_id, set()).discard(websocket)
        if user_id in _connections and not _connections[user_id]:
            del _connections[user_id]


# ── Event Bus Integration ──
# Wire the existing event_bus to push through WebSocket

async def _on_agent_event(event):
    """Forward agent events to WebSocket clients."""
    if hasattr(event, "agent_id"):
        # Try to find user_id from event context
        user_id = getattr(event, "user_id", None)
        if user_id:
            await broadcast_to_user(user_id, {
                "type": "agent_activity",
                "agent_id": event.agent_id,
                "event_type": event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type),
                "description": event.description,
                "progress": getattr(event, "progress", 0),
            })


# Helper functions for specific event types
async def notify_content_published(user_id: str, content_item_id: str, platform: str):
    await broadcast_to_user(user_id, {
        "type": "content_published",
        "content_item_id": content_item_id,
        "platform": platform,
    })


async def notify_lead_captured(user_id: str, contact_id: str, icp_score: float):
    await broadcast_to_user(user_id, {
        "type": "lead_captured",
        "contact_id": contact_id,
        "icp_score": icp_score,
    })


async def notify_approval_needed(user_id: str, content_count: int):
    await broadcast_to_user(user_id, {
        "type": "approval_request",
        "pending_count": content_count,
    })


async def notify_milestone(user_id: str, goal_id: str, milestone_title: str):
    await broadcast_to_user(user_id, {
        "type": "milestone_reached",
        "goal_id": goal_id,
        "milestone": milestone_title,
    })
