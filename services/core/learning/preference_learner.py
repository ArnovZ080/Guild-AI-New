"""
Preference Learner Service.
Observes user behavior signals and derives preference rules using LLM analysis.
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from .models import UserPreference, PreferenceCategory, PreferenceConfidence
from services.core.llm import default_llm
import json

logger = logging.getLogger(__name__)

class PreferenceLearner:
    """
    Observes user actions and extracts behavioral preferences.
    Uses signal accumulation + LLM pattern recognition.
    """

    _signals: List[Dict[str, Any]] = []
    _preferences: Dict[str, UserPreference] = {}

    # --- Signal Recording ---

    @classmethod
    def record_signal(cls, signal_type: str, data: Dict[str, Any]):
        """
        Record a user behavior signal.
        Examples:
          - record_signal("meeting_declined", {"day": "tuesday", "time": "14:00"})
          - record_signal("task_moved", {"task": "finance_review", "to_day": "monday"})
          - record_signal("report_requested", {"type": "weekly", "day": "friday", "time": "09:00"})
        """
        signal = {
            "id": str(uuid.uuid4()),
            "type": signal_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        cls._signals.append(signal)
        logger.info(f"PreferenceLearner: Recorded signal [{signal_type}]")

        # Auto-derive if enough signals of this type accumulate
        type_signals = [s for s in cls._signals if s["type"] == signal_type]
        if len(type_signals) >= 3:
            cls._derive_preference_from_signals(signal_type, type_signals)

    @classmethod
    def _derive_preference_from_signals(cls, signal_type: str, signals: List[Dict]):
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
            
            if rule_key not in cls._preferences:
                # Generate human-readable rule
                rule_text = cls._generate_rule_text(signal_type, dominant_conditions)
                category = cls._infer_category(signal_type)

                preference = UserPreference(
                    id=str(uuid.uuid4()),
                    category=category,
                    rule=rule_text,
                    rule_key=rule_key,
                    conditions=dominant_conditions,
                    confidence=PreferenceConfidence.SUGGESTED if len(signals) < 5 else PreferenceConfidence.LIKELY,
                    signal_count=len(signals),
                    source="observation"
                )
                cls._preferences[rule_key] = preference
                logger.info(f"PreferenceLearner: Derived preference [{rule_text}] (confidence: {preference.confidence})")
            else:
                # Strengthen existing preference
                existing = cls._preferences[rule_key]
                existing.signal_count = len(signals)
                existing.last_observed = datetime.utcnow()
                if existing.signal_count >= 5 and existing.confidence == PreferenceConfidence.SUGGESTED:
                    existing.confidence = PreferenceConfidence.LIKELY

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
    def get_active_preferences(cls) -> List[UserPreference]:
        """Return all active (non-rejected) preferences."""
        return [p for p in cls._preferences.values() if p.confidence != PreferenceConfidence.REJECTED]

    @classmethod
    def get_preferences_prompt(cls) -> str:
        """Generate a context prompt for the Orchestrator with all learned preferences."""
        active = cls.get_active_preferences()
        if not active:
            return ""

        lines = ["## Learned User Preferences (Adaptive Learning)"]
        for p in active:
            confidence_icon = {"suggested": "🔵", "likely": "🟡", "confirmed": "🟢"}.get(p.confidence, "⚪")
            lines.append(f"- {confidence_icon} **{p.rule}** (observed {p.signal_count}x, confidence: {p.confidence})")
        lines.append("\nRespect these preferences when planning. If a task conflicts with a CONFIRMED preference, warn the user.")
        return "\n".join(lines)

    # --- LLM-Powered Deep Analysis ---

    @classmethod
    async def extract_preferences_llm(cls) -> List[UserPreference]:
        """Use LLM to analyze all signals and find deeper behavioral patterns."""
        if len(cls._signals) < 5:
            return []

        recent_signals = cls._signals[-50:]  # Last 50 signals
        
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
                pref = UserPreference(
                    id=str(uuid.uuid4()),
                    category=PreferenceCategory(p.get("category", "general")),
                    rule=p["rule"],
                    rule_key=p["rule_key"],
                    conditions=p.get("conditions", {}),
                    confidence=PreferenceConfidence.LIKELY if p.get("confidence_score", 0) > 0.6 else PreferenceConfidence.SUGGESTED,
                    signal_count=len(recent_signals),
                    source="llm_analysis"
                )
                if pref.rule_key not in cls._preferences:
                    cls._preferences[pref.rule_key] = pref
                    new_prefs.append(pref)
            return new_prefs
        except Exception as e:
            logger.error(f"LLM preference extraction failed: {e}")
            return []

    # --- User Feedback ---

    @classmethod
    def confirm_preference(cls, rule_key: str) -> bool:
        """User confirms a learned preference."""
        if rule_key in cls._preferences:
            cls._preferences[rule_key].confidence = PreferenceConfidence.CONFIRMED
            return True
        return False

    @classmethod
    def reject_preference(cls, rule_key: str) -> bool:
        """User rejects a suggested preference."""
        if rule_key in cls._preferences:
            cls._preferences[rule_key].confidence = PreferenceConfidence.REJECTED
            return True
        return False

    @classmethod
    def add_explicit_preference(cls, rule: str, rule_key: str, category: str, conditions: Dict[str, Any]):
        """User explicitly adds a preference."""
        pref = UserPreference(
            id=str(uuid.uuid4()),
            category=PreferenceCategory(category),
            rule=rule,
            rule_key=rule_key,
            conditions=conditions,
            confidence=PreferenceConfidence.CONFIRMED,
            source="explicit"
        )
        cls._preferences[rule_key] = pref
        logger.info(f"PreferenceLearner: Explicit preference added [{rule}]")
