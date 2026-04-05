"""Calendar API Routes"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.db.base import get_db
from services.core.db.models import UserAccount
from services.api.middleware.auth import get_current_user
from services.core.calendar.engine import CalendarHarmonyAgent, calendar_engine

router = APIRouter()


class AddEventRequest(BaseModel):
    title: str
    start_time: str
    end_time: Optional[str] = None
    category: Optional[str] = None


class SuggestTimeRequest(BaseModel):
    event_type: str = "meeting"
    duration_minutes: int = 60


@router.get("/events")
async def get_events(
    start: Optional[str] = None, end: Optional[str] = None,
    db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user),
):
    start_dt = datetime.fromisoformat(start) if start else datetime.utcnow()
    end_dt = datetime.fromisoformat(end) if end else start_dt + timedelta(days=30)
    return await calendar_engine.get_unified_view(db, current_user.id, start_dt, end_dt)


@router.post("/events")
async def add_event(request: AddEventRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    event = await calendar_engine.add_event(db, current_user.id, request.model_dump())
    return {"id": event.id, "title": event.title, "start_time": event.start_time.isoformat()}


@router.get("/daily-brief")
async def daily_brief(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    agent = CalendarHarmonyAgent()
    return await agent.get_daily_brief(db=db, user_id=current_user.id)


@router.post("/sync")
async def sync_calendars(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    return {"status": "sync_initiated", "note": "Connect Google Calendar or Outlook in Settings"}


@router.post("/suggest-time")
async def suggest_time(request: SuggestTimeRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    agent = CalendarHarmonyAgent()
    return await agent.suggest_time(db=db, user_id=current_user.id, data=request.model_dump())
