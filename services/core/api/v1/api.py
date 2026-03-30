from fastapi import APIRouter

from services.core.api.v1.endpoints import (
    auth, chat, agents, dashboard, events,
    workflows, projects, integrations, learning
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
