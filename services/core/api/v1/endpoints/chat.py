from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.api import deps
from services.core.api.schemas import ChatRequest, ChatResponse
from services.core.db.models import UserAccount
from services.core.agents.orchestrator import OrchestratorAgent
from services.core.agents.base import AgentConfig

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.check_tier_limits),
) -> Any:
    """
    Main chat endpoint — delegates to the OrchestratorAgent.
    """
    orchestrator = OrchestratorAgent(AgentConfig(
        name="orchestrator",
        model="gpt-4-turbo-preview",
        description="Core orchestrator"
    ))
    
    context = {
        "user_id": current_user.id,
        "db": db,
        **(request.context_overrides or {})
    }
    
    input_data = {
        "goal": request.goal,
        "require_preflight": request.require_preflight,
    }
    
    result = await orchestrator.run(input_data, context)
    
    return ChatResponse(
        status=result.status.value if hasattr(result.status, 'value') else str(result.status),
        data=result.data if isinstance(result.data, dict) else {"result": str(result.data)},
        process_log=result.process_log or [],
        educational_takeaway=result.educational_takeaway
    )
