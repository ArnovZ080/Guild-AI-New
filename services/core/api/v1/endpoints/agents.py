from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.api import deps
from services.core.api.schemas import AgentExecuteRequest
from services.core.db.models import UserAccount
from services.core.agents.registry import AgentRegistry
from services.core.agents.base import AgentConfig

router = APIRouter()

@router.post("/{agent_name}/execute")
async def execute_agent(
    agent_name: str,
    request: AgentExecuteRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.check_tier_limits),
) -> Any:
    """
    Execute a specific agent by name.
    """
    agent_cls = AgentRegistry.get(agent_name)
    if not agent_cls:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    
    config = AgentConfig(name=agent_name, model="gpt-4-turbo-preview", description=f"Direct execution of {agent_name}")
    agent = agent_cls(config)
    
    context = {
        "user_id": current_user.id,
        "db": db,
        **(request.context or {})
    }
    
    result = await agent.run(request.input_data, context)
    
    return {
        "agent": agent_name,
        "status": result.status.value if hasattr(result.status, 'value') else str(result.status),
        "data": result.data if isinstance(result.data, dict) else {"result": str(result.data)},
        "process_log": result.process_log or [],
    }

@router.get("")
async def list_agents(
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """
    List all registered agents and their capabilities.
    """
    return {"agents": AgentRegistry.get_description_map()}
