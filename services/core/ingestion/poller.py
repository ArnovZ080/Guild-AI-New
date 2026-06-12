"""Polls Meta for engagement on each connected user's recent posts."""
import logging
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.db.models import ConnectedIntegration, ContentItem
from services.core.integrations.connectors.meta import MetaConnector, NeedsReauth
from services.core.ingestion.service import ingest_engagement

logger = logging.getLogger(__name__)
LOOKBACK_DAYS = 7


async def poll_meta_for_user(db: AsyncSession, row: ConnectedIntegration) -> dict:
    try:
        connector = await MetaConnector.for_user(db, row.user_id)
    except NeedsReauth:
        logger.warning("Meta needs reauth for user %s — skipping", row.user_id)
        return {"status": "needs_reauth"}
    if connector is None:
        return {"status": "not_connected"}

    since = datetime.utcnow() - timedelta(days=LOOKBACK_DAYS)
    result = await db.execute(select(ContentItem).where(
        ContentItem.user_id == row.user_id,
        ContentItem.status == "published",
        ContentItem.platform.in_(["facebook", "instagram"]),
        ContentItem.published_at >= since,
    ))
    items = list(result.scalars().all())

    all_events = []
    for item in items:
        publish_result = (item.performance_metrics or {}).get("publish_result", {})
        post_id = publish_result.get("post_id")
        channel = publish_result.get("channel", item.platform)
        if not post_id:
            continue
        try:
            all_events.extend(
                await connector.fetch_engagement(post_id, channel, item.id))
        except Exception as e:
            logger.warning("fetch_engagement failed for %s: %s", post_id, e)

    report = await ingest_engagement(db, row.user_id, all_events)
    row.last_synced = datetime.utcnow()
    await db.commit()
    return {"status": "ok", **report}


async def poll_all_meta(db: AsyncSession) -> dict:
    result = await db.execute(select(ConnectedIntegration).where(
        ConnectedIntegration.platform == "meta",
        ConnectedIntegration.status == "connected",
    ))
    rows = list(result.scalars().all())
    summary = {"users": len(rows), "ok": 0, "errors": 0}
    for row in rows:
        try:
            await poll_meta_for_user(db, row)
            summary["ok"] += 1
        except Exception as e:           # one user never blocks the rest
            logger.error("poll failed for user %s: %s", row.user_id, e)
            summary["errors"] += 1
    return summary
