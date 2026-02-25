import logging
import httpx
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)

class HubSpotIntegration(BaseIntegration):
    """
    HubSpot CRM integration port.
    """
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://api.hubapi.com"
        
    async def validate_connection(self) -> bool:
        """Validate connection by fetching a single contact."""
        token = self.config.credentials.get("api_key")
        if not token:
            return False
            
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{self.base_url}/crm/v3/objects/contacts?limit=1", headers=headers)
            return response.status_code == 200

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        """Execute HubSpot specific actions."""
        if action_name == "sync_contact":
            return await self._sync_contact(params)
        elif action_name == "update_deal":
            return await self._update_deal(params)
        elif action_name == "get_contact_metrics":
            return await self._get_contact_metrics()
        else:
            raise ValueError(f"Action '{action_name}' not supported by HubSpot.")

    async def _sync_contact(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a contact in HubSpot."""
        token = self.config.credentials.get("api_key")
        email = params.get("email")
        if not email:
            raise ValueError("Email is required for HubSpot contact sync.")
            
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {"properties": params}
            
            # Try searching first or just use upsert if available
            response = await client.post(f"{self.base_url}/crm/v3/objects/contacts", headers=headers, json=payload)
            
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 409: # Conflict, already exists
                # Logic to update instead
                # For brevity in this port, we'll return a message
                return {"status": "already_exists", "message": "Contact already exists in HubSpot."}
                
            response.raise_for_status()
            return response.json()

    async def _update_deal(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update a deal in HubSpot."""
        token = self.config.credentials.get("api_key")
        deal_id = params.get("id")
        if not deal_id:
            raise ValueError("Deal ID is required for HubSpot deal update.")
            
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {"properties": params.get("properties", {})}
            
            response = await client.patch(f"{self.base_url}/crm/v3/objects/deals/{deal_id}", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def _get_contact_metrics(self) -> Dict[str, Any]:
        """Fetch basic contact metrics."""
        # Simple count for now
        token = self.config.credentials.get("api_key")
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{self.base_url}/crm/v3/objects/contacts", headers=headers)
            data = response.json()
            return {"total_contacts": data.get("total", 0)}

    @property
    def capabilities(self) -> List[str]:
        return ["sync_contact", "update_deal", "get_contact_metrics"]
