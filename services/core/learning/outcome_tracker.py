"""
Outcome Tracker Service.
Records the result of every AI-initiated action and derives optimization patterns.
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import defaultdict
from .models import ActionOutcome, LearnedPattern, OutcomeScore
from services.core.llm import default_llm
import json

logger = logging.getLogger(__name__)

class OutcomeTracker:
    """
    Tracks the results of AI actions and uses pattern analysis
    to discover what works and what doesn't.
    """

    _outcomes: List[ActionOutcome] = []
    _patterns: Dict[str, LearnedPattern] = {}

    # --- Outcome Recording ---

    @classmethod
    def record_outcome(
        cls,
        task_id: str,
        agent_id: str,
        action_type: str,
        platform: str,
        params: Dict[str, Any],
        score: str,
        metrics: Dict[str, float] = None,
        context: Dict[str, Any] = None
    ):
        """
        Record the outcome of an AI action.
        Examples:
          - record_outcome("t1", "ContentAgent", "social_post", "linkedin",
                          {"topic": "AI"}, "excellent", {"engagement": 0.08, "clicks": 150},
                          {"day": "monday", "time": "10:00"})
        """
        outcome = ActionOutcome(
            id=str(uuid.uuid4()),
            task_id=task_id,
            agent_id=agent_id,
            action_type=action_type,
            platform=platform,
            params=params,
            score=OutcomeScore(score),
            metrics=metrics or {},
            context=context or {},
            timestamp=datetime.utcnow()
        )
        cls._outcomes.append(outcome)
        logger.info(f"OutcomeTracker: Recorded [{action_type}] on [{platform}] -> {score}")

        # Auto-analyze after accumulating enough outcomes
        if len(cls._outcomes) % 10 == 0:
            cls._auto_analyze()

    # --- Pattern Analysis ---

    @classmethod
    def _auto_analyze(cls):
        """Run automatic pattern analysis on accumulated outcomes."""
        # Group by action_type + platform
        groups = defaultdict(list)
        for outcome in cls._outcomes:
            key = f"{outcome.action_type}_{outcome.platform}"
            groups[key].append(outcome)

        for group_key, outcomes in groups.items():
            if len(outcomes) < 5:
                continue

            # Score map for numerical comparison
            score_map = {"excellent": 5, "good": 4, "neutral": 3, "poor": 2, "failed": 1}
            
            # Find contextual patterns (e.g., time of day, day of week)
            context_performance = defaultdict(lambda: {"scores": [], "count": 0})
            
            for o in outcomes:
                for ctx_key, ctx_value in o.context.items():
                    ctx_group = f"{ctx_key}={ctx_value}"
                    context_performance[ctx_group]["scores"].append(score_map.get(o.score, 3))
                    context_performance[ctx_group]["count"] += 1

            # Find best-performing contexts
            for ctx_group, data in context_performance.items():
                if data["count"] >= 3:
                    avg_score = sum(data["scores"]) / len(data["scores"])
                    if avg_score >= 4.0:  # Good or better
                        pattern_key = f"{group_key}_{ctx_group}"
                        if pattern_key not in cls._patterns:
                            cls._patterns[pattern_key] = LearnedPattern(
                                id=str(uuid.uuid4()),
                                category=group_key,
                                insight=f"{group_key} performs best when {ctx_group} (avg score: {avg_score:.1f}/5)",
                                recommendation=f"Optimize {group_key}: prefer {ctx_group}",
                                supporting_data={"avg_score": avg_score, "sample_size": data["count"]},
                                confidence_score=min(data["count"] / 10, 1.0),
                                sample_size=data["count"]
                            )
                            logger.info(f"OutcomeTracker: New pattern [{cls._patterns[pattern_key].insight}]")

    @classmethod
    def get_active_patterns(cls) -> List[LearnedPattern]:
        """Return all active optimization patterns."""
        return [p for p in cls._patterns.values() if p.active]

    @classmethod
    def get_optimization_prompt(cls) -> str:
        """Generate a context prompt for the Orchestrator with optimization insights."""
        active = cls.get_active_patterns()
        if not active:
            return ""

        lines = ["## Business Optimization Insights (Learned from Outcomes)"]
        for p in sorted(active, key=lambda x: x.confidence_score, reverse=True):
            confidence_pct = int(p.confidence_score * 100)
            lines.append(f"- 📊 **{p.insight}** → _{p.recommendation}_ ({confidence_pct}% confidence, {p.sample_size} samples)")
        lines.append("\nApply these optimizations when planning actions. Prefer strategies with higher confidence scores.")
        return "\n".join(lines)

    # --- LLM-Powered Deep Analysis ---

    @classmethod
    async def analyze_patterns_llm(cls) -> List[LearnedPattern]:
        """Use LLM to discover deeper cause-effect patterns."""
        if len(cls._outcomes) < 10:
            return []

        recent = cls._outcomes[-100:]
        outcomes_data = [
            {
                "action": o.action_type,
                "platform": o.platform,
                "score": o.score,
                "metrics": o.metrics,
                "context": o.context,
                "timestamp": o.timestamp.isoformat()
            }
            for o in recent
        ]

        sys_prompt = """You are a business optimization analyst. Analyze the following action outcomes and identify patterns that correlate with success or failure.
Return a JSON array of insights, each with:
- "category": The action/platform group
- "insight": A human-readable finding
- "recommendation": An actionable optimization
- "confidence_score": 0.0-1.0
- "supporting_data": Key metrics that support this finding"""

        user_prompt = f"Action Outcomes:\n{json.dumps(outcomes_data, indent=2)}"

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
            new_patterns = []
            for p in patterns:
                pattern = LearnedPattern(
                    id=str(uuid.uuid4()),
                    category=p.get("category", "general"),
                    insight=p["insight"],
                    recommendation=p["recommendation"],
                    supporting_data=p.get("supporting_data", {}),
                    confidence_score=p.get("confidence_score", 0.5),
                    sample_size=len(recent)
                )
                pattern_key = f"llm_{pattern.category}_{pattern.id[:8]}"
                if pattern_key not in cls._patterns:
                    cls._patterns[pattern_key] = pattern
                    new_patterns.append(pattern)
            return new_patterns
        except Exception as e:
            logger.error(f"LLM pattern analysis failed: {e}")
            return []

    # --- Querying ---

    @classmethod
    def get_best_strategy(cls, action_type: str) -> Optional[LearnedPattern]:
        """Get the highest-confidence optimization for a given action type."""
        relevant = [p for p in cls._patterns.values() if action_type in p.category and p.active]
        if not relevant:
            return None
        return max(relevant, key=lambda p: p.confidence_score)

    @classmethod
    def get_performance_summary(cls, action_type: str = None) -> Dict[str, Any]:
        """Get a summary of action performance."""
        outcomes = cls._outcomes
        if action_type:
            outcomes = [o for o in outcomes if o.action_type == action_type]

        if not outcomes:
            return {"total_actions": 0}

        score_map = {"excellent": 5, "good": 4, "neutral": 3, "poor": 2, "failed": 1}
        scores = [score_map.get(o.score, 3) for o in outcomes]

        return {
            "total_actions": len(outcomes),
            "avg_score": sum(scores) / len(scores),
            "excellent_rate": len([s for s in scores if s == 5]) / len(scores),
            "failure_rate": len([s for s in scores if s == 1]) / len(scores),
            "top_platform": max(set(o.platform for o in outcomes), key=lambda p: len([o for o in outcomes if o.platform == p])),
        }
