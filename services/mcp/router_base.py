from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Callable

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class MCPRouter(APIRouter):
    """
    Extensions to APIRouter to support MCP tool discovery.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tools: List[ToolDefinition] = []

    def tool(self, name: str, description: str):
        """Decorator to register a function as an MCP tool endpoint"""
        def decorator(func: Callable):
            # Register the route normally
            self.post(f"/tools/{name}", name=name, description=description)(func)
            
            # Extract parameters from Pydantic model in the function signature if possible
            # For now, we manually register metadata or infer it later.
            self.tools.append(ToolDefinition(
                name=name,
                description=description,
                parameters={} # TODO: Introspect Pydantic schema
            ))
            return func
        return decorator
