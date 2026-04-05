"""
Goals Engine — Milestone tracking with repeatable processes

Create goals, track progress, record milestones, and repeat what works.
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.models import Goal, Milestone

logger = logging.getLogger(__name__)


class GoalsEngine:
    """Business goal management with repeatable process recording."""

    async def create_goal(
        self,
        db: AsyncSession,
        user_id: str,
        title: str,
        target_metric: str,
        target_value: float,
        description: str = "",
    ) -> Goal:
        goal = Goal(
            user_id=user_id,
            title=title,
            description=description,
            target_metric=target_metric,
            target_value=target_value,
            current_value=0.0,
            status="active",
        )
        db.add(goal)
        await db.commit()
        await db.refresh(goal)
        return goal

    async def track_progress(self, db: AsyncSession, goal_id: str, new_value: float) -> Goal:
        """Update current progress."""
        result = await db.execute(select(Goal).where(Goal.id == goal_id))
        goal = result.scalars().first()
        if not goal:
            raise ValueError("Goal not found")

        goal.current_value = new_value
        if new_value >= goal.target_value:
            goal.status = "completed"
            goal.completed_at = datetime.utcnow()

        await db.commit()
        await db.refresh(goal)
        return goal

    async def record_milestone(
        self,
        db: AsyncSession,
        goal_id: str,
        title: str,
        process_snapshot: dict,
        repeatable: bool = False,
    ) -> Milestone:
        """Record a milestone with what actions led to it."""
        milestone = Milestone(
            goal_id=goal_id,
            title=title,
            reached_at=datetime.utcnow(),
            process_snapshot=process_snapshot,
            repeatable=repeatable,
        )
        db.add(milestone)
        await db.commit()
        await db.refresh(milestone)
        return milestone

    async def repeat_with_escalation(
        self,
        db: AsyncSession,
        milestone_id: str,
        user_id: str,
        new_target_value: float,
    ) -> Goal:
        """Repeat the process that achieved a milestone with a higher target."""
        result = await db.execute(select(Milestone).where(Milestone.id == milestone_id))
        milestone = result.scalars().first()
        if not milestone:
            raise ValueError("Milestone not found")

        # Create new goal based on the milestone's process snapshot
        snapshot = milestone.process_snapshot or {}
        new_goal = Goal(
            user_id=user_id,
            title=f"Repeat: {milestone.title} (escalated)",
            description=f"Repeating process from milestone '{milestone.title}' with escalated target",
            target_metric=snapshot.get("metric", ""),
            target_value=new_target_value,
            current_value=0.0,
            status="active",
            process_recording=snapshot,
        )
        db.add(new_goal)
        await db.commit()
        await db.refresh(new_goal)
        return new_goal

    async def list_goals(self, db: AsyncSession, user_id: str) -> List[Goal]:
        result = await db.execute(
            select(Goal).where(Goal.user_id == user_id).order_by(Goal.created_at.desc()))
        return list(result.scalars().all())

    async def get_goal_with_milestones(self, db: AsyncSession, goal_id: str) -> dict:
        result = await db.execute(select(Goal).where(Goal.id == goal_id))
        goal = result.scalars().first()
        if not goal:
            raise ValueError("Goal not found")

        ms_result = await db.execute(
            select(Milestone).where(Milestone.goal_id == goal_id).order_by(Milestone.reached_at))
        milestones = list(ms_result.scalars().all())

        progress = (goal.current_value / goal.target_value * 100) if goal.target_value > 0 else 0

        return {
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "target_metric": goal.target_metric,
            "target_value": goal.target_value,
            "current_value": goal.current_value,
            "progress_pct": round(min(progress, 100), 1),
            "status": goal.status,
            "milestones": [
                {"id": m.id, "title": m.title, "reached_at": m.reached_at.isoformat() if m.reached_at else None,
                 "repeatable": m.repeatable}
                for m in milestones
            ],
        }


# Global
goals_engine = GoalsEngine()
