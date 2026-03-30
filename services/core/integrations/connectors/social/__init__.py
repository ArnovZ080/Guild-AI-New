"""
Social & Job-Board Connectors.
Real API implementations for MetaSocial, LinkedIn, TikTok, Indeed, and Upwork.
"""
import logging
import httpx
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)


class MetaSocialIntegration(BaseIntegration):
    """
    Meta (Facebook/Instagram) social publishing integration.
    Auth: User access token with pages_manage_posts permission.
    """

    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")
        self.page_id = self.config.credentials.get("page_id", "")

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
            logger.error(f"Meta Social validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "publish_post":
            return await self._publish_post(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _publish_post(self, params: Dict[str, Any]) -> Dict[str, Any]:
        page = self.page_id or params.get("page_id")
        if not page:
            raise ValueError("page_id required")
        message = params.get("message", "")
        link = params.get("link")
        payload: Dict[str, Any] = {"message": message}
        if link:
            payload["link"] = link
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/{page}/feed",
                params=self._params(),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": "success", "post_id": data.get("id")}

    @property
    def capabilities(self) -> List[str]:
        return ["publish_post"]


class LinkedInSocialIntegration(BaseIntegration):
    """
    LinkedIn social posting integration.
    Auth: Bearer token (OAuth2 with w_member_social scope).
    """

    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")

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
                    f"{self.BASE_URL}/me",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"LinkedIn Social validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "publish_post":
            return await self._publish_post(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _publish_post(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Get author URN from /me
        async with httpx.AsyncClient() as client:
            me_resp = await client.get(
                f"{self.BASE_URL}/me", headers=self._headers(), timeout=10.0
            )
            me_resp.raise_for_status()
            person_id = me_resp.json().get("id", "")
            author_urn = f"urn:li:person:{person_id}"

        content = params.get("content", params.get("message", ""))
        payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/ugcPosts",
                headers=self._headers(),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            post_id = resp.headers.get("x-restli-id", resp.json().get("id", ""))
            return {"status": "success", "post_id": post_id}

    @property
    def capabilities(self) -> List[str]:
        return ["publish_post"]


class TikTokIntegration(BaseIntegration):
    """
    TikTok social integration (Content Posting API / Research API).
    Auth: Bearer token from TikTok Login Kit.
    """

    BASE_URL = "https://open.tiktokapis.com/v2"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/user/info/",
                    headers=self._headers(),
                    params={"fields": "display_name"},
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"TikTok validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "publish_video":
            return await self._publish_video(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _publish_video(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate a video upload via TikTok Content Posting API.
        Requires video_url or chunk_size for direct upload.
        """
        payload = {
            "post_info": {
                "title": params.get("title", ""),
                "privacy_level": params.get("privacy_level", "SELF_ONLY"),
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": params.get("video_url", ""),
            },
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/post/publish/video/init/",
                headers=self._headers(),
                json=payload,
                timeout=30.0,
            )
            resp.raise_for_status()
            data = resp.json()
            publish_id = data.get("data", {}).get("publish_id", "")
            return {"status": "success", "publish_id": publish_id}

    @property
    def capabilities(self) -> List[str]:
        return ["publish_video"]


class IndeedIntegration(BaseIntegration):
    """
    Indeed job posting integration.
    Auth: Bearer token (Indeed Publisher API / GraphQL).
    Note: Indeed's API access is highly restricted. This implements the
    GraphQL-based approach for employers with API access.
    """

    BASE_URL = "https://apis.indeed.com/graphql"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")
        self.employer_id = self.config.credentials.get("employer_id", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Indeed-Employer-Id": self.employer_id,
        }

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.BASE_URL,
                    headers=self._headers(),
                    json={"query": "{ __typename }"},
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Indeed validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "post_job":
            return await self._post_job(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _post_job(self, params: Dict[str, Any]) -> Dict[str, Any]:
        title = params.get("title", "")
        description = params.get("description", "")
        location = params.get("location", "")

        mutation = """
        mutation CreateJobPosting($input: CreateJobPostingInput!) {
            createJobPosting(input: $input) {
                jobPosting { id title status }
            }
        }
        """
        variables = {
            "input": {
                "title": title,
                "description": description,
                "location": {"city": location},
            }
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.BASE_URL,
                headers=self._headers(),
                json={"query": mutation, "variables": variables},
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            job = data.get("data", {}).get("createJobPosting", {}).get("jobPosting", {})
            return {"status": "success", "job_id": job.get("id", "")}

    @property
    def capabilities(self) -> List[str]:
        return ["post_job"]


class UpworkIntegration(BaseIntegration):
    """
    Upwork freelancer/job integration.
    Auth: OAuth2 bearer token.
    """

    BASE_URL = "https://www.upwork.com/api/v3"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/profiles/v1/me",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Upwork validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "post_job":
            return await self._post_job(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _post_job(self, params: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "title": params.get("title", ""),
            "description": params.get("description", ""),
            "budget": params.get("budget"),
            "category2": params.get("category", ""),
            "subcategory2": params.get("subcategory", ""),
            "visibility": params.get("visibility", "public"),
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/hr/v4/postings",
                headers=self._headers(),
                json=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": "success", "job_id": data.get("reference", "")}

    @property
    def capabilities(self) -> List[str]:
        return ["post_job"]


# Export
__all__ = [
    "MetaSocialIntegration",
    "LinkedInSocialIntegration",
    "TikTokIntegration",
    "IndeedIntegration",
    "UpworkIntegration",
]
