"""
CalendarHarmonyAgent + Calendar Engine

Smart calendar: unified view, conflict detection, pattern learning,
optimal scheduling. The user's executive PA.
"""
import logging
import json
from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.db.models import CalendarEvent, CalendarPattern, ContentItem
from services.core.llm import default_llm, ModelTier

logger = logging.getLogger(__name__)


class CalendarHarmonyAgent(BaseAgent):
    """Executive PA — manages schedules, detects conflicts, learns patterns."""

    def __init__(self):
        super().__init__(AgentConfig(
            name="CalendarHarmonyAgent",
            description="Smart calendar management: scheduling, conflict detection, pattern learning",
        ))

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        action = input_data.get("action", "suggest_time") if isinstance(input_data, dict) else "suggest_time"
        db = context.get("db") if context else None
        user_id = input_data.get("user_id", "")

        handlers = {
            "suggest_time": self.suggest_time,
            "detect_conflicts": self.detect_conflicts,
            "learn_patterns": self.learn_patterns,
            "schedule_content": self.schedule_content,
            "daily_brief": self.get_daily_brief,
        }
        handler = handlers.get(action)
        if not handler:
            return {"error": f"Unknown action: {action}"}
        return await handler(db=db, user_id=user_id, data=input_data)

    async def suggest_time(self, db: AsyncSession, user_id: str, data: dict) -> dict:
        """Suggest optimal time slots based on patterns and availability."""
        event_type = data.get("event_type", "meeting")
        duration = data.get("duration_minutes", 60)

        # Get existing events for next 7 days
        now = datetime.utcnow()
        events = await self._get_events_range(db, user_id, now, now + timedelta(days=7))

        busy_hours = set()
        for e in events:
            hour = e.start_time.hour
            busy_hours.add((e.start_time.date(), hour))

        # Find open slots
        suggestions = []
        for day_offset in range(1, 8):
            target_date = (now + timedelta(days=day_offset)).date()
            for hour in [9, 10, 11, 14, 15, 16]:
                if (target_date, hour) not in busy_hours:
                    suggestions.append({
                        "date": target_date.isoformat(),
                        "time": f"{hour:02d}:00",
                        "duration_minutes": duration,
                        "confidence": 0.85,
                    })
                    if len(suggestions) >= 5:
                        break
            if len(suggestions) >= 5:
                break

        return {"suggestions": suggestions, "event_type": event_type}

    async def detect_conflicts(self, db: AsyncSession, user_id: str, data: dict) -> dict:
        """Check for conflicts with a proposed event."""
        start = datetime.fromisoformat(data.get("start_time", datetime.utcnow().isoformat()))
        end = start + timedelta(minutes=data.get("duration_minutes", 60))

        events = await self._get_events_range(db, user_id, start - timedelta(hours=1), end + timedelta(hours=1))

        conflicts = []
        for event in events:
            event_end = event.end_time or (event.start_time + timedelta(hours=1))
            if start < event_end and end > event.start_time:
                conflicts.append({
                    "event_id": event.id,
                    "title": event.title,
                    "start": event.start_time.isoformat(),
                })

        return {"has_conflicts": len(conflicts) > 0, "conflicts": conflicts}

    async def learn_patterns(self, db: AsyncSession, user_id: str, data: dict = None) -> dict:
        """Analyze calendar history to learn user patterns."""
        now = datetime.utcnow()
        events = await self._get_events_range(db, user_id, now - timedelta(days=90), now)

        if len(events) < 10:
            return {"patterns": [], "note": "Not enough data (need 10+ events)"}

        # Ask LLM to find patterns
        event_summary = [{"title": e.title, "day": e.start_time.strftime("%A"),
                          "hour": e.start_time.hour, "category": e.category}
                         for e in events[:50]]

        prompt = f"""Analyze these calendar events and identify recurring patterns.

Events: {json.dumps(event_summary)}

Return ONLY valid JSON:
[{{"pattern_type": "recurring|preference|blocker", "description": "pattern description", "confidence": 0.0-1.0}}]"""

        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.3, tier=ModelTier.FLASH)
            patterns = json.loads(res.strip().strip('`').replace('json\n', '').strip())

            # Store patterns
            for p in patterns:
                pattern = CalendarPattern(
                    user_id=user_id,
                    pattern_type=p.get("pattern_type", "preference"),
                    description=p.get("description", ""),
                    confidence=p.get("confidence", 0.5),
                )
                db.add(pattern)
            await db.commit()
            return {"patterns_found": len(patterns), "patterns": patterns}
        except Exception:
            return {"patterns": [], "note": "Pattern analysis failed"}

    async def schedule_content(self, db: AsyncSession, user_id: str, data: dict) -> dict:
        """Schedule approved content using the content scheduler."""
        from services.core.content_pipeline.engine import content_scheduler
        result = await db.execute(
            select(ContentItem).where(
                ContentItem.user_id == user_id, ContentItem.status == "approved",
                ContentItem.scheduled_for.is_(None)))
        items = list(result.scalars().all())
        if not items:
            return {"scheduled": 0}
        await content_scheduler.suggest_schedule(db, user_id, items)
        return {"scheduled": len(items)}

    async def get_daily_brief(self, db: AsyncSession, user_id: str, data: dict = None) -> dict:
        """Generate a morning brief: today's events, pending approvals, active sequences."""
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        events = await self._get_events_range(db, user_id, today_start, today_end)

        # Pending content
        from services.core.content_pipeline.engine import content_queue
        pending = await content_queue.get_pending_review(db, user_id)

        # Scheduled for today
        scheduled = await db.execute(
            select(ContentItem).where(
                ContentItem.user_id == user_id, ContentItem.status == "approved",
                ContentItem.scheduled_for >= today_start, ContentItem.scheduled_for <= today_end))

        return {
            "date": now.date().isoformat(),
            "events": [{"title": e.title, "time": e.start_time.strftime("%H:%M"), "category": e.category} for e in events],
            "pending_approvals": len(pending),
            "scheduled_posts": len(list(scheduled.scalars().all())),
        }

    async def _get_events_range(self, db, user_id, start, end):
        result = await db.execute(
            select(CalendarEvent).where(
                CalendarEvent.user_id == user_id,
                CalendarEvent.start_time >= start,
                CalendarEvent.start_time <= end,
            ).order_by(CalendarEvent.start_time))
        return list(result.scalars().all())


