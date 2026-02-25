#!/usr/bin/env python3
"""
Verify Phase 15 implementation: Operations & HR agents
"""
import asyncio
import os
import sys

# Ensure the root of the project is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.core.agents.registry import AgentRegistry

# Importing these will register them
from services.core.adk.operations import FinanceOperationsAgent, LegalComplianceAgent
from services.core.adk.hr import TalentAcquisitionAgent, TeamCultureAgent

async def verify():
    print("Verifying Phase 15 Agents...")
    
    expected_agents = [
        "FinanceOperationsAgent",
        "LegalComplianceAgent",
        "TalentAcquisitionAgent",
        "TeamCultureAgent"
    ]
    
    missing = []
    
    for agent_name in expected_agents:
        capability = AgentRegistry.get(agent_name)
        if not capability:
            print(f"❌ Missing agent: {agent_name}")
            missing.append(agent_name)
            continue
            
        print(f"✅ Found agent: {agent_name} ({capability.category})")
        print(f"   Capabilities: {', '.join(capability.capabilities)}")
        
        from services.core.agents.base import AgentConfig
        agent_instance = capability.agent_class(config=AgentConfig(name=agent_name, description="test"))
        
    if missing:
        print(f"\n❌ Phase 15 verification failed. {len(missing)} agents missing.")
        sys.exit(1)
        
    print("\n✅ All Phase 15 agents successfully integrated and registered.")

if __name__ == "__main__":
    asyncio.run(verify())
