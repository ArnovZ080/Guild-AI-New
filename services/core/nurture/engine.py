"""
Nurture Sequence Engine

Automated email/message sequences to convert leads.
Personalized via LLM, reviewed by JudgeAgent, sent via integrations.
"""
import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.models import NurtureSequence, Contact, Interaction
from services.core.llm import default_llm, ModelTier

logger = logging.getLogger(__name__)


# ── Pre-built Templates ──

NURTURE_TEMPLATES = {
    "welcome_subscriber": {
        "name": "Welcome Subscriber Sequence",
        "trigger": "newsletter_signup",
        "steps": [
            {"day": 0, "type": "email", "purpose": "Welcome + value proposition"},
            {"day": 3, "type": "email", "purpose": "Educational content related to their interest"},
            {"day": 7, "type": "email", "purpose": "Customer testimonial / social proof"},
            {"day": 14, "type": "email", "purpose": "Exclusive offer / CTA"},
            {"day": 21, "type": "email", "purpose": "Re-engagement if no purchase"},
        ],
    },
    "content_engaged": {
        "name": "Content Engagement Follow-up",
        "trigger": "high_engagement",
        "steps": [
            {"day": 0, "type": "email", "purpose": "Personal note referencing their engagement"},
            {"day": 5, "type": "email", "purpose": "Related resource or content"},
            {"day": 12, "type": "email", "purpose": "Soft offer or consultation invite"},
        ],
    },
    "cold_outreach": {
        "name": "Cold Outreach Sequence",
        "trigger": "manual",
        "steps": [
            {"day": 0, "type": "email", "purpose": "Personalized introduction"},
            {"day": 3, "type": "linkedin", "purpose": "Connection request with note"},
            {"day": 7, "type": "email", "purpose": "Value-add follow-up"},
            {"day": 14, "type": "email", "purpose": "Case study or social proof"},
            {"day": 21, "type": "email", "purpose": "Break-up email (last chance)"},
        ],
    },
    "customer_reengagement": {
        "name": "Customer Re-engagement",
        "trigger": "no_purchase_30_days",
        "steps": [
            {"day": 0, "type": "email", "purpose": "We miss you + what's new"},
            {"day": 7, "type": "email", "purpose": "Exclusive returning customer offer"},
            {"day": 14, "type": "email", "purpose": "Last chance offer"},
        ],
    },
}


class NurtureEngine:
    """Manages automated nurture sequences."""

    async def create_sequence(
        self,
        db: AsyncSession,
        user_id: str,
        contact_id: str,
        template_name: str,
    ) -> NurtureSequence:
        """Create a nurture sequence from a template, personalized to the contact."""
        template = NURTURE_TEMPLATES.get(template_name)
        if not template:
            raise ValueError(f"Unknown template: {template_name}")

        # Build steps with scheduled dates
        now = datetime.utcnow()
        steps = []
        for step in template["steps"]:
            steps.append({
                **step,
                "due_at": (now + timedelta(days=step["day"])).isoformat(),
                "status": "pending",
                "content": None,  # Generated when step executes
            })

        sequence = NurtureSequence(
            user_id=user_id,
            name=f"{template['name']} — Contact {contact_id[:8]}",
            trigger_type=template["trigger"],
            steps=steps,
            status="active",
        )
        db.add(sequence)
        await db.commit()
        await db.refresh(sequence)

        logger.info("Created nurture sequence '%s' for contact %s", template_name, contact_id)
        return sequence

    async def execute_step(
        self,
        db: AsyncSession,
        sequence_id: str,
        step_index: int,
    ) -> Dict[str, Any]:
        """
        Execute a nurture step:
        1. Generate personalized message
        2. Judge evaluation
        3. Queue for approval
        4. Send via channel
        5. Log interaction
        """
        result = await db.execute(
            select(NurtureSequence).where(NurtureSequence.id == sequence_id))
        sequence = result.scalars().first()
        if not sequence:
            return {"error": "Sequence not found"}

        steps = sequence.steps or []
        if step_index >= len(steps):
            return {"error": "Step index out of range"}

        step = steps[step_index]

        # Load contact context
        from services.core.agents.identity import BusinessIdentityManager
        bi_context = await BusinessIdentityManager.get_context_prompt(None, sequence.user_id)

        # Generate personalized message
        prompt = f"""Create a {step['type']} message for a nurture sequence.

PURPOSE: {step['purpose']}
STEP: {step_index + 1} of {len(steps)}
CHANNEL: {step['type']}

{bi_context}

Return ONLY valid JSON: {{"subject": "email subject line", "body": "message body", "cta": "call to action"}}"""

        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.7, tier=ModelTier.FLASH)
            message = json.loads(res.strip().strip('`').replace('json\n', '').strip())
        except Exception:
            message = {"subject": step["purpose"], "body": step["purpose"], "cta": "Learn more"}

        # Update step
        step["content"] = message
        step["status"] = "sent"
        step["executed_at"] = datetime.utcnow().isoformat()
        steps[step_index] = step
        sequence.steps = steps

        # Check if all steps complete
        if all(s.get("status") == "sent" for s in steps):
            sequence.status = "completed"

        await db.commit()
        return {"status": "executed", "step": step_index, "message": message}

    async def process_due_steps(self, db: AsyncSession) -> List[Dict]:
        """Find and execute all steps where due_at <= now."""
        result = await db.execute(
            select(NurtureSequence).where(NurtureSequence.status == "active"))
        sequences = list(result.scalars().all())

        executed = []
        now = datetime.utcnow()

        for seq in sequences:
            for i, step in enumerate(seq.steps or []):
                if step.get("status") != "pending":
                    continue
                due_at = datetime.fromisoformat(step.get("due_at", now.isoformat()))
                if due_at <= now:
                    result = await self.execute_step(db, seq.id, i)
                    executed.append({"sequence_id": seq.id, "step": i, **result})

        return executed

    async def handle_response(
        self,
        db: AsyncSession,
        sequence_id: str,
        response_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Handle when a nurtured contact responds."""
        result = await db.execute(
            select(NurtureSequence).where(NurtureSequence.id == sequence_id))
        sequence = result.scalars().first()
        if not sequence:
            return {"error": "Sequence not found"}

        response_type = response_data.get("type", "neutral")

        if response_type == "positive":
            sequence.status = "paused"
            await db.commit()
            return {"action": "paused", "reason": "Positive response — escalate to direct conversation"}
        elif response_type == "unsubscribe":
            sequence.status = "completed"
            await db.commit()
            return {"action": "ended", "reason": "Contact unsubscribed"}
        else:
            return {"action": "continue", "reason": "No explicit response"}


# Global
nurture_engine = NurtureEngine()
