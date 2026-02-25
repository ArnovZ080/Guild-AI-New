import sys
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add source root to path
sys.path.append(os.getcwd())

from services.core.agents.registry import AgentRegistry
from services.core.bridge import scan_and_register_legacy_agents, LegacyAgentAdapter

async def main():
    logger.info("Starting Legacy Bridge Verification...")
    
    # 1. Register agents
    scan_and_register_legacy_agents()
    
    # 2. Check Registry
    marketing_cap = AgentRegistry.get("MarketingAgent")
    if not marketing_cap:
        logger.error("MarketingAgent not found in registry!")
        return
    
    logger.info(f"Found MarketingAgent in registry: {marketing_cap}")
    
    # 3. Instantiate Agent
    try:
        from services.core.agents.base import AgentConfig
        agent_config = AgentConfig(
            name=marketing_cap.name,
            capability=marketing_cap.category, # Using category as capability grouping
            description=marketing_cap.description,
            metadata=marketing_cap.metadata
        )
        # adapter = LegacyAgentAdapter(agent_config) # AgentRegistry usually handles this factories? 
        # But AgentRegistry.create_agent(name) is the way.
        
        # Let's verify we can create the adapter manually first or via registry helper if it exists
        # Inspecting Registry... assuming `create_agent` or we do it manually.
        
        adapter = LegacyAgentAdapter(agent_config)
        logger.info(f"Successfully instantiated LegacyAgentAdapter for {adapter.legacy_class_name}")
        
        if adapter.legacy_agent_instance:
            logger.info("Legacy agent instance is ready.")
            logger.info(f"Legacy agent type: {type(adapter.legacy_agent_instance)}")
        else:
            logger.error("Legacy agent instance is None!")
            
    except Exception as e:
        logger.error(f"Failed to instantiate agent: {e}", exc_info=True)
        return

    logger.info("Verification Complete: Bridge is working for instantiation.")

if __name__ == "__main__":
    asyncio.run(main())
