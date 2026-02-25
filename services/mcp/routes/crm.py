from fastapi import HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from services.core.logging import logger
from services.core.integrations.base import IntegrationRegistry, IntegrationConfig
from services.mcp.router_base import MCPRouter

router = MCPRouter(tags=["crm"])

# --- Request Models ---

class CreateContactRequest(BaseModel):
    platform: str # "hubspot" or "salesforce"
    email: str
    first_name: str
    last_name: str

class GetContactsRequest(BaseModel):
    platform: str

# --- Routes ---

@router.post("/tools/create_contact", name="create_contact", description="Create a contact in CRM")
async def create_contact(request: CreateContactRequest):
    try:
        config = IntegrationConfig(
            name=f"mcp_{request.platform}",
            credentials={"access_token": "mock", "instance_url": "https://mock.salesforce.com"}
        )
        
        integration = IntegrationRegistry.initialize_integration(request.platform, config)
        
        result = await integration.create_contact(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name
        )
        
        return {"status": "success", "contact": result}

    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools/get_contacts", name="get_contacts", description="Get contacts from CRM")
async def get_contacts(request: GetContactsRequest):
    try:
        config = IntegrationConfig(
            name=f"mcp_{request.platform}",
            credentials={"access_token": "mock", "instance_url": "https://mock.salesforce.com"}
        )
        
        integration = IntegrationRegistry.initialize_integration(request.platform, config)
        
        # Some integrations take different args, generic 'get_contacts' usually takes limit/offset
        # HubSpot takes limit, Salesforce takes distinct query logic in real life.
        # Base mock implementation signatures:
        # HubSpot: get_contacts(limit=100)
        # Salesforce: get_contacts() 
        
        if request.platform == "hubspot":
            results = await integration.get_contacts(limit=10)
        else:
            results = await integration.get_contacts()
            
        return {"status": "success", "contacts": results}

    except Exception as e:
        logger.error(f"Error getting contacts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
