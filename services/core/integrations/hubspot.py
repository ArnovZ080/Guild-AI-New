from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp

from services.core.logging import logger
from services.core.integrations.base import BaseIntegration, IntegrationConfig, IntegrationRegistry
from services.core.integrations.crm import Contact, Deal, LeadStatus

class HubSpotIntegration(BaseIntegration):
    """HubSpot CRM Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://api.hubapi.com"
        self.session: Optional[aiohttp.ClientSession] = None
        self.access_token = self.config.credentials.get("access_token")

    @property
    def capabilities(self) -> List[str]:
        return ["get_contacts", "create_contact", "get_deals", "create_deal"]

    async def _ensure_session(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None, params: Dict = None) -> Dict:
        await self._ensure_session()
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            async with self.session.request(method, url, json=data, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"HubSpot API request failed: {e}")
            raise

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        # Mock validation for migration
        return True

    async def get_contacts(self, limit: int = 100) -> List[Contact]:
        # MOCK IMPLEMENTATION
        logger.info("Fetching HubSpot contacts (MOCK)")
        return [
            Contact(
                id="hs_123",
                email="alice@example.com",
                first_name="Alice",
                last_name="Doe",
                status=LeadStatus.NEW
            )
        ]

    async def create_contact(self, email: str, first_name: str, last_name: str) -> Contact:
        # MOCK IMPLEMENTATION
        logger.info(f"Creating HubSpot contact: {email}")
        return Contact(
            id="hs_new_456",
            email=email,
            first_name=first_name,
            last_name=last_name,
            status=LeadStatus.NEW
        )

# Register
IntegrationRegistry.register("hubspot", HubSpotIntegration)
