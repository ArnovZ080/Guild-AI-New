import os
import aiohttp
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PaystackClient:
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or os.getenv("PAYSTACK_SECRET_KEY")
        self.base_url = "https://api.paystack.co"
        
    async def initialize_transaction(self, email: str, amount_usd: float, reference: str, callback_url: str) -> Dict[str, Any]:
        """
        Initialize a transaction with Paystack. 
        Note: Amount should be converted to subunits (e.g. kobo/cents).
        For simplicity, we assume 1 USD = 100 subunits in this logic, 
        but in production, currency conversion to NGN/ZAR would happen here.
        """
        if not self.secret_key:
            logger.warning("Paystack: SECRET_KEY not found. Running in mock mode.")
            return {"status": True, "data": {"authorization_url": f"https://checkout.paystack.com/mock?ref={reference}", "reference": reference}}

        url = f"{self.base_url}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        # Simplified amount conversion (USD to cents)
        amount_subunits = int(amount_usd * 100)
        
        payload = {
            "email": email,
            "amount": amount_subunits,
            "reference": reference,
            "callback_url": callback_url,
            "metadata": {"source": "guild_ai_new"}
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                data = await resp.json()
                if not data.get("status"):
                    logger.error(f"Paystack Initialization Failed: {data.get('message')}")
                return data

    async def verify_transaction(self, reference: str) -> Dict[str, Any]:
        """Verify a Paystack transaction."""
        if not self.secret_key:
            return {"status": True, "data": {"status": "success", "amount": 0, "reference": reference}}

        url = f"{self.base_url}/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {self.secret_key}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                return await resp.json()

paystack_client = PaystackClient()
