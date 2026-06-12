"""Engagement ingestion: events in -> contacts, metrics, outcomes, goal progress out."""
import logging
import uuid
from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

from services.core.db.models import ContentItem, Contact, Goal
from services.core.crm.capture import LeadCaptureService
from services.core.learning.outcome_tracker import OutcomeTracker
from services.core.goals.engine import GoalsEngine
from services.core.ingestion.models import EngagementEvent

logger = logging.getLogger(__name__)
lead_capture = LeadCaptureService()
goals_engine = GoalsEngine()

_MAX_PROCESSED_IDS = 500


def _score_band(likes: int, comments: int) -> str:
    total = likes + comments * 3  # comments weigh more
    if total >= 30: return "excellent"
    if total >= 12: return "good"
    if total >= 3:  return "neutral"
    if total > 0:   return "poor"
    return "failed"


async def ingest_engagement(db: AsyncSession, user_id: str,
                            events: List[EngagementEvent]) -> dict:
    report = {"comments_processed": 0, "comments_skipped": 0,
              "items_updated": 0, "outcomes_recorded": 0, "goals_updated": 0}

    by_item: dict[str, list[EngagementEvent]] = {}
    for ev in events:
        by_item.setdefault(ev.content_item_id, []).append(ev)

    for item_id, item_events in by_item.items():
        result = await db.execute(select(ContentItem).where(ContentItem.id == item_id))
        item = result.scalars().first()
        if item is None:
            continue

        pm = dict(item.performance_metrics or {})
        processed: list = pm.get("processed_event_ids", [])
        counts_changed = False

        for ev in item_events:
            if ev.type == "comment":
                if ev.event_id in processed:
                    report["comments_skipped"] += 1
                    continue
                await lead_capture.process_engagement(db, user_id, ev.platform, {
                    "engaged_user": ev.engaged_user,
                    "content_item_id": item_id,
                    "type": "comment",
                    "engagement_text": ev.text,
                })
                processed.append(ev.event_id)
                report["comments_processed"] += 1

            elif ev.type == "reaction_summary":
                old = (pm.get("likes", 0), pm.get("comments", 0), pm.get("shares", 0))
                new = (ev.metrics.get("likes", 0), ev.metrics.get("comments", 0),
                       ev.metrics.get("shares", 0))
                if new != old:
                    counts_changed = True
                pm["likes"], pm["comments"], pm["shares"] = new
                pm["last_collected"] = ev.occurred_at or pm.get("last_collected", "")

        pm["processed_event_ids"] = processed[-_MAX_PROCESSED_IDS:]
        item.performance_metrics = pm
        flag_modified(item, "performance_metrics")
        report["items_updated"] += 1

        if counts_changed:
            await OutcomeTracker.record_outcome(
                db=db, user_id=user_id, task_id=str(uuid.uuid4()),
                agent_id="ingestion", action_type="content",
                platform=item.platform or "meta",
                params={"content_item_id": item.id, "content_type": item.content_type},
                score=_score_band(pm.get("likes", 0), pm.get("comments", 0)),
                metrics={"likes": float(pm.get("likes", 0)),
                         "comments": float(pm.get("comments", 0)),
                         "shares": float(pm.get("shares", 0))},
            )
            report["outcomes_recorded"] += 1

    await db.commit()

    # ── Goal auto-progress ────────────────────────────────────────────────
    result = await db.execute(select(Goal).where(
        Goal.user_id == user_id, Goal.status == "active"))
    for goal in result.scalars().all():
        metric = (goal.target_metric or "").lower()
        new_value = None
        if "lead" in metric or "contact" in metric:
            r = await db.execute(select(func.count(Contact.id)).where(
                Contact.user_id == user_id))
            new_value = float(r.scalar() or 0)
        elif "engagement" in metric:
            r = await db.execute(select(ContentItem.performance_metrics).where(
                ContentItem.user_id == user_id, ContentItem.status == "published"))
            total = 0
            for (m,) in r.all():
                m = m or {}
                total += int(m.get("likes", 0)) + int(m.get("comments", 0))
            new_value = float(total)
        if new_value is not None and new_value != goal.current_value:
            await goals_engine.track_progress(db, goal.id, new_value)
            report["goals_updated"] += 1

    logger.info("Ingestion for %s: %s", user_id, report)
    return report
