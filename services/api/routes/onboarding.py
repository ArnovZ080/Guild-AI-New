"""
Conversational Onboarding Route

Multi-turn chat that progressively builds the Business Identity.
Uses the orchestrator to generate natural questions and extract structured data.
"""
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.db.base import get_db
from services.core.db.models import UserAccount, BusinessIdentity
from services.core.agents.identity import BusinessIdentityManager
from services.core.llm import default_llm, ModelTier
from services.api.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


class OnboardingMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class OnboardingResponse(BaseModel):
    reply: str
    completion_percentage: float
    conversation_id: Optional[str] = None
    fields_updated: list = []


# System prompt for the onboarding conversation
ONBOARDING_SYSTEM_PROMPT = """You are a friendly, knowledgeable business consultant onboarding a new user to Guild AI — an AI growth engine for their business.

Your goal is to learn about their business through a warm, natural conversation. You should:
1. Ask ONE clear question at a time
2. Be conversational, not robotic — sound like a business advisor catching up over coffee
3. Help users who don't know their answers discover them
4. Extract structured data from their natural responses
5. Acknowledge what they've shared before asking the next question

You're building their Business Identity, which includes:
- Business name, niche, industry
- Target audience / Ideal Customer Profile (demographics, psychographics, pain points)
- Brand voice and tone (how they want to sound)
- Brand story / origin
- Competitors
- Pricing strategy
- Current marketing channels
- Content preferences (formats, topics, frequency)
- Business goals (3-month and 12-month)
- Key challenges

CURRENT IDENTITY STATE:
{identity_state}

INSTRUCTIONS:
- Look at what's already filled and what's missing
- Ask about the MOST IMPORTANT missing field next
- When the user responds, extract the structured data into a JSON block
- After extraction, formulate your conversational reply

Format your response as:
```json
{{"extracted": {{"field_name": "value", ...}}}}
```
<your conversational reply to the user>

If no data can be extracted from this message, just reply conversationally with no JSON block."""


@router.post("/chat", response_model=OnboardingResponse)
async def onboarding_chat(
    request: OnboardingMessage,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    """
    Process one turn of the onboarding conversation.
    Returns the assistant's reply plus updated completion percentage.
    """
    # Load current identity state
    identity = await BusinessIdentityManager.get(db, current_user.id)
    if not identity:
        identity = await BusinessIdentityManager.create_or_update(
            db, current_user.id, {"business_name": ""}
        )

    # Build identity state string for the prompt
    identity_state = _format_identity_state(identity)

    # Build messages
    messages = [
        {"role": "system", "content": ONBOARDING_SYSTEM_PROMPT.format(identity_state=identity_state)},
        {"role": "user", "content": request.message},
    ]

    # Generate response
    response_text = await default_llm.chat_completion(
        messages=messages,
        temperature=0.7,
        tier=ModelTier.FLASH,
    )

    # Parse extracted data and conversational reply
    extracted, reply = _parse_response(response_text)
    fields_updated = []

    # Update identity with extracted data
    if extracted:
        await BusinessIdentityManager.create_or_update(db, current_user.id, extracted)
        fields_updated = list(extracted.keys())

    # Reload for updated completion
    identity = await BusinessIdentityManager.get(db, current_user.id)

    return OnboardingResponse(
        reply=reply,
        completion_percentage=identity.completion_percentage if identity else 0.0,
        conversation_id=request.conversation_id,
        fields_updated=fields_updated,
    )


@router.get("/status")
async def onboarding_status(
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    """Get the current onboarding completion status."""
    identity = await BusinessIdentityManager.get(db, current_user.id)
    if not identity:
        return {"completion_percentage": 0.0, "fields_filled": [], "fields_missing": list(_ESSENTIAL_FIELDS)}

    filled = []
    missing = []
    for field in _ESSENTIAL_FIELDS:
        val = getattr(identity, field, None)
        if val and (not isinstance(val, (dict, list)) or len(val) > 0):
            filled.append(field)
        else:
            missing.append(field)

    return {
        "completion_percentage": identity.completion_percentage,
        "fields_filled": filled,
        "fields_missing": missing,
    }


_ESSENTIAL_FIELDS = [
    "business_name", "niche", "industry", "target_audience",
    "icp", "brand_voice", "brand_story", "competitors",
    "pricing_strategy", "marketing_channels", "content_preferences",
    "goals_3month", "goals_12month", "challenges",
]


def _format_identity_state(identity: BusinessIdentity) -> str:
    """Format the current identity state for the system prompt."""
    lines = []
    for field in _ESSENTIAL_FIELDS:
        val = getattr(identity, field, None)
        status = "✅ Filled" if val and (not isinstance(val, (dict, list)) or len(val) > 0) else "❌ Missing"
        display = str(val)[:100] + "..." if val and len(str(val)) > 100 else str(val) if val else "—"
        lines.append(f"- {field}: {status} → {display}")
    return "\n".join(lines)


def _parse_response(text: str) -> tuple:
    """Parse the LLM response to extract JSON data and conversational reply."""
    import json
    import re

    # Try to find JSON block
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            extracted = data.get("extracted", {})
            # Remove JSON block from reply
            reply = text[:json_match.start()] + text[json_match.end():]
            reply = reply.strip()
            return extracted, reply
        except json.JSONDecodeError:
            pass

    return {}, text.strip()
