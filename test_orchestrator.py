import asyncio
from services.core.agents.orchestrator import OrchestratorAgent
from services.core.agents.base import AgentConfig
import json

async def run_test():
    config = AgentConfig(name="OrchestratorAgent", description="Test")
    agent = OrchestratorAgent(config)
    result = await agent.run({"goal": "Say hello!"}, context={"user_id": "test_user"})
    print("TASK STATUS:", result.status)
    print("DATA RESPONSE:", result.data.get("response"))

if __name__ == "__main__":
    asyncio.run(run_test())
