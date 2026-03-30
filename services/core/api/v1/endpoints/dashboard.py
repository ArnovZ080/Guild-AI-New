from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from services.core.api import deps
from services.core.db.models import (
    UserAccount, Project, WorkflowExecution, AgentOutput,
    CustomerJourney, LLMUsageRecord
)

router = APIRouter()

@router.get("/snapshot")
async def dashboard_snapshot(
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """
    Returns a comprehensive CEO dashboard snapshot.
    """
    user_id = current_user.id
    
    # Active projects count
    proj_count = await db.execute(
        select(func.count(Project.id)).where(Project.user_id == user_id)
    )
    
    # Workflow executions count
    wf_count = await db.execute(
        select(func.count(WorkflowExecution.id)).where(WorkflowExecution.user_id == user_id)
    )
    
    # Agent outputs count
    output_count = await db.execute(
        select(func.count(AgentOutput.id)).where(AgentOutput.user_id == user_id)
    )
    
    # Customer journeys
    journey_count = await db.execute(
        select(func.count(CustomerJourney.id)).where(CustomerJourney.user_id == user_id)
    )
    
    # Token usage this month
    from datetime import datetime
    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    token_usage = await db.execute(
        select(func.sum(LLMUsageRecord.total_tokens)).where(
            LLMUsageRecord.user_id == user_id,
            LLMUsageRecord.timestamp >= start_of_month,
        )
    )
    
    return {
        "user_tier": current_user.tier,
        "projects_count": proj_count.scalar() or 0,
        "workflows_run": wf_count.scalar() or 0,
        "agent_outputs": output_count.scalar() or 0,
        "customer_journeys": journey_count.scalar() or 0,
        "tokens_used_this_month": token_usage.scalar() or 0,
    }
