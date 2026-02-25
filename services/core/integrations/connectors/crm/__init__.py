from typing import Dict, Any, List
from services.core.integrations.base import BaseIntegration, IntegrationConfig

class SalesforceIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_lead":
            return {"status": "success", "lead_id": "LD-123"}
        elif action_name == "update_opportunity":
            return {"status": "success", "opp_id": params.get("opp_id")}
        elif action_name == "fetch_account":
            return {"status": "success", "account": {"name": "Test Co"}}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["create_lead", "update_opportunity", "fetch_account"]

class AsanaIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_task":
            return {"status": "success", "task_id": "TSK-1"}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["create_task"]

class TrelloIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "add_card":
            return {"status": "success", "card_id": "CRD-1"}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["add_card"]

class MondayIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "update_board":
            return {"status": "success", "board_id": "BRD-1"}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["update_board"]

class JiraIntegration(BaseIntegration):
    def __init__(self, config: IntegrationConfig):
        super().__init__(config)

    async def validate_connection(self) -> bool:
        return True
        
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        if action_name == "create_issue":
            return {"status": "success", "issue_key": "PROJ-123"}
        raise ValueError(f"Unknown action {action_name}")

    @property
    def capabilities(self) -> List[str]:
        return ["create_issue"]

# Export
__all__ = [
    "SalesforceIntegration",
    "AsanaIntegration",
    "TrelloIntegration",
    "MondayIntegration",
    "JiraIntegration"
]
