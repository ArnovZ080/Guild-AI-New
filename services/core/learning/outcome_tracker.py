import logging
import uuid
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.core.db.base import AsyncSessionLocal
from services.core.db.models import AIActionOutcome as DBActionOutcome
from services.core.db.models import LearnedPattern as DBLearnedPattern
from .models import ActionOutcome as PydanticActionOutcome
from .models import LearnedPattern as PydanticLearnedPattern
from .models import OutcomeScore
from services.core.llm import default_llm

logger = logging.getLogger(__name__)

class OutcomeTracker:
    """
    Tracks the results of AI actions and uses pattern analysis
    to discover what works and what doesn't.
    """

    # --- Outcome Recording ---

    @classmethod
    async def record_outcome(
        cls,
        db: Optional[AsyncSession],
        user_id: str,
        task_id: str,
        agent_id: str,
        action_type: str,
        platform: str,
        params: Dict[str, Any],
        score: str,
        metrics: Dict[str, float] = None,
        context: Dict[str, Any] = None
    ):
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            db_outcome = DBActionOutcome(
                id=str(uuid.uuid4()),
                user_id=user_id,
                task_id=task_id,
                agent_id=agent_id,
                action_type=action_type,
                platform=platform,
                params=params,
                score=score,
                metrics=metrics or {},
                context_data=context or {},
                timestamp=datetime.utcnow()
            )
            db.add(db_outcome)
            await db.commit()
            
            logger.info(f"OutcomeTracker: Recorded [{action_type}] on [{platform}] -> {score}")

            # Auto-analyze
            outcomes = await cls._get_all_outcomes(db, user_id)
            if len(outcomes) % 10 == 0:
                await cls._auto_analyze(db, user_id)
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def _get_all_outcomes(cls, db: AsyncSession, user_id: str) -> List[DBActionOutcome]:
        stmt = select(DBActionOutcome).where(DBActionOutcome.user_id == user_id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    # --- Pattern Analysis ---

    @classmethod
    async def _auto_analyze(cls, db: AsyncSession, user_id: str):
        """Run automatic pattern analysis on accumulated outcomes."""
        outcomes = await cls._get_all_outcomes(db, user_id)
        # Group by action_type + platform
        groups = defaultdict(list)
        for outcome in outcomes:
            key = f"{outcome.action_type}_{outcome.platform}"
            groups[key].append(outcome)

        for group_key, group_outcomes in groups.items():
            if len(group_outcomes) < 5:
                continue

            # Score map for numerical comparison
            score_map = {"excellent": 5, "good": 4, "neutral": 3, "poor": 2, "failed": 1}
            
            # Find contextual patterns (e.g., time of day, day of week)
            context_performance = defaultdict(lambda: {"scores": [], "count": 0})
            
            for o in group_outcomes:
                for ctx_key, ctx_value in o.context_data.items():
                    ctx_group = f"{ctx_key}={ctx_value}"
                    context_performance[ctx_group]["scores"].append(score_map.get(o.score, 3))
                    context_performance[ctx_group]["count"] += 1

            # Find best-performing contexts
            for ctx_group, data in context_performance.items():
                if data["count"] >= 3:
                    avg_score = sum(data["scores"]) / len(data["scores"])
                    if avg_score >= 4.0:  # Good or better
                        pattern_key = f"{group_key}_{ctx_group}"
                        
                        stmt = select(DBLearnedPattern).where(
                            DBLearnedPattern.user_id == user_id,
                            DBLearnedPattern.category == pattern_key
                        )
                        result = await db.execute(stmt)
                        existing_pattern = result.scalar_one_or_none()
                        
                        if not existing_pattern:
                            new_pattern = DBLearnedPattern(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                category=pattern_key,
                                insight=f"{group_key} performs best when {ctx_group} (avg score: {avg_score:.1f}/5)",
                                recommendation=f"Optimize {group_key}: prefer {ctx_group}",
                                supporting_data={"avg_score": avg_score, "sample_size": data["count"]},
                                confidence_score=min(data["count"] / 10, 1.0),
                                sample_size=data["count"]
                            )
                            db.add(new_pattern)
                            logger.info(f"OutcomeTracker: New pattern [{new_pattern.insight}]")
        await db.commit()

    @classmethod
    async def get_active_patterns(cls, db: Optional[AsyncSession], user_id: str) -> List[PydanticLearnedPattern]:
        """Return all active optimization patterns."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(DBLearnedPattern).where(
                DBLearnedPattern.user_id == user_id,
                DBLearnedPattern.active == True
            )
            result = await db.execute(stmt)
            db_patterns = result.scalars().all()
            
            return [
                PydanticLearnedPattern(
                    id=p.id,
                    category=p.category,
                    insight=p.insight,
                    recommendation=p.recommendation,
                    supporting_data=p.supporting_data,
                    confidence_score=p.confidence_score,
                    sample_size=p.sample_size,
                    active=p.active,
                ) for p in db_patterns
            ]
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def get_optimization_prompt(cls, db: Optional[AsyncSession], user_id: str) -> str:
        """Generate a context prompt for the Orchestrator with optimization insights."""
        active = await cls.get_active_patterns(db, user_id)
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
    async def analyze_patterns_llm(cls, db: Optional[AsyncSession], user_id: str) -> List[PydanticLearnedPattern]:
        """Use LLM to discover deeper cause-effect patterns."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            outcomes = await cls._get_all_outcomes(db, user_id)
            if len(outcomes) < 10:
                return []

            recent = outcomes[-100:]
            outcomes_data = [
                {
                    "action": o.action_type,
                    "platform": o.platform,
                    "score": o.score,
                    "metrics": o.metrics,
                    "context": o.context_data,
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
                    category = p.get("category", "general")
                    # Check if already exists conceptually (using a hash of category+insight could be better, but we just check category)
                    stmt = select(DBLearnedPattern).where(
                        DBLearnedPattern.user_id == user_id,
                        DBLearnedPattern.category == f"llm_{category}"
                    )
                    result = await db.execute(stmt)
                    existing_pattern = result.scalar_one_or_none()
                    
                    if not existing_pattern:
                        new_pattern = DBLearnedPattern(
                            id=str(uuid.uuid4()),
                            user_id=user_id,
                            category=f"llm_{category}",
                            insight=p["insight"],
                            recommendation=p["recommendation"],
                            supporting_data=p.get("supporting_data", {}),
                            confidence_score=p.get("confidence_score", 0.5),
                            sample_size=len(recent),
                            active=True
                        )
                        db.add(new_pattern)
                        p_pattern = PydanticLearnedPattern(
                            id=new_pattern.id,
                            category=new_pattern.category,
                            insight=new_pattern.insight,
                            recommendation=new_pattern.recommendation,
                            supporting_data=new_pattern.supporting_data,
                            confidence_score=new_pattern.confidence_score,
                            sample_size=new_pattern.sample_size,
                            active=True
                        )
                        new_patterns.append(p_pattern)
                await db.commit()
                return new_patterns
            except Exception as e:
                logger.error(f"LLM pattern analysis failed: {e}")
                return []
        finally:
            if should_close:
                await db.close()

    # --- Querying ---

    @classmethod
    async def get_best_strategy(cls, db: Optional[AsyncSession], user_id: str, action_type: str) -> Optional[PydanticLearnedPattern]:
        """Get the highest-confidence optimization for a given action type."""
        active_patterns = await cls.get_active_patterns(db, user_id)
        relevant = [p for p in active_patterns if action_type in p.category]
        if not relevant:
            return None
        return max(relevant, key=lambda p: p.confidence_score)

    @classmethod
    async def get_performance_summary(cls, db: Optional[AsyncSession], user_id: str, action_type: str = None) -> Dict[str, Any]:
        """Get a summary of action performance."""
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            outcomes = await cls._get_all_outcomes(db, user_id)
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
        finally:
            if should_close:
                await db.close()
