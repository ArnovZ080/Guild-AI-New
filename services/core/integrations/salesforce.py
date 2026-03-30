from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp

from services.core.logging import logger
from services.core.integrations.base import BaseIntegration, IntegrationConfig, IntegrationRegistry
from services.core.integrations.crm import Contact, Deal, LeadStatus

class SalesforceIntegration(BaseIntegration):
    """Salesforce CRM Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.instance_url = self.config.credentials.get("instance_url")
        self.access_token = self.config.credentials.get("access_token")
        self.api_version = "v59.0"
        self.session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> List[str]:
        return ["get_contacts", "create_contact", "get_opportunities"]

    async def validate_connection(self) -> bool:
        if not self.access_token or not self.instance_url:
            return False
        try:
            await self._ensure_session()
            headers = {"Authorization": f"Bearer {self.access_token}"}
            async with self.session.get(
                f"{self.instance_url}/services/data/{self.api_version}/sobjects/",
                headers=headers,
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"Salesforce validation failed: {e}")
            return False

    async def _ensure_session(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def get_contacts(self) -> List[Contact]:
        """Fetch contacts from Salesforce via SOQL."""
        await self._ensure_session()
        headers = {"Authorization": f"Bearer {self.access_token}"}
        query = "SELECT Id, Email, FirstName, LastName, Company, LeadSource FROM Contact LIMIT 50"
        async with self.session.get(
            f"{self.instance_url}/services/data/{self.api_version}/query/",
            headers=headers,
            params={"q": query},
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            records = data.get("records", [])
            return [
                Contact(
                    id=r.get("Id", ""),
                    email=r.get("Email", ""),
                    first_name=r.get("FirstName", ""),
                    last_name=r.get("LastName", ""),
                    status=LeadStatus.QUALIFIED,
                    company=r.get("Company", ""),
                )
                for r in records
            ]

    async def create_contact(self, email: str, first_name: str, last_name: str) -> Contact:
        """Create a contact in Salesforce."""
        await self._ensure_session()
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "Email": email,
            "FirstName": first_name,
            "LastName": last_name,
        }
        async with self.session.post(
            f"{self.instance_url}/services/data/{self.api_version}/sobjects/Contact/",
            headers=headers,
            json=payload,
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return Contact(
                id=data.get("id", ""),
                email=email,
                first_name=first_name,
                last_name=last_name,
                status=LeadStatus.NEW,
            )

# Register
IntegrationRegistry.register("salesforce", SalesforceIntegration)
