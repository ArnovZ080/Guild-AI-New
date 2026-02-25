from fastapi import FastAPI
from services.core.logging import logger

# Import routers
from services.mcp.routes import ads, crm, seo

app = FastAPI(
    title="Guild AI MCP Service",
    description="Model Context Protocol service exposing core integrations as tools.",
    version="0.1.0"
)

app.include_router(ads.router, prefix="/mcp")
app.include_router(crm.router, prefix="/mcp")
app.include_router(seo.router, prefix="/mcp")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mcp-layer"}

@app.get("/mcp/tools")
async def list_tools():
    """
    List all available tools exposed by this service.
    This aggregates tools from all registered modules.
    """
    # TODO: Dynamic registration
    return {"tools": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
