"""
Conversational Onboarding Route

Multi-turn chat that progressively builds the Business Identity.
Uses the orchestrator to generate natural questions and extract structured data.
"""
import logging
import json
from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
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
    history: Optional[List[Dict[str, str]]] = None   # [{"role": "user"|"assistant", "content": "..."}]


class OnboardingResponse(BaseModel):
    reply: str
    completion_percentage: float
    conversation_id: Optional[str] = None
    fields_updated: list = []


ONBOARDING_SYSTEM_PROMPT = """You are Guild's brand strategist conducting a warm induction interview with a new member. This is their first impression of Guild — make it feel like talking to a sharp, kind consultant who is genuinely curious about their business, never like filling in a form.

CONVERSATION RULES:
1. ONE question per message. Never stack questions.
2. Always briefly acknowledge or react to what they just said before moving on — reference specifics from their words.
3. Keep messages short: 2-4 sentences plus the question.
4. Warm, plain language. No marketing jargon (never say "ICP", say "your ideal customer"; never say "psychographics", say "what they care about").
5. Occasionally reflect back an insight they didn't state directly ("Sounds like word-of-mouth is carrying you further than your posts are — that's exactly what we can fix.").

WHAT YOU'RE BUILDING (their Business Identity):
- business_name, niche, industry
- target_audience + icp (who buys, what they care about, their pain points)
- brand_voice (how they want to sound), brand_visual (colors, fonts, style)
- brand_story, competitors, pricing_strategy, marketing_channels
- content_preferences, goals_3month, goals_12month, challenges

CURRENT IDENTITY STATE:
{identity_state}

KNOWLEDGE LEDGER (field statuses — known / coached / flagged):
{ledger_state}

WEBSITE STYLE SCAN:
{style_scan_state}

COACH MODE — applies to ANY question, whenever the user is unsure:
If the user says anything like "I don't know", "not sure", "never thought about it", or gives a vague non-answer, do NOT move on and do NOT re-ask the same question. Instead:
a) Normalize it in one sentence ("Most owners haven't put this into words — that's literally why Guild exists.")
b) Explain the concept in ONE plain sentence (what it is, why it matters for their marketing).
c) Ask a CONCRETE ANECDOTE question instead of the abstract one. Examples:
   - ideal customer → "Think of your favourite customer — the one you wish you had ten of. Who are they? What did they buy? What did they say about it?"
   - brand voice → "If your business were a person at a dinner party, how would they talk? Or: show me a message you've sent a customer that felt 'very you'."
   - competitors → "When someone doesn't buy from you, where do they go instead?"
   - goals → "Picture this time next year going brilliantly. What's different about your business?"
d) Assemble the field's value FROM their anecdotes, read it back to them, and ask if it rings true. Mark it "coached" in the ledger.
e) If after coaching they still don't know: reassure them ("No problem — once your content is live we'll SEE who actually engages, and figure this out from real data"), mark the field "flagged" with a short note, and move on. Never make them feel tested.

STYLE SCAN REVEAL:
If the style scan state above contains results and the ledger does not show "style_reveal_done", then in your NEXT message — before your question — casually reveal it: "By the way, while we've been talking I had a look at your website..." Summarize 2-3 concrete observations (colors, mood, typography feel) in plain words and ask if that feels right. Record their reaction into brand_visual. Include "style_reveal_done": {{"status": "known"}} in your ledger updates.

STRUCTURED OUTPUT — every message, use exactly this format:
```json
{{"extracted": {{"field_name": "value", ...}}, "ledger": {{"field_name": {{"status": "known|coached|flagged", "note": "optional short note"}}}}, "coach_mode": false, "progress_hint": "short label of what was just learned"}}
```
<your conversational reply>

- "extracted" and "ledger" may be empty objects if nothing was learned this turn.
- Set "coach_mode": true when your reply is coaching (the UI renders it differently).
- Choose the next question by importance: business basics → ideal customer → brand voice → goals → challenges → the rest. Skip anything already known.

COMPLETION:
When all essential fields are known/coached/flagged, do NOT ask more questions. Reply with warm closure, summarize the 3 most interesting things you learned about their business, mention any flagged fields you'll revisit together later, and include "onboarding_complete": true inside the JSON block."""


async def _run_style_scan(user_id: str, url: str):
    from services.core.db.base import AsyncSessionLocal
    from services.core.branding.extractor import WebsiteStyleExtractor
    try:
        guide = await WebsiteStyleExtractor().extract_style(url)
        async with AsyncSessionLocal() as db:
            await BusinessIdentityManager.create_or_update(db, user_id, {"brand_style_guide": guide})
    except Exception as e:
        logger.warning("Style scan failed for %s: %s", user_id, e)

def _style_scan_state(identity) -> str:
    if identity.brand_style_guide:
        return f"RESULTS READY:\n{identity.brand_style_guide[:1200]}"
    if identity.website_url:
        return "Scan in progress — results not ready yet. Do not mention the scan."
    return "No website provided."

