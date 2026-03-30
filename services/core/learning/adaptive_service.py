import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from services.core.db.base import AsyncSessionLocal
from services.core.db.models import AdaptiveLearningSignal, AIActionOutcome

from .preference_learner import PreferenceLearner
from .outcome_tracker import OutcomeTracker
from .models import UserPreference, LearnedPattern

logger = logging.getLogger(__name__)

class AdaptiveLearningService:
    """
    Central coordinator for the Adaptive Learning Engine.
    Combines user preferences with business outcome optimization.
    """

    # --- Context Generation ---

    @classmethod
    async def get_context_for_orchestrator(cls, db: Optional[AsyncSession], user_id: str) -> str:
        """
        Generate a combined intelligence prompt for the Orchestrator.
        This is injected into every planning cycle.
        """
        sections = []

        # 1. User Preferences
        pref_prompt = await PreferenceLearner.get_preferences_prompt(db, user_id)
        if pref_prompt:
            sections.append(pref_prompt)

        # 2. Business Optimizations
        opt_prompt = await OutcomeTracker.get_optimization_prompt(db, user_id)
        if opt_prompt:
            sections.append(opt_prompt)

        if not sections:
            return ""

        return "\n\n".join(sections)

    # --- Scheduling Intelligence ---

    @classmethod
    async def should_schedule(cls, db: Optional[AsyncSession], user_id: str, event_type: str, day: str, time: str = None) -> Dict[str, Any]:
        """
        Check if scheduling is appropriate based on learned preferences.
        Returns a recommendation dict.
        """
        preferences = await PreferenceLearner.get_active_preferences(db, user_id)
        
        conflicts = []
        for pref in preferences:
            conditions = pref.conditions
            # Check day-based conflicts
            if conditions.get("day", "").lower() == day.lower():
                if "no_" in pref.rule_key or "declined" in pref.rule_key:
                    conflicts.append(pref)
            # Check type-based conflicts
            if conditions.get("type", "").lower() == event_type.lower():
                if conditions.get("day", "").lower() == day.lower():
                    conflicts.append(pref)

        if conflicts:
            conflict_rules = [c.rule for c in conflicts]
            return {
                "recommended": False,
                "reason": f"Conflicts with learned preferences: {', '.join(conflict_rules)}",
                "conflicts": [c.model_dump() for c in conflicts],
                "suggestion": f"Consider rescheduling. The user prefers no {event_type}s on {day}s."
            }

        return {
            "recommended": True,
            "reason": "No conflicts with learned preferences.",
            "conflicts": []
        }

    # --- Strategy Intelligence ---

    @classmethod
    async def get_best_strategy(cls, db: Optional[AsyncSession], user_id: str, action_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the best-performing strategy for a given action type
        based on historical outcomes.
        """
        pattern = await OutcomeTracker.get_best_strategy(db, user_id, action_type)
        if pattern:
            return {
                "recommendation": pattern.recommendation,
                "insight": pattern.insight,
                "confidence": pattern.confidence_score,
                "sample_size": pattern.sample_size
            }
        return None

    # --- Deep Analysis (Periodic) ---

    @classmethod
    async def run_deep_analysis(cls, db: Optional[AsyncSession], user_id: str) -> Dict[str, Any]:
        """
        Run LLM-powered deep analysis on both user preferences and outcomes.
        Should be triggered periodically (e.g., weekly).
        """
        new_preferences = await PreferenceLearner.extract_preferences_llm(db, user_id)
        new_patterns = await OutcomeTracker.analyze_patterns_llm(db, user_id)

        return {
            "new_preferences": len(new_preferences),
            "new_patterns": len(new_patterns),
            "preferences": [p.model_dump() for p in new_preferences],
            "patterns": [p.model_dump() for p in new_patterns]
        }

    # --- Dashboard Data ---

    @classmethod
    async def get_dashboard_data(cls, db: Optional[AsyncSession], user_id: str) -> Dict[str, Any]:
        """Get all learning data for the AdaptiveInsights dashboard."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            active_prefs = await PreferenceLearner.get_active_preferences(db, user_id)
            active_patterns = await OutcomeTracker.get_active_patterns(db, user_id)
            perf_summary = await OutcomeTracker.get_performance_summary(db, user_id)
            
            # get totals
            stmt_s = select(AdaptiveLearningSignal).where(AdaptiveLearningSignal.user_id == user_id)
            res_s = await db.execute(stmt_s)
            total_signals = len(res_s.scalars().all())
            
            stmt_o = select(AIActionOutcome).where(AIActionOutcome.user_id == user_id)
            res_o = await db.execute(stmt_o)
            total_outcomes = len(res_o.scalars().all())

            return {
                "preferences": [p.model_dump() for p in active_prefs],
                "patterns": [p.model_dump() for p in active_patterns],
                "performance": perf_summary,
                "total_signals": total_signals,
                "total_outcomes": total_outcomes
            }
        finally:
            if should_close:
                await db.close()
