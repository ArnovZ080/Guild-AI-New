"""
Customer Journey Data Models.
Clean Pydantic models for full-funnel customer lifecycle tracking.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid


# --- Enums ---

class JourneyStage(str, Enum):
    """Full-funnel customer lifecycle stages."""
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    PURCHASE = "purchase"
    ONBOARDING = "onboarding"
    ADOPTION = "adoption"
    RETENTION = "retention"
    ADVOCACY = "advocacy"
    CHURN = "churn"

class TouchpointType(str, Enum):
    """Types of customer interactions."""
    WEBSITE_VISIT = "website_visit"
    EMAIL_OPEN = "email_open"
    EMAIL_CLICK = "email_click"
    SOCIAL_ENGAGEMENT = "social_engagement"
    SUPPORT_TICKET = "support_ticket"
    PHONE_CALL = "phone_call"
    MEETING = "meeting"
    DEMO = "demo"
    TRIAL_START = "trial_start"
    PURCHASE = "purchase"
    UPGRADE = "upgrade"
    FEEDBACK = "feedback"
    REFERRAL = "referral"

class ActionType(str, Enum):
    """Types of proactive actions the AI can take."""
    ENGAGEMENT = "engagement"
    RETENTION = "retention"
    UPSELL = "upsell"
    SUPPORT = "support"
    ONBOARDING = "onboarding"
    TRAINING = "training"
    FEATURE_ADOPTION = "feature_adoption"
    COMMUNITY = "community"
    FEEDBACK = "feedback"

class ActionPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# --- Core Models ---

class Touchpoint(BaseModel):
    """A single customer interaction."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    type: TouchpointType
    channel: str              # email, website, social, phone
    platform: str             # gmail, facebook, hubspot
    stage: JourneyStage = JourneyStage.AWARENESS
    sentiment: Optional[str] = None
    outcome: Optional[str] = None
    value: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Milestone(BaseModel):
    """A significant journey event (first purchase, first referral, churn)."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    event: str                # first_contact, first_purchase, churn, etc.
    stage: JourneyStage
    impact_score: float = 0.0
    description: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CustomerJourney(BaseModel):
    """Complete lifecycle view of a customer."""
    customer_id: str
    current_stage: JourneyStage = JourneyStage.AWARENESS
    journey_start: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    touchpoints: List[Touchpoint] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    journey_score: float = 0.0           # 0-100 health composite
    churn_risk: float = 0.0              # 0.0-1.0
    conversion_probability: float = 0.0  # 0.0-1.0
    next_likely_stage: Optional[JourneyStage] = None
    health: str = "good"                 # excellent, good, warning, critical
    days_in_stage: int = 0
    total_duration_days: int = 0

class NextBestAction(BaseModel):
    """A recommended proactive action for a customer."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    action_type: ActionType
    priority: ActionPriority
    title: str
    description: str
    confidence: float = 0.0       # 0.0-1.0
    expected_impact: float = 0.0  # 0-100
    urgency: float = 0.0          # 0-100
    assigned_agent: str = ""
    execution_steps: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    status: str = "recommended"   # recommended, approved, executing, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)
