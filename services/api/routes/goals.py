"""Goals API Routes"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.db.base import get_db
from services.core.db.models import UserAccount
from services.api.middleware.auth import get_current_user
from services.core.goals.engine import goals_engine

router = APIRouter()


class CreateGoalRequest(BaseModel):
    title: str
    target_metric: str
    target_value: float
    description: str = ""


class MilestoneRequest(BaseModel):
    title: str
    process_snapshot: dict = {}
    repeatable: bool = False


class RepeatRequest(BaseModel):
    new_target_value: float


class ProgressRequest(BaseModel):
    value: float


@router.post("/")
async def create_goal(request: CreateGoalRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    goal = await goals_engine.create_goal(db, current_user.id, request.title, request.target_metric, request.target_value, request.description)
    return {"id": goal.id, "title": goal.title, "status": goal.status}


@router.get("/")
async def list_goals(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    goals = await goals_engine.list_goals(db, current_user.id)
    return {"goals": [{"id": g.id, "title": g.title, "target": g.target_value, "current": g.current_value,
                        "status": g.status, "metric": g.target_metric} for g in goals]}


@router.get("/{goal_id}")
async def get_goal(goal_id: str, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    return await goals_engine.get_goal_with_milestones(db, goal_id)


@router.post("/{goal_id}/progress")
async def update_progress(goal_id: str, request: ProgressRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    goal = await goals_engine.track_progress(db, goal_id, request.value)
    return {"id": goal.id, "current": goal.current_value, "status": goal.status}


@router.post("/{goal_id}/milestones")
async def record_milestone(goal_id: str, request: MilestoneRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    m = await goals_engine.record_milestone(db, goal_id, request.title, request.process_snapshot, request.repeatable)
    return {"id": m.id, "title": m.title, "repeatable": m.repeatable}


@router.post("/{goal_id}/repeat")
async def repeat_milestone(goal_id: str, request: RepeatRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    # Uses the latest repeatable milestone from this goal
    from sqlalchemy import select
    from services.core.db.models import Milestone
    result = await db.execute(select(Milestone).where(Milestone.goal_id == goal_id, Milestone.repeatable == True).order_by(Milestone.reached_at.desc()))
    milestone = result.scalars().first()
    if not milestone:
        raise HTTPException(status_code=404, detail="No repeatable milestone found")
    goal = await goals_engine.repeat_with_escalation(db, milestone.id, current_user.id, request.new_target_value)
    return {"id": goal.id, "title": goal.title, "target": goal.target_value}
