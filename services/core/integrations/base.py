from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel, Field

class IntegrationConfig(BaseModel):
    """Configuration for an integration instance."""
    name: str
    platform: str  # e.g., 'hubspot', 'twitter', 'stripe'
    enabled: bool = True
    credentials: Dict[str, Any] = Field(default_factory=dict)
    secret_key: Optional[str] = None # Key for SecretManager if using central storage

class BaseIntegration(ABC):
    """Abstract base class for all external integrations."""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.logger = None # Should be initialized by subclasses or dependency injection
        
    @property
    def name(self) -> str:
        return self.config.name

    @property
    def platform(self) -> str:
        return self.config.platform

    @abstractmethod
    async def validate_connection(self) -> bool:
        """Check if credentials are valid and service is reachable."""
        pass
    
    @abstractmethod
    async def execute_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        """Execute a specific action provided by this integration."""
        pass
        
    @property
    def capabilities(self) -> List[str]:
        """List of capabilities this integration provides (e.g. 'post_tweet', 'read_email')."""
        return []

    @property
    def metadata(self) -> Dict[str, Any]:
        """Return metadata about this integration."""
        return {
            "name": self.name,
            "platform": self.platform,
            "capabilities": self.capabilities,
            "enabled": self.config.enabled
        }

class IntegrationRegistry:
    _registry: Dict[str, Type[BaseIntegration]] = {}
    _instances: Dict[str, BaseIntegration] = {}

    @classmethod
    def register(cls, name: str, integration_cls: Type[BaseIntegration]):
        cls._registry[name] = integration_cls

    @classmethod
    def get_class(cls, name: str) -> Optional[Type[BaseIntegration]]:
        return cls._registry.get(name)

    @classmethod
    def list_integrations(cls) -> List[str]:
        return list(cls._registry.keys())
        
    @classmethod
    def initialize_integration(cls, name: str, config: IntegrationConfig) -> BaseIntegration:
        if name not in cls._registry:
            raise ValueError(f"Integration '{name}' not registered.")
        
        instance = cls._registry[name](config)
        cls._instances[name] = instance
        return instance
        
    @classmethod
    def get_instance(cls, name: str) -> Optional[BaseIntegration]:
        return cls._instances.get(name)

    @classmethod
    def list_instances(cls) -> List[str]:
        return list(cls._instances.keys())
