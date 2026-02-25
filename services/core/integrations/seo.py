from typing import Dict, Any, List, Optional
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field
import aiohttp

from services.core.logging import logger
from services.core.integrations.base import BaseIntegration, IntegrationConfig, IntegrationRegistry

# --- Enums & Models ---

class KeywordDifficulty(str, Enum):
    VERY_EASY = "very_easy"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"

class KeywordData(BaseModel):
    keyword: str
    search_volume: int
    difficulty: KeywordDifficulty
    cpc: float = 0.0
    competition: float = 0.0
    related_keywords: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BacklinkData(BaseModel):
    source_url: str
    target_url: str
    domain_rating: float = 0.0
    link_type: str = "dofollow"

class SERPData(BaseModel):
    keyword: str
    position: int
    url: str
    title: str
    description: str
    domain: str

# --- Integrations ---

class AhrefsIntegration(BaseIntegration):
    """Ahrefs SEO Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://apiv2.ahrefs.com"
        self.api_key = self.config.credentials.get("api_key")
        self.session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> List[str]:
        return ["get_keyword_data", "get_backlinks", "get_serp_data"]

    async def validate_connection(self) -> bool:
        return bool(self.api_key)

    async def get_keyword_data(self, keyword: str) -> KeywordData:
        # MOCK IMPLEMENTATION
        logger.info(f"Fetching Ahrefs keyword data for: {keyword}")
        return KeywordData(
            keyword=keyword,
            search_volume=1500,
            difficulty=KeywordDifficulty.MEDIUM,
            cpc=2.5,
            related_keywords=[f"{keyword} tips", f"best {keyword}"]
        )

class SEMrushIntegration(BaseIntegration):
    """SEMrush SEO Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://api.semrush.com"
        self.api_key = self.config.credentials.get("api_key")
        self.session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> List[str]:
        return ["get_keyword_overview", "get_domain_rank"]

    async def validate_connection(self) -> bool:
        return bool(self.api_key)

    async def get_keyword_overview(self, keyword: str) -> KeywordData:
        # MOCK IMPLEMENTATION
        logger.info(f"Fetching SEMrush keyword overview for: {keyword}")
        return KeywordData(
            keyword=keyword,
            search_volume=1200,
            difficulty=KeywordDifficulty.HARD,
            cpc=3.0,
            related_keywords=[]
        )

class GoogleSearchConsoleIntegration(BaseIntegration):
    """Google Search Console Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://searchconsole.googleapis.com/webmasters/v3"
        self.access_token = self.config.credentials.get("access_token")
        self.session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> List[str]:
        return ["get_sites", "get_search_analytics"]

    async def validate_connection(self) -> bool:
        return bool(self.access_token)

    async def get_sites(self) -> List[str]:
        # MOCK IMPLEMENTATION
        logger.info("Fetching GSC sites")
        return ["https://example.com", "https://blog.example.com"]

# Register
IntegrationRegistry.register("ahrefs", AhrefsIntegration)
IntegrationRegistry.register("semrush", SEMrushIntegration)
IntegrationRegistry.register("google_search_console", GoogleSearchConsoleIntegration)
