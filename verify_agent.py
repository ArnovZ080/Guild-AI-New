import asyncio
import sys
import os

# Add current directory to path so we can import services
sys.path.append(os.getcwd())

from services.core.agents.registry import AgentRegistry
# Import the agent to trigger registration
from services.core.agents.research import ResearchAgent, AgentConfig

async def main():
    print("Initializing Research Agent...")
    config = AgentConfig(
        name="researcher",
        description="A test researcher",
        tools=["web_search"]
    )
    agent = ResearchAgent(config)
    
    print("Running research task...")
    try:
        result = await agent.run({"query": "What is the latest version of Python?"})
        print("\nResult:")
        print(result)
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main())
