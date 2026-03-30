from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.api import deps
from services.core.api.schemas import WorkflowExecuteRequest, WorkflowApproveRequest
from services.core.db.models import UserAccount, WorkflowExecution
from services.core.workflows.executor import WorkflowExecutor

router = APIRouter()

@router.post("/{template}/execute")
async def execute_workflow(
    template: str,
    request: WorkflowExecuteRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.check_tier_limits),
) -> Any:
    """
    Execute a workflow template.
    """
    executor = WorkflowExecutor()
    try:
        result = await executor.execute_template(
            template_name=template,
            params=request.params or {},
            context={"user_id": current_user.id, "db": db}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return {"workflow": template, "status": "completed", "result": result}

@router.post("/{workflow_id}/approve-step")
async def approve_workflow_step(
    workflow_id: str,
    request: WorkflowApproveRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.check_tier_limits),
) -> Any:
    """
    Approve or reject a workflow step that requires human authorization.
    """
    result = await db.execute(
        select(WorkflowExecution).where(
            WorkflowExecution.id == workflow_id,
            WorkflowExecution.user_id == current_user.id
        )
    )
    wf = result.scalars().first()
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {
        "workflow_id": workflow_id,
        "step_index": request.step_index,
        "approved": request.approved,
        "status": "step_approved" if request.approved else "step_rejected",
    }

@router.get("")
async def list_workflows(
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """
    List workflow executions for the current user.
    """
    result = await db.execute(
        select(WorkflowExecution).where(WorkflowExecution.user_id == current_user.id)
    )
    workflows = result.scalars().all()
    return {
        "workflows": [
            {
                "id": w.id,
                "workflow_name": w.workflow_name,
                "status": w.status,
                "started_at": str(w.started_at),
                "completed_at": str(w.completed_at) if w.completed_at else None,
            }
            for w in workflows
        ]
    }
