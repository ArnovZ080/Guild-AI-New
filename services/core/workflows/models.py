"""
Workflow Models.
Clean Pydantic models for autonomous multi-step workflow execution.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    AWAITING_APPROVAL = "awaiting_approval"
    SKIPPED = "skipped"

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"         # Waiting for human approval on a step
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class RiskLevel(str, Enum):
    """Determines whether a step auto-executes or needs HITL approval."""
    AUTO = "auto"             # Just do it
    LOW = "low"               # Log it, but auto-execute
    MEDIUM = "medium"         # Needs approval if above threshold
    HIGH = "high"             # Always needs human approval
    CRITICAL = "critical"     # Always needs human approval + audit trail


class WorkflowStep(BaseModel):
    """A single step in a workflow."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    agent: str                              # Which agent executes this
    action: str                             # The action/intent to perform
    params: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)   # Step names that must complete first
    risk_level: RiskLevel = RiskLevel.AUTO
    timeout_seconds: int = 300
    retry_limit: int = 2
    status: StepStatus = StepStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    evaluator_score: Optional[float] = None

class WorkflowExecution(BaseModel):
    """A running or completed workflow instance."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_name: str
    display_name: str
    description: str = ""
    initiated_by: str = "system"
    steps: List[WorkflowStep] = Field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    params: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_duration_seconds: Optional[int] = None
    transparency_log: List[Dict[str, Any]] = Field(default_factory=list)
    error_log: List[str] = Field(default_factory=list)

class WorkflowTemplate(BaseModel):
    """A reusable workflow blueprint."""
    name: str                  # Unique template key
    display_name: str
    description: str
    category: str = "general"  # customer, content, sales, finance, operations
    steps: List[Dict[str, Any]] = Field(default_factory=list)

    def add_step(self, name: str, agent: str, action: str,
                 params: Optional[Dict[str, Any]] = None,
                 risk_level: RiskLevel = RiskLevel.AUTO,
                 dependencies: Optional[List[str]] = None) -> "WorkflowTemplate":
        self.steps.append({
            "name": name,
            "agent": agent,
            "action": action,
            "params": params or {},
            "risk_level": risk_level,
            "dependencies": dependencies or [],
        })
        return self
