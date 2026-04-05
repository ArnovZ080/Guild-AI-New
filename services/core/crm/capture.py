"""
Lead Capture Service

Processes engagement events from published content and automatically
creates/updates contacts in the CRM with ICP scoring.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.models import Contact, Interaction, ContentItem

logger = logging.getLogger(__name__)


class LeadCaptureService:
    """Captures leads from content engagement and routes to CRM."""

    async def process_engagement(
        self,
        db: AsyncSession,
        user_id: str,
        platform: str,
        engagement_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Process an engagement event from published content.

        Flow:
        1. Check if contact exists
        2. Create or update contact
        3. Score against ICP
        4. Flag for nurture if high score
        5. Log interaction
        """
        engaged_user = engagement_data.get("engaged_user", {})
        email = engaged_user.get("email")
        name = engaged_user.get("name")
        handle = engaged_user.get("handle", "")

        # Check existing
        contact = None
        if email:
            result = await db.execute(
                select(Contact).where(Contact.user_id == user_id, Contact.email == email))
            contact = result.scalars().first()

        if not contact and name:
            # Try by name + platform
            result = await db.execute(
                select(Contact).where(
                    Contact.user_id == user_id, Contact.name == name,
                    Contact.source_platform == platform))
            contact = result.scalars().first()

        is_new = contact is None

        if is_new:
            contact = Contact(
                user_id=user_id,
                name=name,
                email=email,
                source_platform=platform,
                source_content_id=engagement_data.get("content_item_id"),
                profile_data={
                    "handle": handle,
                    "profile_url": engaged_user.get("profile_url", ""),
                },
                engagement_level="warm",
                pipeline_stage="lead",
            )
            db.add(contact)
            await db.commit()
            await db.refresh(contact)

        # Log the interaction
        interaction = Interaction(
            contact_id=contact.id,
            type=engagement_data.get("type", "engagement"),
            channel=platform,
            content=engagement_data.get("engagement_text", ""),
            direction="inbound",
        )
        db.add(interaction)
        await db.commit()

        # Score against ICP
        from services.core.adk.customer.crm import CRMAgent
        crm = CRMAgent()
        scoring = await crm.score_lead(db, user_id, {"contact_id": contact.id})
        score = scoring.get("score", 50)

        # Determine actions
        actions_taken = ["interaction_logged"]
        if is_new:
            actions_taken.append("contact_created")

        if score >= 85:
            actions_taken.append("high_value_lead_flagged")
            contact.engagement_level = "hot"
            await db.commit()
        elif score >= 70:
            actions_taken.append("nurture_candidate")
            contact.engagement_level = "warm"
            await db.commit()

        return {
            "contact_id": contact.id,
            "is_new": is_new,
            "icp_score": score,
            "engagement_level": contact.engagement_level,
            "actions": actions_taken,
        }

    async def process_form_submission(
        self,
        db: AsyncSession,
        user_id: str,
        form_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Handle lead magnet downloads, newsletter signups, etc."""
        return await self.process_engagement(
            db, user_id,
            platform=form_data.get("source", "website"),
            engagement_data={
                "type": "form_submission",
                "engaged_user": {
                    "name": form_data.get("name"),
                    "email": form_data.get("email"),
                },
                "engagement_text": f"Form: {form_data.get('form_name', 'unknown')}",
                "content_item_id": form_data.get("content_item_id"),
            },
        )

    async def process_email_engagement(
        self,
        db: AsyncSession,
        user_id: str,
        email_event: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Handle email opens, clicks, replies from nurture sequences."""
        return await self.process_engagement(
            db, user_id,
            platform="email",
            engagement_data={
                "type": email_event.get("event_type", "email_open"),
                "engaged_user": {
                    "email": email_event.get("email"),
                    "name": email_event.get("name"),
                },
                "engagement_text": f"Email {email_event.get('event_type', 'event')}: {email_event.get('subject', '')}",
            },
        )


# Global
lead_capture = LeadCaptureService()
