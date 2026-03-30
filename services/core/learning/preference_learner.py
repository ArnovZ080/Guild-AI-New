import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.core.db.base import AsyncSessionLocal
from services.core.db.models import AdaptiveLearningSignal
from services.core.db.models import UserPreference as DBUserPreference
from .models import UserPreference as PydanticUserPreference
from .models import PreferenceCategory, PreferenceConfidence
from services.core.llm import default_llm
import json

logger = logging.getLogger(__name__)

class PreferenceLearner:
    """
    Observes user actions and extracts behavioral preferences.
    Uses signal accumulation + LLM pattern recognition.
    """

    # --- Signal Recording ---

    @classmethod
    async def record_signal(cls, db: Optional[AsyncSession], user_id: str, signal_type: str, data: Dict[str, Any]):
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            signal = AdaptiveLearningSignal(
                id=str(uuid.uuid4()),
                user_id=user_id,
                pattern=signal_type,
                source=json.dumps(data),
                created_at=datetime.utcnow()
            )
            db.add(signal)
            await db.commit()
            
            logger.info(f"PreferenceLearner: Recorded signal [{signal_type}] for user {user_id}")

            # Auto-derive if enough signals of this type accumulate
            stmt = select(AdaptiveLearningSignal).where(
                AdaptiveLearningSignal.user_id == user_id,
                AdaptiveLearningSignal.pattern == signal_type
            )
            result = await db.execute(stmt)
            type_signals = result.scalars().all()
            
            if len(type_signals) >= 3:
                # Convert signals back to dict list for derivation
                signals_dict = [
                    {"id": s.id, "type": s.pattern, "data": json.loads(s.source) if s.source else {}, "timestamp": s.created_at.isoformat() if s.created_at else ""}
                    for s in type_signals
                ]
                await cls._derive_preference_from_signals(db, user_id, signal_type, signals_dict)
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def _derive_preference_from_signals(cls, db: AsyncSession, user_id: str, signal_type: str, signals: List[Dict]):
        """Attempt to derive a preference from accumulated signals of the same type."""
        # Find common patterns in the data
        common_fields = {}
        for signal in signals:
            for key, value in signal["data"].items():
                if key not in common_fields:
                    common_fields[key] = {}
                str_value = str(value)
                common_fields[key][str_value] = common_fields[key].get(str_value, 0) + 1

        # Check for dominant values (>= 60% of signals)
        threshold = len(signals) * 0.6
        dominant_conditions = {}
        for field, values in common_fields.items():
            for value, count in values.items():
                if count >= threshold:
                    dominant_conditions[field] = value

        if dominant_conditions:
            rule_key = f"{signal_type}_{'_'.join(f'{k}_{v}' for k, v in dominant_conditions.items())}"
            
            stmt = select(DBUserPreference).where(
                DBUserPreference.user_id == user_id,
                DBUserPreference.rule_key == rule_key
            )
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if not existing:
                # Generate human-readable rule
                rule_text = cls._generate_rule_text(signal_type, dominant_conditions)
                category = cls._infer_category(signal_type)

                preference = DBUserPreference(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    category=category.value,
                    rule=rule_text,
                    rule_key=rule_key,
                    conditions=dominant_conditions,
                    confidence=PreferenceConfidence.SUGGESTED.value if len(signals) < 5 else PreferenceConfidence.LIKELY.value,
                    signal_count=len(signals),
                    source="observation",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(preference)
                logger.info(f"PreferenceLearner: Derived preference [{rule_text}] (confidence: {preference.confidence})")
            else:
                # Strengthen existing preference
                existing.signal_count = len(signals)
                existing.updated_at = datetime.utcnow()
                if existing.signal_count >= 5 and existing.confidence == PreferenceConfidence.SUGGESTED.value:
                    existing.confidence = PreferenceConfidence.LIKELY.value
            await db.commit()

    @classmethod
    def _generate_rule_text(cls, signal_type: str, conditions: Dict[str, str]) -> str:
        """Generate a human-readable rule from signal type and conditions."""
        templates = {
            "meeting_declined": "No meetings on {day}s",
            "task_moved": "Prefer {task} on {to_day}s",
            "report_requested": "Auto-generate {type} report on {day}s at {time}",
            "content_preferred": "Prefer {content_type} content on {platform}",
            "work_start": "Typical work start: {time}",
            "work_end": "Typical work end: {time}",
        }
        template = templates.get(signal_type, f"{signal_type}: {conditions}")
        try:
            return template.format(**conditions)
        except KeyError:
            return f"{signal_type}: {json.dumps(conditions)}"

    @classmethod
    def _infer_category(cls, signal_type: str) -> PreferenceCategory:
        """Infer the category from the signal type."""
        mapping = {
            "meeting_declined": PreferenceCategory.SCHEDULING,
            "meeting_accepted": PreferenceCategory.SCHEDULING,
            "task_moved": PreferenceCategory.SCHEDULING,
            "report_requested": PreferenceCategory.GENERAL,
            "content_preferred": PreferenceCategory.CONTENT,
            "email_preference": PreferenceCategory.COMMUNICATION,
            "finance_review": PreferenceCategory.FINANCE,
            "work_start": PreferenceCategory.SCHEDULING,
            "work_end": PreferenceCategory.SCHEDULING,
        }
        return mapping.get(signal_type, PreferenceCategory.GENERAL)

    # --- Preference Retrieval ---

    @classmethod
    async def get_active_preferences(cls, db: Optional[AsyncSession], user_id: str) -> List[PydanticUserPreference]:
        """Return all active (non-rejected) preferences."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(DBUserPreference).where(
                DBUserPreference.user_id == user_id,
                DBUserPreference.confidence != PreferenceConfidence.REJECTED.value
            )
            result = await db.execute(stmt)
            db_prefs = result.scalars().all()
            
            return [
                PydanticUserPreference(
                    id=p.id,
                    category=PreferenceCategory(p.category),
                    rule=p.rule,
                    rule_key=p.rule_key,
                    conditions=p.conditions,
                    confidence=PreferenceConfidence(p.confidence),
                    signal_count=p.signal_count,
                    source=p.source.value if hasattr(p.source, 'value') else p.source,
                    first_observed=p.created_at,
                    last_observed=p.updated_at
                ) for p in db_prefs
            ]
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def get_preferences_prompt(cls, db: Optional[AsyncSession], user_id: str) -> str:
        """Generate a context prompt for the Orchestrator with all learned preferences."""
        active = await cls.get_active_preferences(db, user_id)
        if not active:
            return ""

        lines = ["## Learned User Preferences (Adaptive Learning)"]
        for p in active:
            confidence_icon = {"suggested": "🔵", "likely": "🟡", "confirmed": "🟢"}.get(p.confidence.value, "⚪")
            lines.append(f"- {confidence_icon} **{p.rule}** (observed {p.signal_count}x, confidence: {p.confidence.value})")
        lines.append("\nRespect these preferences when planning. If a task conflicts with a CONFIRMED preference, warn the user.")
        return "\n".join(lines)

    # --- LLM-Powered Deep Analysis ---

    @classmethod
    async def extract_preferences_llm(cls, db: Optional[AsyncSession], user_id: str) -> List[PydanticUserPreference]:
        """Use LLM to analyze all signals and find deeper behavioral patterns."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(AdaptiveLearningSignal).where(AdaptiveLearningSignal.user_id == user_id).order_by(AdaptiveLearningSignal.created_at.desc()).limit(50)
            result = await db.execute(stmt)
            recent_db_signals = result.scalars().all()
            
            if len(recent_db_signals) < 5:
                return []

            recent_signals = [
                {"id": s.id, "type": s.pattern, "data": json.loads(s.source) if s.source else {}, "timestamp": s.created_at.isoformat() if s.created_at else ""}
                for s in recent_db_signals
            ]
            
            sys_prompt = """You are a behavioral analyst. Analyze the following user activity signals and identify recurring patterns or preferences.
Return a JSON array of preferences, each with:
- "rule": A human-readable preference statement
- "rule_key": A machine-readable key (snake_case)
- "category": One of: scheduling, communication, finance, content, general
- "conditions": A dict of key-value pairs describing the pattern
- "confidence_score": 0.0-1.0 based on how strong the pattern is"""

            user_prompt = f"User Activity Signals:\n{json.dumps(recent_signals, indent=2)}"

            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ])

            try:
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                elif "[" in response:
                    start = response.index("[")
                    end = response.rindex("]") + 1
                    json_str = response[start:end]
                else:
                    return []

                patterns = json.loads(json_str)
                new_prefs = []
                for p in patterns:
                    rule_key = p["rule_key"]
                    stmt = select(DBUserPreference).where(
                        DBUserPreference.user_id == user_id,
                        DBUserPreference.rule_key == rule_key
                    )
                    res = await db.execute(stmt)
                    existing = res.scalar_one_or_none()
                    
                    if not existing:
                        pref = DBUserPreference(
                            id=str(uuid.uuid4()),
                            user_id=user_id,
                            category=p.get("category", "general"),
                            rule=p["rule"],
                            rule_key=rule_key,
                            conditions=p.get("conditions", {}),
                            confidence=PreferenceConfidence.LIKELY.value if p.get("confidence_score", 0) > 0.6 else PreferenceConfidence.SUGGESTED.value,
                            signal_count=len(recent_signals),
                            source="llm_analysis",
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        db.add(pref)
                        
                        p_pref = PydanticUserPreference(
                            id=pref.id,
                            category=PreferenceCategory(pref.category),
                            rule=pref.rule,
                            rule_key=pref.rule_key,
                            conditions=pref.conditions,
                            confidence=PreferenceConfidence(pref.confidence),
                            signal_count=pref.signal_count,
                            source=pref.source,
                            first_observed=pref.created_at,
                            last_observed=pref.updated_at
                        )
                        new_prefs.append(p_pref)
                await db.commit()
                return new_prefs
            except Exception as e:
                logger.error(f"LLM preference extraction failed: {e}")
                return []
        finally:
            if should_close:
                await db.close()

    # --- User Feedback ---

    @classmethod
    async def confirm_preference(cls, db: Optional[AsyncSession], user_id: str, rule_key: str) -> bool:
        """User confirms a learned preference."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(DBUserPreference).where(
                DBUserPreference.user_id == user_id,
                DBUserPreference.rule_key == rule_key
            )
            res = await db.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                existing.confidence = PreferenceConfidence.CONFIRMED.value
                existing.updated_at = datetime.utcnow()
                await db.commit()
                return True
            return False
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def reject_preference(cls, db: Optional[AsyncSession], user_id: str, rule_key: str) -> bool:
        """User rejects a suggested preference."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(DBUserPreference).where(
                DBUserPreference.user_id == user_id,
                DBUserPreference.rule_key == rule_key
            )
            res = await db.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                existing.confidence = PreferenceConfidence.REJECTED.value
                existing.updated_at = datetime.utcnow()
                await db.commit()
                return True
            return False
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def add_explicit_preference(cls, db: Optional[AsyncSession], user_id: str, rule: str, rule_key: str, category: str, conditions: Dict[str, Any]):
        """User explicitly adds a preference."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            pref = DBUserPreference(
                id=str(uuid.uuid4()),
                user_id=user_id,
                category=category,
                rule=rule,
                rule_key=rule_key,
                conditions=conditions,
                confidence=PreferenceConfidence.CONFIRMED.value,
                source="explicit",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(pref)
            await db.commit()
            logger.info(f"PreferenceLearner: Explicit preference added [{rule}]")
        finally:
            if should_close:
                await db.close()
