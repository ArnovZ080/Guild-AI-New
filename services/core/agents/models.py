import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    BLOCKED = "blocked"
    ESCALATED = "escalated" # Reassigned or needs intervention
    COMPLETED = "completed"
    VERIFIED = "verified"   # Validated by Judge
    FAILED = "failed"

class AgentEventType(str, Enum):
    STARTED = "started"
    THINKING = "thinking"
    STEP_COMPLETED = "step_completed"
    COMPLETED = "completed"
    FAILED = "failed"
    HANDOFF = "handoff"
    APPROVAL_REQUEST = "approval_request"

class TaskResult(BaseModel):
    """
    Standardized result from an agent task execution.
    Aligned with Transparency and Education pillars.
    """
    data: Any
    status: TaskStatus = TaskStatus.COMPLETED
    process_log: List[str] = Field(default_factory=list) # "Theater" actions
    educational_takeaway: Optional[str] = None         # "Lesson learned"
    cost: float = 0.0                                  # Calculated cost
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentEvent(BaseModel):
    """
    Real-time event for Agent Theater visualization.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    workflow_name: Optional[str] = None
    event_type: AgentEventType
    description: str
    how: Optional[str] = None  # Technical detail/tool used
    why: Optional[str] = None  # Reasoning/Strategic goal
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    data: Dict[str, Any] = Field(default_factory=dict)
    progress: float = 0.0

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuthorityLevel(str, Enum):
    FULL = "full"           # Agent runs with full autonomy
    SEMI = "semi"           # Agent requires checkpoints/approval for key actions
    HUMAN = "human"         # Agent must wait for explicit human approval

class DelegationSpec(BaseModel):
    """
    Structured specification for a delegated task (The "Smart Contract").
    """
    id: str
    intent: str
    assigned_agent: str
    dependencies: List[str] = Field(default_factory=list)
    boundaries: List[str] = Field(default_factory=list)
    authority_level: AuthorityLevel = AuthorityLevel.FULL
    success_criteria: List[str] = Field(default_factory=list)
    rationale: str
    
    # Contractual Enhancements
    risk_level: RiskLevel = RiskLevel.LOW
    deadline: Optional[str] = None
    resources: Dict[str, Any] = Field(default_factory=dict)
    retry_limit: int = 2
    verification_method: str = "evaluator_league"
    
    # Context/Results
    context_requirements: List[str] = Field(default_factory=list)
    result: Optional[TaskResult] = None
    status: TaskStatus = TaskStatus.PENDING
    
    # Transparency & Education (Theater Meta)
    process_log: List[str] = Field(default_factory=list) # Step-by-step "Theater" actions
    educational_takeaway: Optional[str] = None         # "Lesson learned" for the user
    cost_breakdown: Dict[str, float] = Field(default_factory=dict) # Token costs, tool costs

class DelegationPlan(BaseModel):
    """
    A collection of delegated tasks forming a workflow.
    """
    tasks: List[DelegationSpec]
    overall_rational: Optional[str] = None

class BrandIdentity(BaseModel):
    voice: str
    tone: str
    vocabulary: List[str] = Field(default_factory=list)
    visual_style: Dict[str, str] = Field(default_factory=dict) # e.g. {"colors": ["#...", "#..."], "typography": "Inter"}
    dos: List[str] = Field(default_factory=list)
    donts: List[str] = Field(default_factory=list)

class ICPProfile(BaseModel):
    ideal_client_description: str
    demographics: Dict[str, Any] = Field(default_factory=dict)
    psychographics: List[str] = Field(default_factory=list)
    pain_points: List[str] = Field(default_factory=list)
    buying_triggers: List[str] = Field(default_factory=list)

class KnowledgeSource(BaseModel):
    id: str
    type: str # "file", "url", "tool"
    name: str
    content_preview: Optional[str] = None
    indexed_at: str

class BusinessIdentity(BaseModel):
    """
    Persistent context of the small business.
    Expanded in Phase 4 for Brand, ICP, and Knowledge persistence.
    """
    business_name: str
    niche: str
    core_objectives: List[str] = Field(default_factory=list)
    
    # Deep Context Modules
    brand: BrandIdentity
    icp: ICPProfile
    knowledge_base: List[KnowledgeSource] = Field(default_factory=list)
    
    # Operational Settings
    constraints: Dict[str, Any] = Field(default_factory=dict)
    budget_limit: float = 0.0
    integrations_active: List[str] = Field(default_factory=list)

class ProjectMilestone(BaseModel):
    id: str
    title: str
    focus: Optional[str] = None
    metrics: List[str] = Field(default_factory=list)
    task_ids: List[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    target_date: str

class Project(BaseModel):
    """
    Long-running strategic roadmap (e.g. 90-day growth plan).
    """
    id: str
    goal: str
    business_id: str
    created_at: str
    milestones: List[ProjectMilestone]
    current_milestone_index: int = 0
    status: TaskStatus = TaskStatus.PENDING

class AuthorizationRequest(BaseModel):
    """
    User approval request for a sensitive agent action.
    """
    id: str
    task_id: str
    agent_id: str
    action_type: str # e.g. "finance", "social_media", "real_world"
    description: str
    params: Dict[str, Any]
    status: str = "pending" # pending, approved, rejected
    created_at: str
