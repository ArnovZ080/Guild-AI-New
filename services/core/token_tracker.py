"""
Guild-AI Token Tracking & Cost Estimation

Tracks per-agent, per-workflow, per-user token usage and cost.
Provides upfront cost estimation before workflow execution.
Enforces monthly budget limits per subscription tier.
"""
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from services.core.config import settings

logger = logging.getLogger(__name__)


# ── Pricing (per 1M tokens) ──
# Source: Vertex AI pricing as of 2026
PRICING = {
    # model_name: (input_per_1M, output_per_1M)
    settings.GEMINI_FLASH_MODEL: (0.075, 0.30),
    settings.GEMINI_PRO_MODEL: (1.25, 5.00),
    "claude-sonnet-4-20250514": (3.00, 15.00),
    # Defaults for unknown models
    "_default": (1.00, 5.00),
}

# Monthly token budgets by subscription tier
TIER_BUDGETS = {
    "starter": 2_000_000,   # ~$0.50-$2.00 cost
    "growth": 10_000_000,   # ~$2.50-$10.00 cost
    "scale": 30_000_000,    # ~$7.50-$30.00 cost
    "free": 100_000,        # Trial
}

ALERT_THRESHOLDS = [0.75, 0.90, 1.00]


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    """Calculate the dollar cost for a given LLM call."""
    pricing = PRICING.get(model, PRICING["_default"])
    input_cost = (input_tokens / 1_000_000) * pricing[0]
    output_cost = (output_tokens / 1_000_000) * pricing[1]
    return round(input_cost + output_cost, 6)


class TokenTracker:
    """Track and enforce token usage budgets."""

    async def record_usage(
        self,
        db: AsyncSession,
        user_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        agent_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Record token usage after an LLM call.

        Returns dict with `cost`, `total_tokens`, and any `alerts`.
        """
        from services.core.db.models import LLMUsageRecord

        cost = calculate_cost(model, input_tokens, output_tokens)
        total = input_tokens + output_tokens

        record = LLMUsageRecord(
            user_id=user_id,
            provider="vertex_ai" if "gemini" in model else "anthropic",
            model=model,
            prompt_tokens=input_tokens,
            completion_tokens=output_tokens,
            total_tokens=total,
            cost=cost,
            agent_id=agent_id,
            workflow_id=workflow_id,
        )
        db.add(record)
        await db.commit()

        # Check budget alerts
        alerts = await self._check_alerts(db, user_id)

        return {"cost": cost, "total_tokens": total, "alerts": alerts}

    async def estimate_workflow_cost(
        self,
        steps: list,
        tier_per_step: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Estimate cost before running a workflow.

        Args:
            steps: List of workflow step descriptions.
            tier_per_step: Optional list of ModelTier per step.

        Returns:
            Dict with `estimated_tokens`, `estimated_cost`, `per_step`.
        """
        from services.core.llm import ModelTier

        per_step = []
        total_input = 0
        total_output = 0

        for i, step in enumerate(steps):
            # Estimate based on typical usage patterns
            tier = (
                tier_per_step[i] if tier_per_step
                else ModelTier.FLASH
            )
            model = (
                settings.GEMINI_PRO_MODEL if tier == ModelTier.PRO
                else settings.GEMINI_FLASH_MODEL
            )

            # Rough estimates per step type
            est_input = 2000   # ~2K input tokens average
            est_output = 1000  # ~1K output tokens average
            if tier == ModelTier.PRO:
                est_input = 4000
                est_output = 2000

            cost = calculate_cost(model, est_input, est_output)
            per_step.append({
                "step": i,
                "description": str(step)[:100],
                "model": model,
                "estimated_input_tokens": est_input,
                "estimated_output_tokens": est_output,
                "estimated_cost": cost,
            })
            total_input += est_input
            total_output += est_output

        total_cost = sum(s["estimated_cost"] for s in per_step)

        return {
            "estimated_input_tokens": total_input,
            "estimated_output_tokens": total_output,
            "estimated_total_tokens": total_input + total_output,
            "estimated_cost": round(total_cost, 4),
            "per_step": per_step,
        }

    async def get_monthly_usage(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> Dict[str, Any]:
        """Get current month's token usage and cost for a user."""
        from services.core.db.models import LLMUsageRecord

        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        result = await db.execute(
            select(
                func.coalesce(func.sum(LLMUsageRecord.total_tokens), 0),
                func.coalesce(func.sum(LLMUsageRecord.cost), 0.0),
                func.count(LLMUsageRecord.id),
            ).where(
                LLMUsageRecord.user_id == user_id,
                LLMUsageRecord.timestamp >= month_start,
            )
        )
        row = result.one()

        return {
            "total_tokens": int(row[0]),
            "total_cost": float(row[1]),
            "call_count": int(row[2]),
            "period_start": month_start.isoformat(),
        }

    async def check_budget(
        self,
        db: AsyncSession,
        user_id: str,
        user_tier: str,
    ) -> Dict[str, Any]:
        """
        Check if user is within budget.

        Returns dict with `within_budget`, `usage_percentage`, `alerts`.
        """
        usage = await self.get_monthly_usage(db, user_id)
        budget = TIER_BUDGETS.get(user_tier, TIER_BUDGETS["free"])
        pct = usage["total_tokens"] / budget if budget > 0 else 1.0

        alerts = []
        for threshold in ALERT_THRESHOLDS:
            if pct >= threshold:
                alerts.append(f"Token usage at {int(threshold * 100)}% of monthly budget")

        return {
            "within_budget": pct < 1.0,
            "usage_percentage": round(pct * 100, 1),
            "tokens_used": usage["total_tokens"],
            "token_budget": budget,
            "cost_this_month": usage["total_cost"],
            "alerts": alerts,
        }

    async def _check_alerts(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> list:
        """Internal: check if usage crossed any alert thresholds."""
        from services.core.db.models import UserAccount

        result = await db.execute(
            select(UserAccount.tier).where(UserAccount.id == user_id)
        )
        tier = result.scalar_one_or_none() or "free"

        budget_info = await self.check_budget(db, user_id, tier)
        return budget_info["alerts"]


# Global instance
token_tracker = TokenTracker()
