import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from services.core.logging import logger
from services.core.db.base import AsyncSessionLocal
from services.core.db.models import Project as DBProject, ProjectMilestone as DBMilestone
from services.core.agents.models import Project as PydanticProject, ProjectMilestone as PydanticMilestone, TaskStatus

class ProjectManager:
    """
    Manages long-running (30/60/90 day) growth roadmaps using PostgreSQL.
    """
    @classmethod
    async def create_project(cls, db: Optional[AsyncSession], user_id: str, business_id: str, goal: str, timeframe_days: int = 90, milestones: Optional[List[PydanticMilestone]] = None) -> PydanticProject:
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            db_project = DBProject(
                user_id=user_id,
                goal=goal,
                timeframe_days=timeframe_days,
                status=TaskStatus.RUNNING.value
            )
            db.add(db_project)
            await db.flush()
            
            pydantic_milestones = []
            
            if not milestones:
                for i in range(1, 4):
                    period_days = (timeframe_days // 3) * i
                    target_date = (datetime.now() + timedelta(days=period_days)).strftime("%Y-%m-%d")
                    db_m = DBMilestone(
                        project_id=db_project.id,
                        title=f"Month {i}: Phase Execution",
                        focus="",
                        target_date=target_date,
                        status=TaskStatus.PENDING.value
                    )
                    db.add(db_m)
                    pydantic_milestones.append(PydanticMilestone(
                        id=db_m.id,
                        title=db_m.title,
                        focus=db_m.focus,
                        target_date=db_m.target_date,
                        task_ids=[],
                        status=TaskStatus.PENDING
                    ))
            else:
                for pm in milestones:
                    db_m = DBMilestone(
                        id=pm.id,
                        project_id=db_project.id,
                        title=pm.title,
                        focus=pm.focus,
                        target_date=pm.target_date,
                        metrics=pm.metrics,
                        status=pm.status.value
                    )
                    db.add(db_m)
                    pydantic_milestones.append(pm)
                    
            await db.commit()
            
            logger.info(f"Created {timeframe_days}-day strategic project: {goal} for user {user_id}")
            
            return PydanticProject(
                id=db_project.id,
                goal=db_project.goal,
                business_id=business_id,
                created_at=db_project.created_at.strftime("%Y-%m-%d"),
                milestones=pydantic_milestones,
                status=TaskStatus(db_project.status),
                current_milestone_index=db_project.current_milestone_index
            )
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def get_project(cls, db: Optional[AsyncSession], project_id: str) -> Optional[PydanticProject]:
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(DBProject).options(selectinload(DBProject.milestones)).where(DBProject.id == project_id)
            result = await db.execute(stmt)
            db_project = result.scalar_one_or_none()
            
            if not db_project:
                return None
                
            pydantic_milestones = [
                PydanticMilestone(
                    id=m.id,
                    title=m.title,
                    focus=m.focus,
                    target_date=m.target_date,
                    metrics=m.metrics or [],
                    task_ids=[], 
                    status=TaskStatus(m.status)
                ) for m in db_project.milestones
            ]
            
            pydantic_milestones.sort(key=lambda x: x.target_date)
            
            return PydanticProject(
                id=db_project.id,
                goal=db_project.goal,
                business_id=db_project.user_id,
                created_at=db_project.created_at.strftime("%Y-%m-%d"),
                milestones=pydantic_milestones,
                status=TaskStatus(db_project.status),
                current_milestone_index=db_project.current_milestone_index
            )
        finally:
            if should_close:
                await db.close()

    @classmethod
    async def advance_project(cls, db: Optional[AsyncSession], project_id: str):
        should_close = False
        if db is None:
            db = AsyncSessionLocal()
            should_close = True
            
        try:
            stmt = select(DBProject).options(selectinload(DBProject.milestones)).where(DBProject.id == project_id)
            result = await db.execute(stmt)
            db_project = result.scalar_one_or_none()
            
            if not db_project:
                return
                
            if db_project.current_milestone_index < len(db_project.milestones) - 1:
                db_project.current_milestone_index += 1
                await db.commit()
                logger.info(f"Project {project_id} advanced to next milestone.")
            else:
                db_project.status = TaskStatus.COMPLETED.value
                await db.commit()
                logger.info(f"Project {project_id} marked as COMPLETED.")
        finally:
            if should_close:
                await db.close()

# Global instance
project_manager = ProjectManager()
