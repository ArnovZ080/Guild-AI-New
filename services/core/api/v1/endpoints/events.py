import asyncio
import json
from typing import Any
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from services.core.api import deps
from services.core.db.models import UserAccount, AgentEventRecord
from services.core.utils.event_bus import event_bus

router = APIRouter()

@router.get("/stream")
async def event_stream(
    request: Request,
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> StreamingResponse:
    """
    Server-Sent Events stream for the Agent Theater.
    Streams real-time agent events to the frontend.
    """
    async def generate():
        last_index = len(event_bus._buffer)
        while True:
            if await request.is_disconnected():
                break
            current_len = len(event_bus._buffer)
            if current_len > last_index:
                for i in range(last_index, current_len):
                    event = event_bus._buffer[i]
                    data = json.dumps(event.model_dump(), default=str)
                    yield f"data: {data}\n\n"
                last_index = current_len
            await asyncio.sleep(0.5)
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@router.get("/history")
async def event_history(
    limit: int = 50,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get recent events from the DB audit trail.
    """
    result = await db.execute(
        select(AgentEventRecord)
        .order_by(desc(AgentEventRecord.timestamp))
        .limit(limit)
    )
    events = result.scalars().all()
    return {
        "events": [
            {
                "id": e.id,
                "agent_id": e.agent_id,
                "event_type": e.event_type,
                "description": e.description,
                "how": e.how,
                "why": e.why,
                "timestamp": str(e.timestamp),
                "data": e.data_json,
                "progress": e.progress,
            }
            for e in events
        ]
    }
