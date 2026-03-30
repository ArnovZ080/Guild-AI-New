"""
Commerce Connectors.
Real API implementations for PayPal, Square, Shopify, WooCommerce, and Amazon.
"""
import logging
import base64
import httpx
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)


class PayPalIntegration(BaseIntegration):
    """
    PayPal integration.
    Auth: OAuth2 client credentials (client_id + client_secret → bearer token).
    """

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.client_id = self.config.credentials.get("client_id", "")
        self.client_secret = self.config.credentials.get("client_secret", "")
        self.sandbox = self.config.credentials.get("sandbox", True)
        self.base_url = (
            "https://api-m.sandbox.paypal.com"
            if self.sandbox
            else "https://api-m.paypal.com"
        )
        self._token: Optional[str] = None

    async def _get_token(self) -> str:
        if self._token:
            return self._token
        creds = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/v1/oauth2/token",
                headers={
                    "Authorization": f"Basic {creds}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"grant_type": "client_credentials"},
                timeout=10.0,
            )
            resp.raise_for_status()
            self._token = resp.json()["access_token"]
            return self._token

    def _headers(self, token: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    async def validate_connection(self) -> bool:
        if not self.client_id or not self.client_secret:
            return False
        try:
            await self._get_token()
            return True
        except Exception as e:
            logger.error(f"PayPal validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_invoice":
            return await self._create_invoice(params)
        elif action_name == "check_payment_status":
            return await self._check_payment_status(params)
        elif action_name == "process_refund":
            return await self._process_refund(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _create_invoice(self, params: Dict[str, Any]) -> Dict[str, Any]:
        token = await self._get_token()
        payload = {
            "detail": {
                "currency_code": params.get("currency", "USD"),
                "note": params.get("note", ""),
                "memo": params.get("memo", ""),
            },
            "items": params.get("items", []),
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/v2/invoicing/invoices",
                headers=self._headers(token),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            return resp.json()

    async def _check_payment_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        token = await self._get_token()
        order_id = params.get("order_id") or params.get("transaction_id")
        if not order_id:
            raise ValueError("order_id or transaction_id required")
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/v2/checkout/orders/{order_id}",
                headers=self._headers(token),
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": data.get("status"), "id": data.get("id")}

    async def _process_refund(self, params: Dict[str, Any]) -> Dict[str, Any]:
        token = await self._get_token()
        capture_id = params.get("capture_id")
        if not capture_id:
            raise ValueError("capture_id required")
        payload = {}
        if params.get("amount"):
            payload = {
                "amount": {
                    "value": str(params["amount"]),
                    "currency_code": params.get("currency", "USD"),
                }
            }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/v2/payments/captures/{capture_id}/refund",
                headers=self._headers(token),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": data.get("status"), "refund_id": data.get("id")}

    @property
    def capabilities(self) -> List[str]:
        return ["create_invoice", "check_payment_status", "process_refund"]


class SquareIntegration(BaseIntegration):
    """
    Square POS integration.
    Auth: Bearer token (access_token).
    """

    BASE_URL = "https://connect.squareup.com/v2"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Square-Version": "2024-01-18",
        }

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/locations",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Square validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "sync_pos":
            return await self._sync_pos(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _sync_pos(self, params: Dict[str, Any]) -> Dict[str, Any]:
        location_id = params.get("location_id")
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/payments"
            query = {"location_id": location_id} if location_id else {}
            resp = await client.get(
                url, headers=self._headers(), params=query, timeout=15.0
            )
            resp.raise_for_status()
            data = resp.json()
            payments = data.get("payments", [])
            return {"status": "success", "synced_transactions": len(payments)}

    @property
    def capabilities(self) -> List[str]:
        return ["sync_pos"]


class ShopifyIntegration(BaseIntegration):
    """
    Shopify Admin API integration.
    Auth: X-Shopify-Access-Token header. Requires shop_domain + access_token.
    """

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.shop_domain = self.config.credentials.get("shop_domain", "")
        self.access_token = self.config.credentials.get("access_token", "")
        self.api_version = self.config.credentials.get("api_version", "2024-01")
        self.base_url = (
            f"https://{self.shop_domain}/admin/api/{self.api_version}"
            if self.shop_domain
            else ""
        )

    def _headers(self) -> Dict[str, str]:
        return {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json",
        }

    async def validate_connection(self) -> bool:
        if not self.shop_domain or not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.base_url}/shop.json",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Shopify validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "get_product_catalog":
            return await self._get_products(params)
        elif action_name == "get_recent_orders":
            return await self._get_orders(params)
        elif action_name == "sync_inventory":
            return await self._sync_inventory(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _get_products(self, params: Dict[str, Any]) -> Dict[str, Any]:
        limit = params.get("limit", 50)
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/products.json",
                headers=self._headers(),
                params={"limit": limit},
                timeout=15.0,
            )
            resp.raise_for_status()
            return resp.json()

    async def _get_orders(self, params: Dict[str, Any]) -> Dict[str, Any]:
        limit = params.get("limit", 50)
        status = params.get("status", "any")
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/orders.json",
                headers=self._headers(),
                params={"limit": limit, "status": status},
                timeout=15.0,
            )
            resp.raise_for_status()
            return resp.json()

    async def _sync_inventory(self, params: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/inventory_levels.json",
                headers=self._headers(),
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            items = data.get("inventory_levels", [])
            return {"status": "success", "synced_items": len(items)}

    @property
    def capabilities(self) -> List[str]:
        return ["get_product_catalog", "get_recent_orders", "sync_inventory"]


class WooCommerceIntegration(BaseIntegration):
    """
    WooCommerce integration.
    Auth: Basic Auth (consumer_key + consumer_secret).
    """

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.store_url = self.config.credentials.get("store_url", "").rstrip("/")
        self.consumer_key = self.config.credentials.get("consumer_key", "")
        self.consumer_secret = self.config.credentials.get("consumer_secret", "")
        self.base_url = f"{self.store_url}/wp-json/wc/v3" if self.store_url else ""

    def _auth(self) -> httpx.BasicAuth:
        return httpx.BasicAuth(self.consumer_key, self.consumer_secret)

    async def validate_connection(self) -> bool:
        if not self.store_url or not self.consumer_key or not self.consumer_secret:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.base_url}/system_status",
                    auth=self._auth(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"WooCommerce validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "sync_orders":
            return await self._sync_orders(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _sync_orders(self, params: Dict[str, Any]) -> Dict[str, Any]:
        per_page = params.get("per_page", 50)
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/orders",
                auth=self._auth(),
                params={"per_page": per_page},
                timeout=15.0,
            )
            resp.raise_for_status()
            orders = resp.json()
            return {"status": "success", "synced_orders": len(orders)}

    @property
    def capabilities(self) -> List[str]:
        return ["sync_orders"]


class AmazonIntegration(BaseIntegration):
    """
    Amazon Selling Partner API integration.
    Auth: LWA (Login with Amazon) access_token. Simplified — real impl would use
    AWS Signature V4. This uses the SP-API access_token approach.
    """

    BASE_URL = "https://sellingpartnerapi-na.amazon.com"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")
        self.marketplace_id = self.config.credentials.get(
            "marketplace_id", "ATVPDKIKX0DER"
        )  # US default

    def _headers(self) -> Dict[str, str]:
        return {
            "x-amz-access-token": self.access_token,
            "Content-Type": "application/json",
        }

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/sellers/v1/marketplaceParticipations",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Amazon SP-API validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "get_seller_metrics":
            return await self._get_seller_metrics(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _get_seller_metrics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.BASE_URL}/sellers/v1/marketplaceParticipations",
                headers=self._headers(),
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            participations = data.get("payload", [])
            return {
                "active_marketplaces": len(participations),
                "marketplace_id": self.marketplace_id,
            }

    @property
    def capabilities(self) -> List[str]:
        return ["get_seller_metrics"]


# Export
__all__ = [
    "PayPalIntegration",
    "SquareIntegration",
    "ShopifyIntegration",
    "WooCommerceIntegration",
    "AmazonIntegration",
]
