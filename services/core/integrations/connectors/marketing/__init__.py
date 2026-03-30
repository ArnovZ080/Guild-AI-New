"""
Marketing Connectors.
Real API implementations for MetaAds, GoogleAds, LinkedInAds,
Mailchimp, ConvertKit, and ActiveCampaign.
"""
import logging
import httpx
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)


class MetaAdsIntegration(BaseIntegration):
    """
    Meta (Facebook/Instagram) Ads integration.
    Auth: Bearer token (User or System User access token).
    """

    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")
        self.ad_account_id = self.config.credentials.get("ad_account_id", "")

    def _params(self, extra: Optional[Dict] = None) -> Dict[str, Any]:
        p: Dict[str, Any] = {"access_token": self.access_token}
        if extra:
            p.update(extra)
        return p

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/me",
                    params=self._params(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Meta Ads validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_ad_campaign":
            return await self._create_campaign(params)
        elif action_name == "get_ad_campaign_metrics":
            return await self._get_metrics(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _create_campaign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        account = self.ad_account_id or params.get("ad_account_id")
        if not account:
            raise ValueError("ad_account_id required")
        payload = {
            "name": params.get("name", "Campaign"),
            "objective": params.get("objective", "OUTCOME_TRAFFIC"),
            "status": params.get("status", "PAUSED"),
            "special_ad_categories": params.get("special_ad_categories", []),
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/act_{account}/campaigns",
                params=self._params(),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": "success", "campaign_id": data.get("id")}

    async def _get_metrics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        campaign_id = params.get("campaign_id")
        if not campaign_id:
            raise ValueError("campaign_id required")
        fields = "spend,impressions,clicks,conversions,cpc,cpm"
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.BASE_URL}/{campaign_id}/insights",
                params=self._params({"fields": fields}),
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            insights = data.get("data", [{}])
            return insights[0] if insights else {}

    @property
    def capabilities(self) -> List[str]:
        return ["create_ad_campaign", "get_ad_campaign_metrics"]


class GoogleAdsIntegration(BaseIntegration):
    """
    Google Ads integration (connector-level).
    Auth: OAuth2 access_token + developer_token + customer_id.
    """

    BASE_URL = "https://googleads.googleapis.com/v14"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")
        self.developer_token = self.config.credentials.get("developer_token", "")
        self.customer_id = self.config.credentials.get("customer_id", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "developer-token": self.developer_token,
            "Content-Type": "application/json",
        }

    async def validate_connection(self) -> bool:
        if not self.access_token or not self.customer_id:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/customers/{self.customer_id}",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Google Ads validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_ad_campaign":
            return await self._create_campaign(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _create_campaign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "operations": [
                {
                    "create": {
                        "name": params.get("name", "Campaign"),
                        "advertisingChannelType": params.get("channel", "SEARCH"),
                        "status": "PAUSED",
                        "campaignBudget": params.get("budget_resource"),
                    }
                }
            ]
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/customers/{self.customer_id}/campaigns:mutate",
                headers=self._headers(),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [{}])
            resource = results[0].get("resourceName", "") if results else ""
            return {"status": "success", "campaign_id": resource}

    @property
    def capabilities(self) -> List[str]:
        return ["create_ad_campaign"]


class LinkedInAdsIntegration(BaseIntegration):
    """
    LinkedIn Ads integration.
    Auth: Bearer token (OAuth2).
    """

    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")
        self.ad_account_id = self.config.credentials.get("ad_account_id", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/adAccountsV2",
                    headers=self._headers(),
                    params={"q": "search", "count": 1},
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"LinkedIn Ads validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_ad_campaign":
            return await self._create_campaign(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _create_campaign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        account = self.ad_account_id or params.get("ad_account_id")
        if not account:
            raise ValueError("ad_account_id required")
        payload = {
            "account": f"urn:li:sponsoredAccount:{account}",
            "name": params.get("name", "Campaign"),
            "status": "PAUSED",
            "type": params.get("type", "TEXT_AD"),
            "costType": params.get("cost_type", "CPM"),
            "dailyBudget": {"amount": str(params.get("daily_budget", "50")), "currencyCode": "USD"},
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/adCampaignsV2",
                headers=self._headers(),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            # LinkedIn returns the campaign ID in the x-restli-id header
            campaign_id = resp.headers.get("x-restli-id", resp.json().get("id", ""))
            return {"status": "success", "campaign_id": campaign_id}

    @property
    def capabilities(self) -> List[str]:
        return ["create_ad_campaign"]


class MailchimpIntegration(BaseIntegration):
    """
    Mailchimp integration.
    Auth: Basic Auth with any username and API key as password.
    DC (datacenter) is extracted from the API key suffix.
    """

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.api_key = self.config.credentials.get("api_key", "")
        self.dc = self.api_key.split("-")[-1] if "-" in self.api_key else "us1"
        self.base_url = f"https://{self.dc}.api.mailchimp.com/3.0"

    def _auth(self) -> httpx.BasicAuth:
        return httpx.BasicAuth("anystring", self.api_key)

    async def validate_connection(self) -> bool:
        if not self.api_key:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.base_url}/ping",
                    auth=self._auth(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Mailchimp validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "add_subscriber":
            return await self._add_subscriber(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _add_subscriber(self, params: Dict[str, Any]) -> Dict[str, Any]:
        list_id = params.get("list_id")
        email = params.get("email")
        if not list_id or not email:
            raise ValueError("list_id and email required")
        payload = {
            "email_address": email,
            "status": params.get("status", "subscribed"),
            "merge_fields": params.get("merge_fields", {}),
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/lists/{list_id}/members",
                auth=self._auth(),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": "success", "email": data.get("email_address"), "id": data.get("id")}

    @property
    def capabilities(self) -> List[str]:
        return ["add_subscriber"]


class ConvertKitIntegration(BaseIntegration):
    """
    ConvertKit (now Kit) email marketing integration.
    Auth: API secret passed as query param.
    """

    BASE_URL = "https://api.convertkit.com/v3"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.api_secret = self.config.credentials.get("api_secret", "")

    async def validate_connection(self) -> bool:
        if not self.api_secret:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/account",
                    params={"api_secret": self.api_secret},
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"ConvertKit validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "add_subscriber":
            return await self._add_subscriber(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _add_subscriber(self, params: Dict[str, Any]) -> Dict[str, Any]:
        form_id = params.get("form_id")
        email = params.get("email")
        if not form_id or not email:
            raise ValueError("form_id and email required")
        payload = {
            "api_secret": self.api_secret,
            "email": email,
            "first_name": params.get("first_name", ""),
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/forms/{form_id}/subscribe",
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            sub = data.get("subscription", {})
            return {"status": "success", "email": email, "subscriber_id": sub.get("subscriber", {}).get("id")}

    @property
    def capabilities(self) -> List[str]:
        return ["add_subscriber"]


class ActiveCampaignIntegration(BaseIntegration):
    """
    ActiveCampaign integration.
    Auth: Api-Token header. Requires account URL + API token.
    """

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.account_url = self.config.credentials.get("account_url", "").rstrip("/")
        self.api_token = self.config.credentials.get("api_token", "")
        self.base_url = f"{self.account_url}/api/3" if self.account_url else ""

    def _headers(self) -> Dict[str, str]:
        return {"Api-Token": self.api_token}

    async def validate_connection(self) -> bool:
        if not self.account_url or not self.api_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.base_url}/users/me",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"ActiveCampaign validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "add_subscriber":
            return await self._add_subscriber(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _add_subscriber(self, params: Dict[str, Any]) -> Dict[str, Any]:
        email = params.get("email")
        if not email:
            raise ValueError("email required")
        payload = {
            "contact": {
                "email": email,
                "firstName": params.get("first_name", ""),
                "lastName": params.get("last_name", ""),
            }
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/contacts",
                headers=self._headers(),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            contact = data.get("contact", {})
            return {"status": "success", "email": email, "contact_id": contact.get("id")}

    @property
    def capabilities(self) -> List[str]:
        return ["add_subscriber"]


# Export
__all__ = [
    "MetaAdsIntegration",
    "GoogleAdsIntegration",
    "LinkedInAdsIntegration",
    "MailchimpIntegration",
    "ConvertKitIntegration",
    "ActiveCampaignIntegration",
]
