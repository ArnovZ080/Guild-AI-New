"""
CRM Agent — Contact & Pipeline Management

Manages the built-in CRM: contacts, pipeline, interactions, ICP scoring.
Can sync with external CRMs (HubSpot, Pipedrive).
"""
import json
import logging
from typing import Any, Dict, Optional, List
from datetime import datetime

from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm, ModelTier

logger = logging.getLogger(__name__)


class CRMAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentConfig(
            name="CRMAgent",
            description="Contact management, pipeline tracking, ICP scoring, and external CRM sync",
        ))

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        action = input_data.get("action", "get_pipeline_summary") if isinstance(input_data, dict) else "get_pipeline_summary"
        db = context.get("db") if context else None
        user_id = input_data.get("user_id", context.get("user_id", "")) if isinstance(input_data, dict) else ""

        actions = {
            "add_contact": self.add_contact,
            "score_lead": self.score_lead,
            "move_stage": self.move_stage,
            "log_interaction": self.log_interaction,
            "get_pipeline_summary": self.get_pipeline_summary,
        }
        handler = actions.get(action)
        if not handler:
            return {"error": f"Unknown action: {action}"}
        return await handler(db=db, user_id=user_id, data=input_data)

    async def add_contact(self, db, user_id: str, data: dict) -> dict:
        """Add a new contact from engagement or manual entry."""
        from services.core.db.models import Contact
        contact = Contact(
            user_id=user_id,
            name=data.get("name"),
            email=data.get("email"),
            company=data.get("company"),
            source_platform=data.get("source_platform"),
            source_content_id=data.get("source_content_id"),
            profile_data=data.get("profile_data", {}),
        )
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return {"contact_id": contact.id, "status": "created"}

    async def score_lead(self, db, user_id: str, data: dict) -> dict:
        """Score a contact against the ICP."""
        from sqlalchemy import select
        from services.core.db.models import Contact, BusinessIdentity

        contact_id = data.get("contact_id")
        result = await db.execute(select(Contact).where(Contact.id == contact_id))
        contact = result.scalars().first()
        if not contact:
            return {"error": "Contact not found"}

        bi_result = await db.execute(
            select(BusinessIdentity).where(BusinessIdentity.user_id == user_id))
        bi = bi_result.scalars().first()
        icp = bi.icp if bi and bi.icp else {}

        prompt = f"""Score this lead against the Ideal Customer Profile on a scale of 0-100.

LEAD:
- Name: {contact.name}
- Company: {contact.company}
- Source: {contact.source_platform}
- Profile: {json.dumps(contact.profile_data, default=str)[:500]}

ICP: {json.dumps(icp, default=str)[:500]}

Return ONLY valid JSON: {{"score": 0-100, "reasoning": "string", "engagement_level": "cold|warm|hot"}}"""

        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.2, tier=ModelTier.FLASH)
            scoring = json.loads(res.strip().strip('`').replace('json\n', '').strip())

            contact.icp_score = scoring.get("score", 0) / 100.0
            contact.engagement_level = scoring.get("engagement_level", "cold")
            await db.commit()

            return {"contact_id": contact_id, **scoring}
        except Exception as e:
            logger.error("Lead scoring failed: %s", e)
            return {"contact_id": contact_id, "score": 50, "reasoning": "Scoring unavailable"}

    async def move_stage(self, db, user_id: str, data: dict) -> dict:
        """Move a contact through the pipeline."""
        from sqlalchemy import select
        from services.core.db.models import Contact

        contact_id = data.get("contact_id")
        new_stage = data.get("new_stage", "qualified")

        result = await db.execute(select(Contact).where(Contact.id == contact_id))
        contact = result.scalars().first()
        if not contact:
            return {"error": "Contact not found"}

        contact.pipeline_stage = new_stage
        contact.updated_at = datetime.utcnow()
        await db.commit()
        return {"contact_id": contact_id, "stage": new_stage}

    async def log_interaction(self, db, user_id: str, data: dict) -> dict:
        """Log an interaction with a contact."""
        from services.core.db.models import Interaction

        interaction = Interaction(
            contact_id=data.get("contact_id"),
            type=data.get("type", "note"),
            channel=data.get("channel"),
            content=data.get("content"),
            direction=data.get("direction", "outbound"),
        )
        db.add(interaction)
        await db.commit()
        return {"status": "logged"}

    async def get_pipeline_summary(self, db, user_id: str, data: dict = None) -> dict:
        """Return pipeline stats."""
        from sqlalchemy import select, func
        from services.core.db.models import Contact

        stages = ["lead", "qualified", "opportunity", "customer"]
        counts = {}
        for stage in stages:
            result = await db.execute(
                select(func.count(Contact.id)).where(
                    Contact.user_id == user_id, Contact.pipeline_stage == stage))
            counts[stage] = result.scalar() or 0

        total = sum(counts.values())
        return {"pipeline": counts, "total_contacts": total}


# Register
AgentRegistry.register(
    AgentCapability(
        name="CRMAgent",
        category="sales",
        capabilities=["add_contact", "score_lead", "move_stage", "log_interaction",
                       "get_pipeline_summary", "sync_external"],
        description="Contact management, pipeline tracking, ICP scoring",
    ),
    agent_class=CRMAgent,
)
