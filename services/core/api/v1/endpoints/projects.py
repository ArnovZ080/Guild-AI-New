from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.api import deps
from services.core.api.schemas import ProjectCreate, ProjectResponse
from services.core.db.models import UserAccount, Project

router = APIRouter()

@router.post("", response_model=ProjectResponse)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """Create a new project."""
    db_project = Project(user_id=current_user.id, goal=project_in.goal)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("")
async def list_projects(
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """List all projects for the current user."""
    result = await db.execute(
        select(Project).where(Project.user_id == current_user.id)
    )
    projects = result.scalars().all()
    return {
        "projects": [
            {"id": p.id, "goal": p.goal, "status": p.status, "created_at": str(p.created_at)}
            for p in projects
        ]
    }

@router.get("/{project_id}")
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(deps.get_db),
    current_user: UserAccount = Depends(deps.get_current_active_user),
) -> Any:
    """Get a specific project by ID."""
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalars().first()
    if not project:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Project not found")
    return {"id": project.id, "goal": project.goal, "status": project.status, "created_at": str(project.created_at)}
