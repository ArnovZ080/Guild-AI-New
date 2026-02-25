from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

from services.core.agents.registry import AgentRegistry, AgentCapability
# Import agents to trigger registration
import services.core.agents.research
import services.core.agents.content
import services.core.adk.financial_advisor
import services.core.adk.business_intelligence
import services.core.adk.customer_intelligence
import services.core.adk.marketing_strategist
import services.core.adk.trend_analyst
import services.core.interfaces.voice
from services.core.agents.base import AgentConfig
from services.core.logging import logger
from services.core.utils.event_bus import event_bus
from services.core.agents.models import AgentEvent

router = APIRouter(prefix="/agents", tags=["agents"])

class AgentRunRequest(BaseModel):
    input_data: Any
    context: Optional[Dict] = None

class AgentRunResponse(BaseModel):
    status: str
    message: str
    run_id: Optional[str] = None # For future async task tracking

class AgentCapabilityResponse(BaseModel):
    name: str
    category: str
    capabilities: List[str]
    description: str

@router.get("/", response_model=List[AgentCapabilityResponse])
async def list_agents():
    """List all available agent capabilities."""
    registry_items = AgentRegistry.list_all()
    # Convert dataclasses to Pydantic models (excluding agent_class)
    return [
        AgentCapabilityResponse(
            name=item.name,
            category=item.category,
            capabilities=item.capabilities,
            description=item.description
        ) for item in registry_items
    ]

@router.post("/{agent_name}/run", response_model=AgentRunResponse)
async def run_agent(agent_name: str, request: AgentRunRequest, background_tasks: BackgroundTasks):
    """
    Trigger an agent run.
    For now, this runs synchronously or via background tasks.
    In production, this should dispatch to Celery.
    """
    capability = AgentRegistry.get(agent_name)
    if not capability:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    
    if not capability.agent_class:
        raise HTTPException(status_code=500, detail=f"Agent class for '{agent_name}' not registered")

    # Instantiate the agent
    try:
        config = AgentConfig(
            name=agent_name,
            description=capability.description,
            tools=capability.capabilities 
        )
        agent_instance = capability.agent_class(config)
        
        # Run the agent (synchronously for now to return result, or background)
        # Detailed implementation:
        # If we want a result immediately, we await it.
        # If we want async, we use background_tasks.
        
        # For this phase, let's await it to verify it works, then move to async.
        # Ideally, we return a run_id and have a status endpoint.
        
        result = await agent_instance.run(request.input_data, request.context)
        
        # In a real system, we'd store the result in DB/Redis associated with a run_id
        
        return AgentRunResponse(
            status="completed",
            message="Agent execution successful",
            run_id="sync-execution" # Placeholder
        )

    except Exception as e:
        logger.error(f"Failed to run agent {agent_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events", response_model=List[AgentEvent])
async def get_agent_events(since_id: Optional[str] = None, limit: int = 50):
    """
    Retrieve real-time agent activity events.
    Polling endpoint for the Agent Theater UI.
    """
    return event_bus.get_events(since_id=since_id, limit=limit)
