from fastapi import HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from services.core.logging import logger
from services.core.integrations.base import IntegrationRegistry, IntegrationConfig
from services.mcp.router_base import MCPRouter

router = MCPRouter(tags=["ads"])

# --- Request Models ---

class CreateCampaignRequest(BaseModel):
    platform: str # "google_ads" or "tiktok_ads"
    name: str
    budget: float
    objective: str

# --- Routes ---

@router.post("/tools/create_campaign", name="create_campaign", description="Create an ad campaign on a specific platform")
async def create_campaign(request: CreateCampaignRequest):
    """
    Create an ad campaign.
    Platform must be 'google_ads' or 'tiktok_ads'.
    """
    try:
        # Mock Config - In production, fetch from DB
        config = IntegrationConfig(
            name=f"mcp_{request.platform}",
            credentials={
                "api_key": "mock_key", 
                "access_token": "mock_token",
                "customer_id": "123-456-7890", # Added mock customer_id
                "advertiser_id": "mock_adv_id" # For TikTok
            }
        )
        
        integration_name = request.platform
        integration = IntegrationRegistry.initialize_integration(integration_name, config)
        
        # Determine objective enum
        # For simplicity, passing as string, integration might expect Enum. 
        # Base implementation uses CampaignObjective enum. 
        # We'll map string to enum if needed, or update integration to accept str.
        # Assuming integration handles it or we pass a mock object.
        from services.core.integrations.ads import CampaignObjective
        objective_enum = CampaignObjective.TRAFFIC # Defaulting for simplicity of mock
        
        result = await integration.create_campaign(
            name=request.name,
            budget=request.budget,
            objective=objective_enum
        )
        
        return {
            "status": "success",
            "campaign": result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating campaign: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
