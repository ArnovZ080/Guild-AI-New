import logging
import httpx
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)

class TwitterIntegration(BaseIntegration):
    """
    Twitter/X integration port.
    """
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://api.twitter.com/2"
        
    async def validate_connection(self) -> bool:
        """Validate connection by fetching authenticating user info."""
        token = self.config.credentials.get("api_key")
        if not token:
            return False
            
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{self.base_url}/users/me", headers=headers)
            return response.status_code == 200

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        """Execute Twitter specific actions."""
        if action_name == "post_content":
            return await self._create_tweet(params)
        elif action_name == "get_user_info":
            return await self._get_user_info()
        else:
            raise ValueError(f"Action '{action_name}' not supported by Twitter.")

    async def _create_tweet(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Post a tweet."""
        token = self.config.credentials.get("api_key")
        content = params.get("content")
        if not content:
            raise ValueError("Tweet content is required.")
            
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {"text": content}
            
            response = await client.post(f"{self.base_url}/tweets", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def _get_user_info(self) -> Dict[str, Any]:
        """Get authenticating user information."""
        token = self.config.credentials.get("api_key")
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{self.base_url}/users/me", headers=headers)
            response.raise_for_status()
            return response.json()

    @property
    def capabilities(self) -> List[str]:
        return ["post_content", "get_user_info"]
