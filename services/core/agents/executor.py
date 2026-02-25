import logging
import asyncio
import json
from typing import Dict, Any, List, Optional
from .base import BaseAgent, AgentConfig
from .models import TaskResult, TaskStatus, DelegationSpec, AuthorizationRequest
from ..integrations.base import IntegrationRegistry, IntegrationConfig
from ..integrations.oauth import OAuthService
from .secrets import SecretManager
from ..integrations.social_bridge import SocialBridge
from ..integrations.crm_bridge import CRMBridge
from ..integrations.calendar_bridge import CalendarBridge
from ..security.auth_service import HumanAuthorizationService

logger = logging.getLogger(__name__)

class ExecutorAgent(BaseAgent):
    """
    The "Hands" of the system.
    Responsible for executing specific, tool-based tasks delegated by the Orchestrator.
    Manages integration lifecycle and autonomous action dispatching.
    """
    
    def __init__(self, agent_id: str, secret_manager: SecretManager):
        config = AgentConfig(
            name="Executor",
            description="Autonomously executes tasks via external integrations."
        )
        super().__init__(config)
        self.agent_id = agent_id
        self.secret_manager = secret_manager
        self.oauth_service = OAuthService(secret_manager)
        self.active_auth_requests: Dict[str, AuthorizationRequest] = {}

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> TaskResult:
        """
        Execute a delegated task by identifying the appropriate integration and action.
        """
        if not isinstance(input_data, DelegationSpec):
            return TaskResult(
                data=None,
                status=TaskStatus.FAILED,
                process_log=["Invalid input data. Expected DelegationSpec."],
                educational_takeaway="I received an invalid task format."
            )

        spec = input_data
        self.logger.info(f"Received execution task: {spec.intent}")
        process_log = [f"Executor initiated: Analyzing intent '{spec.intent}'"]
        
        try:
            parts = spec.intent.split(":", 1)
            if len(parts) < 2:
                process_log.append("Failed to identify action: Intent format invalid.")
                return TaskResult(
                    data=None,
                    status=TaskStatus.FAILED,
                    process_log=process_log,
                    educational_takeaway="I couldn't identify the specific action to perform from your request."
                )
            
            action_identifier = parts[0].strip()
            action_params_raw = parts[1].strip()
            
            action_parts = action_identifier.split(".")
            if len(action_parts) != 2:
                process_log.append(f"Failed to parse action identifier: {action_identifier}")
                return TaskResult(
                    data=None,
                    status=TaskStatus.FAILED,
                    process_log=process_log,
                    educational_takeaway=f"Invalid action format '{action_identifier}'. Expected 'platform.action'."
                )
            
            platform, action_name = action_parts
            
            # 1. Check if it's a Bridge (Category) action
            if platform == "financial":
                params = json.loads(action_params_raw) if action_params_raw.startswith("{") else {}
                if HumanAuthorizationService.should_require_approval("financial", params):
                    req_id = HumanAuthorizationService.create_request(
                        task_id=spec.id,
                        agent_id=self.agent_id,
                        action_type="financial",
                        description=f"Action: {action_name} on {platform}",
                        params=params
                    )
                    process_log.append(f"Financial action BLOCKED. Approval required (Request ID: {req_id}).")
                    return TaskResult(
                        status=TaskStatus.BLOCKED,
                        data={"auth_request_id": req_id},
                        process_log=process_log,
                        educational_takeaway="This financial action exceeds your safety threshold and requires manual approval in the Executive Review Dashboard."
                    )

            if platform == "social":
                process_log.append("Routing to SocialBridge...")
                return await SocialBridge.post_content(action_params_raw) if action_name == "post_content" else await SocialBridge.get_unified_analytics()
            elif platform == "crm":
                process_log.append("Routing to CRMBridge...")
                params = json.loads(action_params_raw) if action_params_raw.startswith("{") else {}
                return await CRMBridge.sync_contact(params) if action_name == "sync_contact" else await CRMBridge.update_deal(params)
            elif platform == "calendar":
                process_log.append("Routing to CalendarBridge...")
                params = json.loads(action_params_raw) if action_params_raw.startswith("{") else {}
                return await CalendarBridge.schedule_event(params) if action_name == "schedule_event" else await CalendarBridge.get_daily_agenda()

            # 2. Get/Initialize Specific Integration
            integration = await self._get_integration_instance(platform, process_log)
            if not integration:
                process_log.append(f"Connection missing for platform: {platform}")
                return TaskResult(
                    data=None,
                    status=TaskStatus.FAILED,
                    process_log=process_log,
                    educational_takeaway=f"I couldn't find an active connection for {platform}. Please visit the Integration Hub to set it up."
                )

            # 4. Execute Action
            process_log.append(f"Executing {action_name} on {platform}...")
            
            try:
                params = json.loads(action_params_raw)
            except:
                params = {"content": action_params_raw} if action_name == "post_content" else {}

            result_data = await integration.execute_action(action_name, params)
            
            process_log.append(f"Successfully executed {action_name} on {platform}.")
            
            return TaskResult(
                data=result_data,
                status=TaskStatus.COMPLETED,
                process_log=process_log,
                educational_takeaway=f"I've successfully performed the '{action_name}' action on {platform} as requested."
            )

        except Exception as e:
            self.logger.error(f"Execution error: {e}")
            process_log.append(f"Execution failed: {str(e)}")
            return TaskResult(
                data=None,
                status=TaskStatus.FAILED,
                process_log=process_log,
                educational_takeaway=f"I encountered an error while trying to execute the task: {str(e)}"
            )

    async def _get_integration_instance(self, platform: str, process_log: List[str]):
        """Retrieve an active integration instance or initialize if secrets/tokens are available."""
        instance = IntegrationRegistry.get_instance(platform)
        if instance:
            return instance
        
        # 1. Try OAuth token first
        access_token = await self.oauth_service.get_valid_access_token(platform)
        if access_token:
            process_log.append(f"Initializing {platform} integration via OAuth...")
            config = IntegrationConfig(
                name=f"{platform}_oauth",
                platform=platform,
                credentials={"api_key": access_token}
            )
            return IntegrationRegistry.initialize_integration(platform, config)

        # 2. Fallback to static secrets
        secrets = self.secret_manager.get_secret(platform)
        if secrets:
            process_log.append(f"Initializing {platform} integration from stored secrets...")
            config = IntegrationConfig(
                name=f"{platform}_default",
                platform=platform,
                credentials=secrets
            )
            return IntegrationRegistry.initialize_integration(platform, config)
            
        return None
