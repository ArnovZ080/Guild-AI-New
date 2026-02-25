import json
import os
from typing import Dict, Any
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.logging import logger

class LegacyBridge:
    """
    Bridges the legacy 120-agent workforce into the new architecture.
    """
    @staticmethod
    def import_legacy_registry(registry_path: str):
        if not os.path.exists(registry_path):
            logger.error(f"Legacy registry path not found: {registry_path}")
            return
            
        try:
            with open(registry_path, 'r') as f:
                data = json.load(f)
                
            agents = data.get("agents", [])
            logger.info(f"Importing {len(agents)} agents from legacy registry...")
            
            for agent_data in agents:
                LegacyBridge._register_agent(agent_data)
                
            logger.info("Legacy registry import complete.")
            
        except Exception as e:
            logger.error(f"Failed to import legacy registry: {e}")

    @staticmethod
    def scan_codebase_for_agents(search_path: str):
        """
        Scans the legacy codebase for agent classes defined in python files.
        As requested, this ensures we find agents scattered outside the main registry.
        """
        import re
        logger.info(f"Scanning {search_path} for scattered agents...")
        
        # Pattern to find class definitions like "class BookkeepingAgent(BaseAgent):"
        agent_pattern = re.compile(r"class (\w+Agent)\((BaseAgent|Agent|AgentTemplate)\):")
        
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r') as f:
                            content = f.read()
                            matches = agent_pattern.findall(content)
                            for class_name, base_class in matches:
                                # Convert CamelCase to snake_case for agent_id
                                agent_id = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
                                
                                # Check if already registered
                                if AgentRegistry.get(agent_id):
                                    continue
                                    
                                logger.info(f"Found scattered agent: {class_name} in {file}")
                                
                                # Basic metadata for scattered agents
                                agent_data = {
                                    "agent_id": agent_id,
                                    "name": class_name.replace("Agent", " Agent"),
                                    "description": f"Legacy {class_name} discovered in {file}.",
                                    "category": "legacy_scanned",
                                    "file_name": file.replace(".py", ""),
                                    "capabilities": ["legacy_capability"]
                                }
                                LegacyBridge._register_agent(agent_data)
                    except Exception as e:
                        logger.warning(f"Could not read {full_path}: {e}")

    @staticmethod
    def _register_agent(agent_data: Dict[str, Any]):
        """Helper to standardize and register an agent with Education/Transparency metadata."""
        category = agent_data.get("category", "general")
        description = agent_data.get("description", "")
        agent_id = agent_data.get("agent_id") or agent_data.get("name")
        
        # Transparency & Education synthesis
        educational_context = (
            f"This agent specializes in {category}. By observing its actions, you can learn how "
            f"professional {category} systems handle {', '.join(agent_data.get('capabilities', [])[:2])}."
        )
        process_description = (
            f"Action Protocol: 1. Parse business context 2. Cross-reference {category} standards "
            f"3. Execute optimized logic for '{description[:40]}...'"
        )
        
        capability = AgentCapability(
            name=agent_id,
            category=category,
            capabilities=agent_data.get("capabilities", []),
            description=description,
            educational_context=educational_context,
            process_description=process_description,
            trust_score=0.9,
            success_rate=1.0,
            avg_completion_time=0.0,
            resource_efficiency=1.0,
            revision_rate=0.0,
            metadata={
                "legacy_id": agent_id,
                "icon": agent_data.get("icon", "🤖"),
                "file_name": agent_data.get("file_name"),
                "type": agent_data.get("type", "class_based"),
                "is_legacy": True
            }
        )
        
        AgentRegistry.register(capability)

# Example usage (to be called during initialization)
# bridge = LegacyBridge()
# bridge.import_legacy_registry("/Users/arnovanzyl/Dropbox/Mac (2)/Documents/GitHub/Guild-AI/backend/src/agents/comprehensive_registry.json")