@router.post("/chat", response_model=OnboardingResponse)
async def onboarding_chat(
    request: OnboardingMessage,
    background_tasks: BackgroundTasks,
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
    history = (request.history or [])[-16:]  # last 8 exchanges is plenty; caps token cost
    messages = (
        [{"role": "system", "content": ONBOARDING_SYSTEM_PROMPT.format(
            identity_state=identity_state,
            ledger_state=json.dumps(identity.knowledge_ledger or {}),
            style_scan_state=_style_scan_state(identity),
        )}]
        + history
        + [{"role": "user", "content": request.message}]
    )

    # Generate response
    response_text = await default_llm.chat_completion(
        messages=messages,
        temperature=0.7,
        tier=ModelTier.FLASH,
    )

    # Parse extracted data and conversational reply
    extracted, ledger_updates, coach_mode, onboarding_complete, reply = _parse_response(response_text)
    fields_updated = []

    # Update identity with extracted data
    if extracted:
        await BusinessIdentityManager.create_or_update(db, current_user.id, extracted)
        fields_updated = list(extracted.keys())

    # Merge ledger updates
    if ledger_updates:
        merged = dict(identity.knowledge_ledger or {})
        merged.update(ledger_updates)
        await BusinessIdentityManager.create_or_update(db, current_user.id, {"knowledge_ledger": merged})

    # Fire the style scan the moment a website_url is captured (non-blocking)
    if extracted.get("website_url") and not identity.brand_style_guide:
        background_tasks.add_task(_run_style_scan, current_user.id, extracted["website_url"])

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
        from services.core.agents.identity import _is_populated
        if _is_populated(val):
            filled.append(field)
        else:
            missing.append(field)

    from services.core.agents.identity import _compute_completion
    completion = _compute_completion(identity)

    # Automatically fix DB if it's out of sync
    if abs(identity.completion_percentage - completion) > 0.1:
        identity.completion_percentage = completion
        await db.commit()

    return {
        "completion_percentage": completion,
        "fields_filled": filled,
        "fields_missing": missing,
    }


@router.post("/update")
async def update_identity_manual(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    """Manually update identity from the UI flow."""
    # We save all data from the UI directly into the onboarding_answers JSONB column
    # And we also pull out top-level fields for the Orchestrator context
    flat_data = {
        "onboarding_answers": data,
        "business_name": data.get("business_name", ""),
        "niche": data.get("niche", ""),
        "industry": data.get("business_type", ""),
        "target_audience": data.get("icp_description", ""),
        "brand_voice": {
            "tone": data.get("brand_voice_tone", ""),
            "personality": data.get("brand_personality", ""),
            "values": data.get("brand_values", "")
        },
        "brand_visual": {
            "colors": data.get("brand_colors", ""),
            "fonts": data.get("brand_fonts", ""),
            "style": data.get("brand_style", "")
        },
        "brand_story": f"Positioning: {data.get('brand_positioning', '')}\nDifferentiation: {data.get('brand_differentiation', '')}",
        "goals_3month": data.get("priority_3months", ""),
        "goals_12month": data.get("vision_12months", ""),
        "challenges": [data.get("biggest_challenge", "")] if data.get("biggest_challenge") else [],
        "competitors": data.get("competitors", []),
        "pricing_strategy": data.get("pricing_strategy", ""),
        "marketing_channels": data.get("marketing_channels", []),
        "content_preferences": data.get("content_preferences", {}),
        "icp": {
            "type": data.get("audience_type", ""),
            "problem": data.get("audience_problem", ""),
            "avatar": data.get("customer_avatar", "")
        }
    }
    
    identity = await BusinessIdentityManager.create_or_update(db, current_user.id, flat_data)
    
    
    # Update the user's name if provided
    if data.get("user_name"):
        current_user.name = data["user_name"]
        db.add(current_user)

    # Note: We rely on the core _compute_completion method to accurately calculate percentage instead of forcing it to 100.
    await db.commit()
    await db.refresh(identity)
    
    return {"completion_percentage": identity.completion_percentage}


_ESSENTIAL_FIELDS = [
    "business_name", "niche", "industry", "target_audience",
    "icp", "brand_voice", "brand_visual", "brand_story", "competitors",
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
            ledger = data.get("ledger", {})
            coach_mode = data.get("coach_mode", False)
            onboarding_complete = data.get("onboarding_complete", False)
            
            # Remove JSON block from reply
            reply = text[:json_match.start()] + text[json_match.end():]
            reply = reply.strip()
            return extracted, ledger, coach_mode, onboarding_complete, reply
        except json.JSONDecodeError:
            pass

    return {}, {}, False, False, text.strip()

@router.post("/finale")
async def onboarding_finale(
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    """Generate one real, Judge-scored sample post from the fresh identity."""
    from services.core.content_pipeline.engine import content_generator
    identity = await BusinessIdentityManager.get(db, current_user.id)
    topic = f"An introduction post that captures what makes {identity.business_name or 'this business'} special"
    try:
        item = await content_generator.generate_single_content(
            db, current_user.id, content_type="social", platform="instagram", topic=topic)
        return {"status": "ok", "content_item_id": item.id, "title": item.title,
                "body": item.body, "judge_score": (item.performance_metrics or {}).get("judge_score")}
    except Exception as e:
        logger.error("Onboarding finale generation failed: %s", e)
        return {"status": "skipped"}  # never block completion on this
