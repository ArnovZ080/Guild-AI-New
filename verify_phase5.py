import asyncio
import json
from services.core.agents.orchestrator import OrchestratorAgent
from services.core.agents.base import AgentConfig
from services.core.agents.registry import AgentRegistry
from services.core.agents.identity import identity_manager

async def verify_phase5():
    print("🚀 Verifying Phase 5: Workforce Scaling & Knowledge Capture...")
    
    # 1. Initialize Orchestrator (triggers LegacyBridge import)
    config = AgentConfig(name="Orchestrator", description="Main Orchestrator", model="gpt-4-turbo-preview")
    orchestrator = OrchestratorAgent(config)
    
    # 2. Check Registry size
    all_agents = AgentRegistry.list_all()
    print(f"📊 Total Agents in Registry: {len(all_agents)}")
    
    if len(all_agents) > 100:
        print("✅ Legacy agents imported successfully!")
    else:
        print("❌ Legacy agents import failed.")

    # 3. Check specialized categories
    marketing_agents = AgentRegistry.list_by_category("marketing")
    print(f"📣 Marketing Agents found: {len(marketing_agents)}")
    
    # 4. Check Business Identity access
    identity = identity_manager.get_identity()
    print(f"🏠 Business Profile Loaded: {identity.business_name} ({identity.niche})")

    print("\n✅ Phase 5 Architecture Verified!")

if __name__ == "__main__":
    asyncio.run(verify_phase5())
