import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from services.core.agents.models import Project, ProjectMilestone, TaskStatus
from services.core.logging import logger

class ProjectManager:
    """
    Manages long-running (30/60/90 day) growth roadmaps.
    """
    def __init__(self):
        self.projects: Dict[str, Project] = {}

    def create_project(self, business_id: str, goal: str, timeframe_days: int = 90, milestones: Optional[List[ProjectMilestone]] = None) -> Project:
        project_id = str(uuid.uuid4())
        
        if not milestones:
            # Simple heuristic fallback if no AI milestones provided
            milestones = []
            for i in range(1, 4):
                period_days = (timeframe_days // 3) * i
                target_date = (datetime.now() + timedelta(days=period_days)).strftime("%Y-%m-%d")
                milestones.append(ProjectMilestone(
                    id=f"m{i}_{project_id[:8]}",
                    title=f"Month {i}: Phase Execution",
                    focus="",
                    target_date=target_date,
                    task_ids=[],
                    status=TaskStatus.PENDING
                ))
            
        project = Project(
            id=project_id,
            goal=goal,
            business_id=business_id,
            created_at=datetime.now().strftime("%Y-%m-%d"),
            milestones=milestones,
            status=TaskStatus.RUNNING
        )
        
        self.projects[project_id] = project
        logger.info(f"Created {timeframe_days}-day strategic project: {goal}")
        return project

    def get_project(self, project_id: str) -> Project:
        return self.projects.get(project_id)

    def advance_project(self, project_id: str):
        project = self.get_project(project_id)
        if not project: return
        
        if project.current_milestone_index < len(project.milestones) - 1:
            project.current_milestone_index += 1
            logger.info(f"Project {project_id} advanced to milestone: {project.milestones[project.current_milestone_index].title}")
        else:
            project.status = TaskStatus.COMPLETED
            logger.info(f"Project {project_id} marked as COMPLETED.")

# Global instance
project_manager = ProjectManager()
