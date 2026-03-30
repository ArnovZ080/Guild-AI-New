from typing import Dict, Any, List, Optional
from datetime import date, timedelta
from enum import Enum
from pydantic import BaseModel, Field
import aiohttp
import asyncio

from services.core.logging import logger
from services.core.integrations.base import BaseIntegration, IntegrationConfig, IntegrationRegistry

# --- Enums & Models ---

class AdPlatform(str, Enum):
    GOOGLE_ADS = "google_ads"
    TIKTOK_ADS = "tiktok_ads"
    META_ADS = "meta_ads"

class CampaignObjective(str, Enum):
    AWARENESS = "AWARENESS"
    TRAFFIC = "TRAFFIC"
    ENGAGEMENT = "ENGAGEMENT"
    LEADS = "LEADS"
    SALES = "SALES"
    APP_PROMOTION = "APP_PROMOTION"

class BidStrategy(str, Enum):
    MANUAL_CPC = "MANUAL_CPC"
    TARGET_CPA = "TARGET_CPA"
    TARGET_ROAS = "TARGET_ROAS"
    MAXIMIZE_CONVERSIONS = "MAXIMIZE_CONVERSIONS"
    MAXIMIZE_CONVERSION_VALUE = "MAXIMIZE_CONVERSION_VALUE"

class AdCredentials(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    developer_token: Optional[str] = None # Google specific
    customer_id: Optional[str] = None # Google specific
    advertiser_id: Optional[str] = None # TikTok specific

class CampaignData(BaseModel):
    id: str
    name: str
    objective: CampaignObjective
    status: str
    budget: float
    start_date: date
    end_date: Optional[date] = None
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AdExperiment(BaseModel):
    experiment_id: str
    name: str
    platform: AdPlatform
    campaigns: List[str]
    status: str
    results: Dict[str, Any] = Field(default_factory=dict)

# --- Integrations ---

class GoogleAdsIntegration(BaseIntegration):
    """Google Ads Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.credentials = AdCredentials(**self.config.credentials)
        self.base_url = "https://googleads.googleapis.com/v14"
        self.session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> List[str]:
        return ["create_campaign", "get_campaigns", "create_experiment"]

    async def _ensure_session(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None, params: Dict = None) -> Dict:
        await self._ensure_session()
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Authorization': f'Bearer {self.credentials.access_token}',
                'developer-token': self.credentials.developer_token or "",
                'Content-Type': 'application/json'
            }
            async with self.session.request(method, url, json=data, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Google Ads API request failed: {e}")
            raise

    async def validate_connection(self) -> bool:
        if not self.credentials.customer_id or not self.credentials.access_token:
            return False
        try:
            await self._make_request(f"customers/{self.credentials.customer_id}")
            return True
        except Exception as e:
            logger.error(f"Google Ads validation failed: {e}")
            return False

    async def create_campaign(self, name: str, budget: float, objective: CampaignObjective) -> CampaignData:
        customer_id = self.credentials.customer_id
        if not customer_id:
            raise ValueError("Customer ID required")

        endpoint = f"customers/{customer_id}/campaigns:mutate"
        payload = {
            "operations": [{
                "create": {
                    "name": name,
                    "advertisingChannelType": "SEARCH",
                    "status": "PAUSED",
                }
            }]
        }
        data = await self._make_request(endpoint, method='POST', data=payload)
        results = data.get("results", [{}])
        campaign_id = results[0].get("resourceName", "").split("/")[-1] if results else ""
        return CampaignData(
            id=campaign_id or f"ga_{name[:8]}",
            name=name,
            objective=objective,
            status="PAUSED",
            budget=budget,
            start_date=date.today()
        )

class TikTokAdsIntegration(BaseIntegration):
    """TikTok Ads Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.credentials = AdCredentials(**self.config.credentials)
        self.base_url = "https://business-api.tiktok.com/open_api/v1.3"
        self.session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> List[str]:
        return ["create_campaign", "get_campaigns"]

    async def validate_connection(self) -> bool:
        if not self.credentials.access_token or not self.credentials.advertiser_id:
            return False
        try:
            if not self.session or self.session.closed:
                self.session = aiohttp.ClientSession()
            headers = {
                "Access-Token": self.credentials.access_token,
                "Content-Type": "application/json",
            }
            async with self.session.get(
                f"{self.base_url}/advertiser/info/",
                params={"advertiser_ids": f'["{self.credentials.advertiser_id}"]'},
                headers=headers,
            ) as resp:
                resp.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"TikTok Ads validation failed: {e}")
            return False

    async def create_campaign(self, name: str, budget: float, objective: CampaignObjective) -> CampaignData:
        advertiser_id = self.credentials.advertiser_id
        if not advertiser_id:
            raise ValueError("Advertiser ID required")

        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

        headers = {
            "Access-Token": self.credentials.access_token,
            "Content-Type": "application/json",
        }
        payload = {
            "advertiser_id": advertiser_id,
            "campaign_name": name,
            "objective_type": objective.value,
            "budget": budget,
            "budget_mode": "BUDGET_MODE_TOTAL",
        }
        async with self.session.post(
            f"{self.base_url}/campaign/create/",
            json=payload,
            headers=headers,
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            campaign_id = str(data.get("data", {}).get("campaign_id", ""))

        return CampaignData(
            id=campaign_id or f"tt_{name[:8]}",
            name=name,
            objective=objective,
            status="ENABLE",
            budget=budget,
            start_date=date.today()
        )

# Register
IntegrationRegistry.register("google_ads", GoogleAdsIntegration)
IntegrationRegistry.register("tiktok_ads", TikTokAdsIntegration)
