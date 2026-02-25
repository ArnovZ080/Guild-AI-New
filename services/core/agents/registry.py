from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass
class AgentCapability:
    name: str
    category: str
    capabilities: List[str]
    description: str
    educational_context: str = "" # Explains "why" this agent exists and what the user can learn
    process_description: str = ""   # Explains "how" the agent performs its tasks step-by-step
    agent_class: Optional[type] = None
    trust_score: float = 1.0  
    success_rate: float = 1.0 
    avg_completion_time: float = 0.0 
    resource_efficiency: float = 1.0 
    revision_rate: float = 0.0 
    performance_history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class AgentRegistry:
    _registry: Dict[str, AgentCapability] = {}

    @classmethod
    def register(cls, capability: AgentCapability, agent_class: type = None):
        if agent_class:
            capability.agent_class = agent_class
        cls._registry[capability.name] = capability

    @classmethod
    def get(cls, name: str) -> Optional[AgentCapability]:
        return cls._registry.get(name)

    @classmethod
    def list_all(cls) -> List[AgentCapability]:
        return list(cls._registry.values())

    @classmethod
    def list_by_category(cls, category: str) -> List[AgentCapability]:
        return [cap for cap in cls._registry.values() if cap.category == category]

    @classmethod
    def get_description_map(cls) -> str:
        """Returns a string summary of all agents for LLM planning context."""
        return "\n".join([f"- {c.name} ({c.category}): {c.description}" for c in cls._registry.values()])
