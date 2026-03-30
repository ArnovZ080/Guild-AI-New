import aiohttp
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from services.core.logging import logger
from services.core.integrations.base import BaseIntegration, IntegrationConfig, IntegrationRegistry

class SocialCredentials(BaseModel):
    """Standardized credentials for social platforms"""
    access_token: str
    user_id: Optional[str] = None
    refresh_token: Optional[str] = None
    app_id: Optional[str] = None
    app_secret: Optional[str] = None

class TwitterIntegration(BaseIntegration):
    """Twitter/X Integration"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.credentials = SocialCredentials(**self.config.credentials)
        self.base_url = "https://api.twitter.com/2"
        self.session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> List[str]:
        return ["post_content", "get_analytics", "get_profile"]

    async def _ensure_session(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None, params: Dict = None) -> Dict:
        await self._ensure_session()
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Authorization': f'Bearer {self.credentials.access_token}',
                'Content-Type': 'application/json'
            }
            
            async with self.session.request(method, url, json=data, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
                
        except Exception as e:
            logger.error(f"Twitter API request failed: {e}")
            raise

    async def validate_connection(self) -> bool:
        if not self.credentials.access_token:
            return False
        try:
            await self._ensure_session()
            url = f"{self.base_url}/users/me"
            headers = {
                'Authorization': f'Bearer {self.credentials.access_token}',
                'Content-Type': 'application/json'
            }
            async with self.session.request('GET', url, headers=headers) as response:
                return response.status == 200
        except Exception:
            return False

    async def post_content(self, content: str) -> Dict[str, Any]:
        """Post a tweet"""
        endpoint = "tweets"
        data = {"text": content}
        return await self._make_request(endpoint, method='POST', data=data)

    async def close(self):
        if self.session:
            await self.session.close()

class LinkedInIntegration(BaseIntegration):
    """LinkedIn Integration"""
    
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.credentials = SocialCredentials(**self.config.credentials)
        self.base_url = "https://api.linkedin.com/v2"
        self.session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> List[str]:
        return ["post_content", "get_profile"]

    async def _ensure_session(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        await self._ensure_session()
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Authorization': f'Bearer {self.credentials.access_token}',
                'Content-Type': 'application/json'
            }
            async with self.session.request(method, url, json=data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"LinkedIn API request failed: {e}")
            raise

    async def validate_connection(self) -> bool:
        return bool(self.credentials.access_token)

    async def get_profile(self) -> Dict[str, Any]:
        endpoint = "people/~:(id,firstName,lastName)"
        return await self._make_request(endpoint)

    async def post_content(self, content: str) -> Dict[str, Any]:
        """Create a LinkedIn post"""
        endpoint = "ugcPosts"
        # We need the author URN. In a real app we'd cache this.
        profile = await self.get_profile()
        author_urn = f"urn:li:person:{profile.get('id', 'unknown')}"
        
        data = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        return await self._make_request(endpoint, method='POST', data=data)

    async def close(self):
        if self.session:
            await self.session.close()

# Register integrations
IntegrationRegistry.register("twitter", TwitterIntegration)
IntegrationRegistry.register("linkedin", LinkedInIntegration)
