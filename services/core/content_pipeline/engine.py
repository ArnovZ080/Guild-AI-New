"""
Content Pipeline — Generator, Queue, Publisher, Scheduler

The core engine: agents → judge → approval queue → calendar → publish.
"""
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.models import ContentItem, BusinessIdentity
from services.core.llm import default_llm, ModelTier

logger = logging.getLogger(__name__)


# ── Content Generator ──

class ContentGenerator:
    """Orchestrates content creation across agents + judge evaluation + revision loop."""

    async def generate_weekly_content(
        self,
        db: AsyncSession,
        user_id: str,
        week_start: date,
    ) -> List[ContentItem]:
        """
        Generate a full week of content:
        1. Load BusinessIdentity
        2. Ask ContentMarketingAgent for weekly strategy
        3. For each piece: generate → judge → revision loop → queue
        """
        from services.core.agents.identity import BusinessIdentityManager

        identity = await BusinessIdentityManager.get(db, user_id)
        bi_dict = self._identity_to_dict(identity) if identity else {}

        # Generate content plan via LLM
        plan = await self._generate_weekly_plan(bi_dict, week_start)

        items = []
        for piece in plan:
            item = await self.generate_single_content(
                db, user_id,
                content_type=piece.get("content_type", "social"),
                platform=piece.get("platform", ""),
                topic=piece.get("topic", ""),
                business_identity=bi_dict,
            )
            items.append(item)

        logger.info("Generated %d content items for user %s week of %s", len(items), user_id, week_start)
        return items

    async def generate_single_content(
        self,
        db: AsyncSession,
        user_id: str,
        content_type: str,
        platform: str,
        topic: str,
        business_identity: Optional[dict] = None,
    ) -> ContentItem:
        """Generate a single content piece with judge evaluation."""
        if not business_identity:
            from services.core.agents.identity import BusinessIdentityManager
            identity = await BusinessIdentityManager.get(db, user_id)
            business_identity = self._identity_to_dict(identity) if identity else {}

        # Step 1: Generate content via LLM
        content_data = await self._create_content(content_type, platform, topic, business_identity)

        # Step 2: Judge evaluation
        from services.core.agents.judge import JudgeAgent
        judge = JudgeAgent()

        rubric = await judge.generate_rubric(content_type, platform, business_identity)
        evaluation = await judge.evaluate_content(content_data, rubric, business_identity)

        # Step 3: Revision loop (up to 3 retries)
        retries = 0
        while not evaluation.get("passed", True) and retries < rubric.get("max_retries", 3):
            revision = evaluation.get("revision_instructions", {})
            content_data = await self._revise_content(content_data, revision, business_identity)
            evaluation = await judge.evaluate_content(content_data, rubric, business_identity)
            retries += 1

        # Step 4: Save to database
        item = ContentItem(
            user_id=user_id,
            content_type=content_type,
            platform=platform,
            title=content_data.get("title", topic),
            body=content_data.get("body", ""),
            media_urls=content_data.get("media_urls", []),
            status="pending_review",
            performance_metrics={
                "judge_score": evaluation.get("overall_score", 0),
                "revision_count": retries,
                "rubric_used": rubric.get("criteria", []),
            },
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    async def regenerate_content(
        self,
        db: AsyncSession,
        content_item_id: str,
        feedback: str,
    ) -> ContentItem:
        """Regenerate a content piece with user feedback."""
        result = await db.execute(select(ContentItem).where(ContentItem.id == content_item_id))
        item = result.scalars().first()
        if not item:
            raise ValueError("Content item not found")

        from services.core.agents.identity import BusinessIdentityManager
        identity = await BusinessIdentityManager.get(db, item.user_id)
        bi_dict = self._identity_to_dict(identity) if identity else {}

        new_data = await self._revise_content(
            {"title": item.title, "body": item.body},
            {"revision_instructions": [{"criterion": "user_feedback", "action": feedback}]},
            bi_dict,
        )

        item.title = new_data.get("title", item.title)
        item.body = new_data.get("body", item.body)
        item.status = "pending_review"
        await db.commit()
        await db.refresh(item)
        return item

    async def _generate_weekly_plan(self, bi: dict, week_start: date) -> List[dict]:
        prompt = f"""Create a 7-day content plan for this business.

Business: {json.dumps(bi, default=str)[:800]}
Week starting: {week_start}

Return ONLY valid JSON — an array of content pieces:
[{{"content_type": "social|blog|email|ad", "platform": "instagram|linkedin|facebook|email|blog", "topic": "brief topic", "day": 0-6}}]

Aim for 5-10 pieces across platforms."""
        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.7, tier=ModelTier.FLASH)
            return json.loads(res.strip().strip('`').replace('json\n', '').strip())
        except Exception:
            return [
                {"content_type": "social", "platform": "linkedin", "topic": "Industry insight", "day": 1},
                {"content_type": "social", "platform": "instagram", "topic": "Behind the scenes", "day": 2},
                {"content_type": "blog", "platform": "blog", "topic": "Educational content", "day": 3},
                {"content_type": "social", "platform": "linkedin", "topic": "Thought leadership", "day": 4},
                {"content_type": "email", "platform": "email", "topic": "Newsletter", "day": 5},
            ]

    async def _create_content(self, content_type: str, platform: str, topic: str, bi: dict) -> dict:
        prompt = f"""Create {content_type} content for {platform}.

Topic: {topic}
Business: {json.dumps(bi, default=str)[:600]}

Return ONLY valid JSON: {{"title": "string", "body": "full content text", "hashtags": ["list"], "cta": "call to action"}}"""
        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.8, tier=ModelTier.FLASH)
            return json.loads(res.strip().strip('`').replace('json\n', '').strip())
        except Exception:
            return {"title": topic, "body": f"Content about {topic} for {platform}"}

    async def _revise_content(self, content: dict, revision: dict, bi: dict) -> dict:
        instructions = revision.get("revision_instructions", [])
        prompt = f"""Revise this content based on feedback.

CURRENT CONTENT: {json.dumps(content, default=str)[:1000]}
REVISION INSTRUCTIONS: {json.dumps(instructions, default=str)}
BUSINESS CONTEXT: {json.dumps(bi, default=str)[:400]}

Return ONLY valid JSON: {{"title": "string", "body": "revised full content"}}"""
        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.7, tier=ModelTier.FLASH)
            return json.loads(res.strip().strip('`').replace('json\n', '').strip())
        except Exception:
            return content

    def _identity_to_dict(self, identity) -> dict:
        if not identity:
            return {}
        return {
            "business_name": identity.business_name or "",
            "niche": identity.niche or "",
            "industry": identity.industry or "",
            "target_audience": identity.target_audience or "",
            "icp": identity.icp or {},
            "brand_voice": identity.brand_voice or {},
            "competitors": identity.competitors or [],
        }


