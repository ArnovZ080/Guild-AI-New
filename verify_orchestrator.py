import asyncio
import sys
import os
import json

sys.path.append(os.getcwd())

from services.core.agents.registry import AgentRegistry
from services.core.agents.orchestrator import OrchestratorAgent, AgentConfig
# Import others to register them
import services.core.agents.research
import services.core.agents.content
from services.core.llm import default_llm
from unittest.mock import AsyncMock

async def main():
    print("Initializing Orchestrator Agent...")
    
    # MOCK THE LLM
    # We need to mock the plan generation
    mock_plan = {
        "tasks": [
            {
                "id": "task_1",
                "description": "Research the future of AI agents",
                "assigned_agent": "ResearchAgent",
                "dependencies": []
            },
            {
                "id": "task_2",
                "description": "Create content based on research",
                "assigned_agent": "ContentStrategistAgent",
                "dependencies": ["task_1"]
            }
        ]
    }
    
    default_llm.chat_completion = AsyncMock(side_effect=[
        json.dumps(mock_plan), # First call: Orchestrator plan
        "Research complete: AI agents are taking over.", # Second call: ResearchAgent (summarize)
        json.dumps({"strategy_summary": "Great content", "content_calendar": []}) # Third call: ContentStrategist
    ])
    
    config = AgentConfig(
        name="boss",
        description="The boss",
    )
    agent = OrchestratorAgent(config)
    
    goal = "Create a content strategy for a blog post about 'The Future of AI Agents in 2026'. First research the topic, then create the strategy."
    
    print(f"Goal: {goal}")
    print("-" * 50)
    
    try:
        # Run the orchestrator
        # The process method returns {plan, results}
        output = await agent.run({"goal": goal})
        
        print("\n\nExecution Complete!")
        print("=" * 50)
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
