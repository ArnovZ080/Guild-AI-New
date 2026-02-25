import logging
import httpx
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)

class GoogleCalendarIntegration(BaseIntegration):
    """
    Google Calendar integration port.
    """
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://www.googleapis.com/calendar/v3"
        
    async def validate_connection(self) -> bool:
        """Validate connection by fetching the calendar list."""
        token = self.config.credentials.get("api_key")
        if not token:
            return False
            
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{self.base_url}/users/me/calendarList", headers=headers)
            return response.status_code == 200

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        """Execute Calendar specific actions."""
        if action_name == "create_event":
            return await self._create_event(params)
        elif action_name == "list_events":
            return await self._list_events(params)
        else:
            raise ValueError(f"Action '{action_name}' not supported by Google Calendar.")

    async def _create_event(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a calendar event."""
        token = self.config.credentials.get("api_key")
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {
                "summary": params.get("title", "AI Scheduled Event"),
                "description": params.get("description", ""),
                "start": {"dateTime": params.get("start_time")},
                "end": {"dateTime": params.get("end_time")},
            }
            
            response = await client.post(f"{self.base_url}/calendars/primary/events", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def _list_events(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List upcoming events."""
        token = self.config.credentials.get("api_key")
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{self.base_url}/calendars/primary/events", headers=headers)
            response.raise_for_status()
            return response.json().get("items", [])

    @property
    def capabilities(self) -> List[str]:
        return ["create_event", "list_events"]
