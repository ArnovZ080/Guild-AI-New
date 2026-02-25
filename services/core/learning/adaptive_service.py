"""
Adaptive Learning Service.
The central brain that combines user preferences and business outcomes
to provide intelligent context for the Orchestrator.
"""
import logging
from typing import Dict, Any, List, Optional
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
    def get_context_for_orchestrator(cls) -> str:
        """
        Generate a combined intelligence prompt for the Orchestrator.
        This is injected into every planning cycle.
        """
        sections = []

        # 1. User Preferences
        pref_prompt = PreferenceLearner.get_preferences_prompt()
        if pref_prompt:
            sections.append(pref_prompt)

        # 2. Business Optimizations
        opt_prompt = OutcomeTracker.get_optimization_prompt()
        if opt_prompt:
            sections.append(opt_prompt)

        if not sections:
            return ""

        return "\n\n".join(sections)

    # --- Scheduling Intelligence ---

    @classmethod
    def should_schedule(cls, event_type: str, day: str, time: str = None) -> Dict[str, Any]:
        """
        Check if scheduling is appropriate based on learned preferences.
        Returns a recommendation dict.
        """
        preferences = PreferenceLearner.get_active_preferences()
        
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
    def get_best_strategy(cls, action_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the best-performing strategy for a given action type
        based on historical outcomes.
        """
        pattern = OutcomeTracker.get_best_strategy(action_type)
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
    async def run_deep_analysis(cls) -> Dict[str, Any]:
        """
        Run LLM-powered deep analysis on both user preferences and outcomes.
        Should be triggered periodically (e.g., weekly).
        """
        new_preferences = await PreferenceLearner.extract_preferences_llm()
        new_patterns = await OutcomeTracker.analyze_patterns_llm()

        return {
            "new_preferences": len(new_preferences),
            "new_patterns": len(new_patterns),
            "preferences": [p.model_dump() for p in new_preferences],
            "patterns": [p.model_dump() for p in new_patterns]
        }

    # --- Dashboard Data ---

    @classmethod
    def get_dashboard_data(cls) -> Dict[str, Any]:
        """Get all learning data for the AdaptiveInsights dashboard."""
        return {
            "preferences": [p.model_dump() for p in PreferenceLearner.get_active_preferences()],
            "patterns": [p.model_dump() for p in OutcomeTracker.get_active_patterns()],
            "performance": OutcomeTracker.get_performance_summary(),
            "total_signals": len(PreferenceLearner._signals),
            "total_outcomes": len(OutcomeTracker._outcomes)
        }
