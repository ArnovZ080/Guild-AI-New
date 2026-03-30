"""
CRM Connectors.
Real API implementations for Salesforce, Asana, Trello, Monday, and Jira.
"""
import logging
import httpx
from typing import Dict, Any, List, Optional
from services.core.integrations.base import BaseIntegration, IntegrationConfig

logger = logging.getLogger(__name__)


class SalesforceIntegration(BaseIntegration):
    """
    Salesforce CRM integration.
    Auth: OAuth2 Bearer token. Requires instance_url + access_token in credentials.
    """

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.instance_url = self.config.credentials.get("instance_url", "")
        self.access_token = self.config.credentials.get("access_token", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def validate_connection(self) -> bool:
        if not self.instance_url or not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.instance_url}/services/data/",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Salesforce validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_lead":
            return await self._create_lead(params)
        elif action_name == "update_opportunity":
            return await self._update_opportunity(params)
        elif action_name == "fetch_account":
            return await self._fetch_account(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _create_lead(self, params: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.instance_url}/services/data/v58.0/sobjects/Lead/",
                headers=self._headers(),
                json=params,
                timeout=15.0,
            )
            resp.raise_for_status()
            return resp.json()

    async def _update_opportunity(self, params: Dict[str, Any]) -> Dict[str, Any]:
        opp_id = params.pop("opp_id", None)
        if not opp_id:
            raise ValueError("opp_id required")
        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{self.instance_url}/services/data/v58.0/sobjects/Opportunity/{opp_id}",
                headers=self._headers(),
                json=params,
                timeout=15.0,
            )
            resp.raise_for_status()
            return {"status": "success", "opp_id": opp_id}

    async def _fetch_account(self, params: Dict[str, Any]) -> Dict[str, Any]:
        account_id = params.get("account_id")
        if not account_id:
            raise ValueError("account_id required")
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.instance_url}/services/data/v58.0/sobjects/Account/{account_id}",
                headers=self._headers(),
                timeout=10.0,
            )
            resp.raise_for_status()
            return resp.json()

    @property
    def capabilities(self) -> List[str]:
        return ["create_lead", "update_opportunity", "fetch_account"]


class AsanaIntegration(BaseIntegration):
    """
    Asana project management integration.
    Auth: Bearer token (Personal Access Token or OAuth2).
    """

    BASE_URL = "https://app.asana.com/api/1.0"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/users/me",
                    headers=self._headers(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Asana validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_task":
            return await self._create_task(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _create_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/tasks",
                headers=self._headers(),
                json={"data": params},
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": "success", "task_id": data["data"]["gid"]}

    @property
    def capabilities(self) -> List[str]:
        return ["create_task"]


class TrelloIntegration(BaseIntegration):
    """
    Trello board management integration.
    Auth: API key + token (query params).
    """

    BASE_URL = "https://api.trello.com/1"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.api_key = self.config.credentials.get("api_key", "")
        self.token = self.config.credentials.get("token", "")

    def _auth_params(self) -> Dict[str, str]:
        return {"key": self.api_key, "token": self.token}

    async def validate_connection(self) -> bool:
        if not self.api_key or not self.token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/members/me",
                    params=self._auth_params(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Trello validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "add_card":
            return await self._add_card(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _add_card(self, params: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            payload = {**self._auth_params(), **params}
            resp = await client.post(
                f"{self.BASE_URL}/cards",
                params=payload,
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": "success", "card_id": data["id"]}

    @property
    def capabilities(self) -> List[str]:
        return ["add_card"]


class MondayIntegration(BaseIntegration):
    """
    Monday.com project management integration.
    Auth: Bearer token. Uses GraphQL API.
    """

    BASE_URL = "https://api.monday.com/v2"

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.access_token = self.config.credentials.get("access_token", "")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": self.access_token,
            "Content-Type": "application/json",
        }

    async def validate_connection(self) -> bool:
        if not self.access_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.BASE_URL,
                    headers=self._headers(),
                    json={"query": "{ me { id name } }"},
                    timeout=10.0,
                )
                return resp.status_code == 200 and "data" in resp.json()
        except Exception as e:
            logger.error(f"Monday validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "update_board":
            return await self._update_board(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _update_board(self, params: Dict[str, Any]) -> Dict[str, Any]:
        board_id = params.get("board_id")
        column_values = params.get("column_values", "{}")
        item_name = params.get("item_name", "New Item")

        mutation = f'''
        mutation {{
            create_item(
                board_id: {board_id},
                item_name: "{item_name}",
                column_values: "{column_values}"
            ) {{ id }}
        }}
        '''
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.BASE_URL,
                headers=self._headers(),
                json={"query": mutation},
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            item_id = data.get("data", {}).get("create_item", {}).get("id")
            return {"status": "success", "board_id": board_id, "item_id": item_id}

    @property
    def capabilities(self) -> List[str]:
        return ["update_board"]


class JiraIntegration(BaseIntegration):
    """
    Jira project tracking integration.
    Auth: Basic Auth (email + API token). Requires domain in credentials.
    """

    def __init__(self, config: IntegrationConfig):
        super().__init__(config)
        self.domain = self.config.credentials.get("domain", "")
        self.email = self.config.credentials.get("email", "")
        self.api_token = self.config.credentials.get("api_token", "")
        self.base_url = f"https://{self.domain}.atlassian.net/rest/api/3" if self.domain else ""

    def _auth(self) -> httpx.BasicAuth:
        return httpx.BasicAuth(self.email, self.api_token)

    async def validate_connection(self) -> bool:
        if not self.domain or not self.email or not self.api_token:
            return False
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.base_url}/myself",
                    auth=self._auth(),
                    timeout=10.0,
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Jira validation failed: {e}")
            return False

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_issue":
            return await self._create_issue(params)
        raise ValueError(f"Unknown action {action_name}")

    async def _create_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        project_key = params.get("project_key", "PROJ")
        summary = params.get("summary", "")
        issue_type = params.get("issue_type", "Task")

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": issue_type},
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"text": params.get("description", ""), "type": "text"}
                            ],
                        }
                    ],
                },
            }
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/issue",
                auth=self._auth(),
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"status": "success", "issue_key": data["key"]}

    @property
    def capabilities(self) -> List[str]:
        return ["create_issue"]


# Export
__all__ = [
    "SalesforceIntegration",
    "AsanaIntegration",
    "TrelloIntegration",
    "MondayIntegration",
    "JiraIntegration",
]