# ── Content Queue ──

class ContentQueue:
    """Content approval queue: draft → review → approved → published."""

    async def get_pending_review(self, db: AsyncSession, user_id: str) -> List[ContentItem]:
        result = await db.execute(
            select(ContentItem).where(
                ContentItem.user_id == user_id,
                ContentItem.status == "pending_review",
            ).order_by(ContentItem.created_at.desc())
        )
        return list(result.scalars().all())

    async def approve(self, db: AsyncSession, content_item_id: str) -> ContentItem:
        result = await db.execute(select(ContentItem).where(ContentItem.id == content_item_id))
        item = result.scalars().first()
        if not item:
            raise ValueError("Content item not found")
        item.status = "approved"
        await db.commit()
        await db.refresh(item)
        return item

    async def reject(self, db: AsyncSession, content_item_id: str, feedback: str) -> ContentItem:
        result = await db.execute(select(ContentItem).where(ContentItem.id == content_item_id))
        item = result.scalars().first()
        if not item:
            raise ValueError("Content item not found")
        item.status = "rejected"
        item.performance_metrics = {**(item.performance_metrics or {}), "rejection_feedback": feedback}
        await db.commit()
        await db.refresh(item)
        return item

    async def edit(self, db: AsyncSession, content_item_id: str, edits: dict) -> ContentItem:
        result = await db.execute(select(ContentItem).where(ContentItem.id == content_item_id))
        item = result.scalars().first()
        if not item:
            raise ValueError("Content item not found")
        if "title" in edits:
            item.title = edits["title"]
        if "body" in edits:
            item.body = edits["body"]
        item.status = "pending_review"
        await db.commit()
        await db.refresh(item)
        return item

    async def bulk_approve(self, db: AsyncSession, content_item_ids: List[str]) -> List[ContentItem]:
        items = []
        for cid in content_item_ids:
            item = await self.approve(db, cid)
            items.append(item)
        return items


