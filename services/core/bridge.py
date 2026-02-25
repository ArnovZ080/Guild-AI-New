import sys
import os
import importlib
import inspect
import logging
from typing import Any, Dict, Optional, List

# Add legacy root to path so imports work
LEGACY_ROOT = "/Users/arnovanzyl/Dropbox/Mac (2)/Documents/GitHub/Guild-AI"
logger = logging.getLogger(__name__)

if LEGACY_ROOT not in sys.path:
    sys.path.append(LEGACY_ROOT)

try:
    import requests
except ImportError:
    from unittest.mock import MagicMock
    sys.modules["requests"] = MagicMock()
    logger.warning("Mocked 'requests' module to allow legacy agent import.")

from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability

class LegacyAgentAdapter(BaseAgent):
    """
    Adapter to run legacy Guild AI agents within the new architecture.
    Wraps the legacy agent class and maps the interface.
    """
    
    def __init__(self, config: AgentConfig = None):
        super().__init__(config)
        
        if config and config.metadata:
            self.legacy_class_name = config.metadata.get("legacy_class_name")
            self.legacy_module_path = config.metadata.get("legacy_module_path")
        else:
            self.legacy_class_name = None
            self.legacy_module_path = None
        
        self.legacy_agent_instance = None

        if self.legacy_class_name and self.legacy_module_path:
            self._initialize_legacy_agent()

    def _initialize_legacy_agent(self):
        """Dynamically import and instantiate the legacy agent."""
        try:
            module = importlib.import_module(self.legacy_module_path)
            agent_class = getattr(module, self.legacy_class_name)
            
            # Legacy agents usually take optional user_input in init
            # Many legacy agents look like: def __init__(self, user_input=None):
            # We instantiate with None to ready it for run()
            self.legacy_agent_instance = agent_class(user_input=None)
            logger.info(f"Successfully initialized legacy agent: {self.legacy_class_name}")
            
        except ImportError as e:
            logger.error(f"Failed to import legacy module {self.legacy_module_path}: {e}")
            raise
        except AttributeError as e:
            logger.error(f"Failed to find class {self.legacy_class_name} in {self.legacy_module_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to instantiate legacy agent {self.legacy_class_name}: {e}")
            raise

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        """
        Adapts the 'process' call to the legacy 'run' method.
        """
        if not self.legacy_agent_instance:
             return {"status": "error", "message": "Legacy agent instance not initialized"}
        
        try:
            # Map input_data to user_input string or pass as is if the agent supports it
            # Typically legacy run(self, user_input: str = None)
            user_input = input_data.get("user_input") or input_data.get("command") or str(input_data)
            
            # Call the legacy run method
            run_method = getattr(self.legacy_agent_instance, "run", None)
            if not run_method:
                return {"status": "error", "message": f"Legacy agent {self.legacy_class_name} has no 'run' method"}

            if inspect.iscoroutinefunction(run_method):
                result = await run_method(user_input=user_input)
            else:
                result = run_method(user_input=user_input)
            
            return result
            
        except Exception as e:
            logger.error(f"Error running legacy agent {self.legacy_class_name}: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

def register_legacy_agent(name: str, module_path: str, class_name: str, capabilities: List[str], description: str):
    """
    Helper to manually register a legacy agent in the new Registry.
    """
    AgentRegistry.register(AgentCapability(
        name=name,
        category="Legacy",
        capabilities=capabilities,
        description=f"[Legacy] {description}",
        agent_class=LegacyAgentAdapter,
        metadata={
            "legacy_module_path": module_path,
            "legacy_class_name": class_name,
            "is_legacy": True
        }
    ))

def scan_and_register_legacy_agents():
    """
    Scans the legacy agents directory (heuristic) and registers known patterns.
    Currently registers a manual list for safety.
    """
    logger.info(f"Registering legacy agents...")
    
    # Manual list of validated agents to bridge
    # Format: (Name, Module Path, Class Name, Capabilities, Description)
    legacy_agents = [
        ("MarketingAgent", "guild.src.agents.marketing_agent", "MarketingAgent", ["marketing_strategy"], "Strategic marketing planning."),
        ("SalesFunnelAgent", "guild.src.agents.sales_funnel_agent", "SalesFunnelAgent", ["sales_funnel"], "Sales funnel optimization."),
        ("CopywriterAgent", "guild.src.agents.copywriter_agent", "CopywriterAgent", ["copywriting"], "Ad copy and content generation."),
    ]

    for name, module, cls_name, caps, desc in legacy_agents:
        try:
            register_legacy_agent(name, module, cls_name, caps, desc)
            logger.info(f"Registered legacy agent: {name}")
        except Exception as e:
            logger.error(f"Failed to register legacy agent {name}: {e}")