# Calendar Engine (pure service, no agent)
class CalendarEngine:
    """Calendar service layer for API routes."""

    async def get_unified_view(self, db: AsyncSession, user_id: str, start_date: datetime, end_date: datetime) -> dict:
        """All events in one view: calendar + content + workflows."""
        events = await db.execute(
            select(CalendarEvent).where(
                CalendarEvent.user_id == user_id,
                CalendarEvent.start_time >= start_date,
                CalendarEvent.start_time <= end_date))

        content = await db.execute(
            select(ContentItem).where(
                ContentItem.user_id == user_id,
                ContentItem.scheduled_for >= start_date,
                ContentItem.scheduled_for <= end_date))

        return {
            "events": [{"id": e.id, "title": e.title, "start": e.start_time.isoformat(),
                         "type": "calendar", "category": e.category}
                       for e in events.scalars().all()],
            "content": [{"id": c.id, "title": c.title, "start": c.scheduled_for.isoformat() if c.scheduled_for else None,
                          "type": "content", "platform": c.platform, "status": c.status}
                        for c in content.scalars().all()],
        }

    async def add_event(self, db: AsyncSession, user_id: str, event_data: dict) -> CalendarEvent:
        event = CalendarEvent(
            user_id=user_id,
            title=event_data.get("title", ""),
            start_time=datetime.fromisoformat(event_data["start_time"]),
            end_time=datetime.fromisoformat(event_data["end_time"]) if event_data.get("end_time") else None,
            category=event_data.get("category"),
            source_platform=event_data.get("source_platform", "guild"),
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event


# Register
AgentRegistry.register(
    AgentCapability(
        name="CalendarHarmonyAgent",
        category="productivity",
        capabilities=["suggest_time", "detect_conflicts", "learn_patterns", "schedule_content", "daily_brief"],
        description="Smart calendar management: scheduling, conflict detection, pattern learning",
    ),
    agent_class=CalendarHarmonyAgent,
)

calendar_engine = CalendarEngine()