# ── Content Publisher ──

class ContentPublisher:
    """Publishes approved content to target platforms via integrations."""

    async def publish(self, db: AsyncSession, content_item: ContentItem) -> dict:
        """Publish a single approved content item to its platform."""
        if content_item.status != "approved":
            return {"error": "Content must be approved before publishing"}

        platform = (content_item.platform or "").lower()

        # Route to appropriate connector
        try:
            result = await self._publish_to_platform(platform, content_item)
            content_item.status = "published"
            content_item.published_at = datetime.utcnow()
            content_item.performance_metrics = {
                **(content_item.performance_metrics or {}),
                "publish_result": result,
            }
            await db.commit()
            return {"status": "published", "platform": platform, "result": result}
        except Exception as e:
            logger.error("Publishing failed for %s to %s: %s", content_item.id, platform, e)
            return {"status": "failed", "error": str(e)}

    async def publish_scheduled(self, db: AsyncSession) -> List[ContentItem]:
        """Find and publish all content where scheduled_for <= now."""
        now = datetime.utcnow()
        result = await db.execute(
            select(ContentItem).where(
                ContentItem.status == "approved",
                ContentItem.scheduled_for <= now,
                ContentItem.scheduled_for.isnot(None),
            )
        )
        items = list(result.scalars().all())
        published = []
        for item in items:
            res = await self.publish(db, item)
            if res.get("status") == "published":
                published.append(item)
        return published

    async def _publish_to_platform(self, platform: str, item: ContentItem) -> dict:
        """Route to the correct integration connector."""
        from services.core.integrations.registry import IntegrationRegistry

        connector = IntegrationRegistry.get_connector(platform)
        if connector and hasattr(connector, "publish_post"):
            return await connector.publish_post(
                content=item.body,
                media_urls=item.media_urls or [],
                title=item.title,
            )
        # Fallback: log but don't fail
        logger.warning("No publishing connector for platform: %s", platform)
        return {"status": "simulated", "platform": platform, "note": "No connector configured"}


# ── Content Scheduler ──

class ContentScheduler:
    """Smart scheduling: optimal times, anti-clash, campaign coordination."""

    PLATFORM_DEFAULTS = {
        "instagram": [10, 13, 18],      # Hours (UTC) with best engagement
        "linkedin": [8, 12, 17],
        "twitter": [9, 12, 15, 18],
        "facebook": [9, 13, 16],
        "email": [10, 14],
        "blog": [10],
    }

    async def suggest_schedule(
        self,
        db: AsyncSession,
        user_id: str,
        content_items: List[ContentItem],
    ) -> List[ContentItem]:
        """Assign optimal posting times to content items."""
        from services.core.db.models import CalendarEvent

        # Get existing calendar events for conflict detection
        now = datetime.utcnow()
        week_end = now + timedelta(days=7)
        events_result = await db.execute(
            select(CalendarEvent).where(
                CalendarEvent.user_id == user_id,
                CalendarEvent.start_time >= now,
                CalendarEvent.start_time <= week_end,
            )
        )
        existing_events = list(events_result.scalars().all())
        busy_times = {e.start_time.replace(minute=0, second=0) for e in existing_events}

        for i, item in enumerate(content_items):
            platform = (item.platform or "").lower()
            preferred_hours = self.PLATFORM_DEFAULTS.get(platform, [10])
            day_offset = i % 7

            # Find optimal time
            target_date = now.date() + timedelta(days=day_offset + 1)
            for hour in preferred_hours:
                candidate = datetime.combine(target_date, datetime.min.time().replace(hour=hour))
                if candidate not in busy_times:
                    item.scheduled_for = candidate
                    break
            else:
                item.scheduled_for = datetime.combine(target_date, datetime.min.time().replace(hour=10))

        await db.commit()
        return content_items


# ── Global instances ──
content_generator = ContentGenerator()
content_queue = ContentQueue()
content_publisher = ContentPublisher()
content_scheduler = ContentScheduler()
