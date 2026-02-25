from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from services.core.integrations.base import IntegrationRegistry, IntegrationConfig
from services.core.agents.secrets import SecretManager

router = APIRouter(prefix="/integrations", tags=["integrations"])
secret_manager = SecretManager()

class ConnectionRequest(BaseModel):
    platform: str
    credentials: Dict[str, Any]
    name: Optional[str] = None

class IntegrationMetadata(BaseModel):
    name: str
    platform: str
    capabilities: List[str]
    enabled: bool
    is_connected: bool

@router.get("/", response_model=List[IntegrationMetadata])
async def list_integrations():
    """List all available integrations and their connection status."""
    available = IntegrationRegistry.list_integrations()
    keys = secret_manager.list_keys()
    
    results = []
    for platform in available:
        # Check if connected via static secret or OAuth
        is_connected = platform in keys or f"oauth_{platform}" in keys
        
        results.append(IntegrationMetadata(
            name=f"{platform.capitalize()} Integration",
            platform=platform,
            capabilities=["generic_action"], # Placeholder
            enabled=True,
            is_connected=is_connected
        ))
    
    return results

@router.post("/connect")
async def connect_integration(request: ConnectionRequest):
    """Store credentials and initialize an integration."""
    if request.platform not in IntegrationRegistry.list_integrations():
        raise HTTPException(status_code=404, detail=f"Platform {request.platform} not supported.")
    
    # Store in SecretManager
    secret_manager.store_secret(request.platform, request.credentials)
    
    # Try to initialize and validate
    try:
        config = IntegrationConfig(
            name=request.name or f"{request.platform}_default",
            platform=request.platform,
            credentials=request.credentials
        )
        instance = IntegrationRegistry.initialize_integration(request.platform, config)
        is_valid = await instance.validate_connection()
        
        if not is_valid:
            # We still keep the secret, but inform the user
            return {"status": "connected_with_warnings", "message": "Credentials stored, but validation failed."}
            
        return {"status": "success", "message": f"Successfully connected to {request.platform}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize integration: {str(e)}")

@router.post("/test/{platform}")
async def test_connection(platform: str):
    """Verify an existing connection."""
    instance = IntegrationRegistry.get_instance(platform)
    if not instance:
        # Try to re-initialize from secrets
        secrets = secret_manager.get_secret(platform)
        if not secrets:
            raise HTTPException(status_code=404, detail="No connection found for this platform.")
        
        config = IntegrationConfig(
            name=f"{platform}_default",
            platform=platform,
            credentials=secrets
        )
        instance = IntegrationRegistry.initialize_integration(platform, config)

    is_valid = await instance.validate_connection()
    return {"platform": platform, "is_valid": is_valid}

@router.delete("/{platform}")
async def disconnect_integration(platform: str):
    """Remove a connection."""
    secret_manager.delete_secret(platform)
    # Also remove from active instances if possible
    # (IntegrationRegistry would need a way to remove instances)
    return {"status": "success", "message": f"Disconnected {platform}."}
