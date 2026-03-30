from typing import Dict, Any, List, Optional
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field
import aiohttp
import httpx

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

    @property
    def capabilities(self) -> List[str]:
        return ["get_keyword_data", "get_backlinks", "get_serp_data"]

    async def validate_connection(self) -> bool:
        if not self.api_key:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    self.base_url,
                    params={"token": self.api_key, "from": "ahrefs_rank", "target": "ahrefs.com", "mode": "domain", "limit": 1, "output": "json"},
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Ahrefs validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "get_keyword_data":
            keyword = params.get("keyword", "")
            return await self.get_keyword_data(keyword)
        raise ValueError(f"Unknown action {action_name}")

    async def get_keyword_data(self, keyword: str) -> KeywordData:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self.base_url,
                params={"token": self.api_key, "from": "keywords_explorer", "target": keyword, "mode": "exact", "output": "json"},
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            keywords = data.get("keywords", [{}])
            kw = keywords[0] if keywords else {}
            return KeywordData(
                keyword=keyword,
                search_volume=kw.get("volume", 0),
                difficulty=KeywordDifficulty.MEDIUM,
                cpc=kw.get("cpc", 0.0),
                related_keywords=kw.get("related", []),
            )

class SEMrushIntegration(BaseIntegration):
    """SEMrush SEO Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://api.semrush.com"
        self.api_key = self.config.credentials.get("api_key")

    @property
    def capabilities(self) -> List[str]:
        return ["get_keyword_overview", "get_domain_rank"]

    async def validate_connection(self) -> bool:
        if not self.api_key:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    self.base_url,
                    params={"type": "domain_ranks", "key": self.api_key, "domain": "semrush.com", "export_columns": "Dn"},
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"SEMrush validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "get_keyword_overview":
            keyword = params.get("keyword", "")
            return await self.get_keyword_overview(keyword)
        raise ValueError(f"Unknown action {action_name}")

    async def get_keyword_overview(self, keyword: str) -> KeywordData:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self.base_url,
                params={"type": "phrase_this", "key": self.api_key, "phrase": keyword, "export_columns": "Ph,Nq,Kd,Cp", "database": "us"},
                timeout=15.0,
            )
            resp.raise_for_status()
            # SEMrush returns semicolon-delimited text
            lines = resp.text.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split(";")
                return KeywordData(
                    keyword=keyword,
                    search_volume=int(parts[1]) if len(parts) > 1 else 0,
                    difficulty=KeywordDifficulty.HARD,
                    cpc=float(parts[3]) if len(parts) > 3 else 0.0,
                    related_keywords=[],
                )
            return KeywordData(keyword=keyword, search_volume=0, difficulty=KeywordDifficulty.MEDIUM)

class GoogleSearchConsoleIntegration(BaseIntegration):
    """Google Search Console Integration"""

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.base_url = "https://searchconsole.googleapis.com/webmasters/v3"
        self.access_token = self.config.credentials.get("access_token")

    @property
    def capabilities(self) -> List[str]:
        return ["get_sites", "get_search_analytics"]

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.base_url}/sites",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"GSC validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "get_sites":
            return await self.get_sites()
        raise ValueError(f"Unknown action {action_name}")

    async def get_sites(self) -> List[str]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/sites",
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return [entry.get("siteUrl", "") for entry in data.get("siteEntry", [])]

# Register
IntegrationRegistry.register("ahrefs", AhrefsIntegration)
IntegrationRegistry.register("semrush", SEMrushIntegration)
IntegrationRegistry.register("google_search_console", GoogleSearchConsoleIntegration)
