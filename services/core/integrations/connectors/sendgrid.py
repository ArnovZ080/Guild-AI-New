import logging
import httpx
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)

class SendGridIntegration(BaseIntegration):
    """
    SendGrid integration port.
    Focuses on transactional email delivery.
    """
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://api.sendgrid.com/v3"
        self.api_key = self.config.credentials.get("api_key")
        
    async def validate_connection(self) -> bool:
        """Validate connection by fetching user account info."""
        if not self.api_key:
            return False
            
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = await client.get(f"{self.base_url}/user/account", headers=headers)
            return response.status_code == 200

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        """Execute SendGrid specific actions."""
        if action_name == "send_message" or action_name == "send_email":
            return await self._send_email(params)
        else:
            raise ValueError(f"Action '{action_name}' not supported by SendGrid.")

    async def _send_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a transactional email."""
        recipient = params.get("recipient") or params.get("to")
        subject = params.get("subject", "Notification from Guild AI")
        content = params.get("content") or params.get("message")
        
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "personalizations": [{"to": [{"email": recipient}], "subject": subject}],
                "from": {"email": self.config.credentials.get("from_email", "system@guild-ai.com")},
                "content": [{"type": "text/html", "value": content}]
            }
            
            response = await client.post(f"{self.base_url}/mail/send", headers=headers, json=payload)
            if response.status_code == 202:
                return {"status": "success", "message_id": response.headers.get("X-Message-Id")}
            else:
                logger.error(f"SendGrid failed: {response.text}")
                return {"status": "error", "message": response.text}

    @property
    def capabilities(self) -> List[str]:
        return ["send_email"]
