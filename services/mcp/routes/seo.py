from fastapi import HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from services.core.logging import logger
from services.core.integrations.base import IntegrationRegistry, IntegrationConfig
from services.mcp.router_base import MCPRouter

router = MCPRouter(tags=["seo"])

# --- Request Models ---

class KeywordResearchRequest(BaseModel):
    platform: str # "ahrefs" or "semrush"
    keyword: str

# --- Routes ---

@router.post("/tools/keyword_research", name="keyword_research", description="Get keyword data")
async def keyword_research(request: KeywordResearchRequest):
    try:
        config = IntegrationConfig(
            name=f"mcp_{request.platform}",
            credentials={"api_key": "mock"}
        )
        
        integration = IntegrationRegistry.initialize_integration(request.platform, config)
        
        if request.platform == "ahrefs":
            result = await integration.get_keyword_data(request.keyword)
        elif request.platform == "semrush":
            result = await integration.get_keyword_overview(request.keyword)
        else:
            raise ValueError(f"Platform {request.platform} not supported for keyword research")
            
        return {"status": "success", "data": result}

    except Exception as e:
        logger.error(f"Error executing keyword research: {e}")
        raise HTTPException(status_code=500, detail=str(e))
