from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.core.logging import logger
from services.core.config import settings
from services.core.security import SecurityMiddleware, SecurityHeadersMiddleware

from services.api.routes import agents, identity, integrations, oauth
from services.core.integrations.registry import register_all_connectors

app = FastAPI(
    title="Guild AI API",
    description="User-facing API for managing the Guild AI workforce.",
    version="0.1.0"
)

# Register all core integrations
register_all_connectors()

# Apply security headers first
app.add_middleware(SecurityHeadersMiddleware)

# Apply comprehensive security middleware
app.add_middleware(SecurityMiddleware)

app.include_router(agents.router)
app.include_router(identity.router)
app.include_router(integrations.router)
app.include_router(oauth.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-layer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # Port 8001 to avoid conflict with MCP (8000)
