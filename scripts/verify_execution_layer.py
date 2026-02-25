import asyncio
import json
import logging
from typing import Dict, Any
from services.core.agents.executor import ExecutorAgent
from services.core.agents.secrets import SecretManager
from services.core.agents.models import DelegationSpec, TaskStatus
from services.core.integrations.base import IntegrationRegistry, BaseIntegration, IntegrationConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verify_execution")

# 1. Create a Mock Integration for testing
class MockCRMIntegration(BaseIntegration):
    @property
    def capabilities(self):
        return ["get_contacts", "create_contact"]

    async def validate_connection(self) -> bool:
        return True

    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        logger.info(f"Mocking execution of {action_name} with params: {params}")
        if action_name == "create_contact":
            return {"id": "mock_id_123", "email": params.get("email"), "status": "created"}
        return {"status": "success"}

# Register the mock integration
IntegrationRegistry.register("mock_crm", MockCRMIntegration)

async def run_verification():
    logger.info("--- Starting Execution Layer Verification ---")
    
    # Initialize components
    secret_manager = SecretManager("/Users/arnovanzyl/.gemini/antigravity/scratch/data/test_secrets")
    executor = ExecutorAgent("executor_test", secret_manager)
    
    # 2. Test Secret Storage
    logger.info("Test Step 1: Secret Storage")
    secret_manager.store_secret("mock_crm", {"api_key": "test_key_123"})
    assert "mock_crm" in secret_manager.list_keys()
    logger.info("✓ Secret Storage successful.")
    
    # 3. Test Autonomous Execution via Executor
    logger.info("Test Step 2: Autonomous Execution")
    spec = DelegationSpec(
        id="task_1",
        intent='mock_crm.create_contact: {"email": "test@example.com", "name": "John Doe"}',
        assigned_agent="executor_test",
        rationale="Testing autonomous execution loop."
    )
    
    result = await executor.process(spec)
    
    logger.info(f"Result Status: {result.status}")
    logger.info(f"Result Data: {result.data}")
    logger.info(f"Process Log: {result.process_log}")
    
    assert result.status == TaskStatus.COMPLETED
    assert result.data["id"] == "mock_id_123"
    assert "Successfully executed create_contact on mock_crm" in result.process_log[-1]
    logger.info("✓ Autonomous Execution successful.")
    
    # 4. Test Error Handling (Invalid platform)
    logger.info("Test Step 3: Error Handling (Missing Connection)")
    spec_fail = DelegationSpec(
        id="task_2",
        intent='invalid_platform.action: {}',
        assigned_agent="executor_test",
        rationale="Testing error handling for missing platform."
    )
    result_fail = await executor.process(spec_fail)
    assert result_fail.status == TaskStatus.FAILED
    assert "I couldn't find an active connection for invalid_platform" in result_fail.educational_takeaway
    logger.info("✓ Error Handling (Missing Connection) successful.")

    logger.info("--- Verification Completed Successfully ---")

if __name__ == "__main__":
    asyncio.run(run_verification())
