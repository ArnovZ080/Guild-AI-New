"""
Adaptive Learning Data Models.
Persistent storage for user preferences, action outcomes, and derived patterns.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

# --- Enums ---

class PreferenceCategory(str, Enum):
    SCHEDULING = "scheduling"
    COMMUNICATION = "communication"
    FINANCE = "finance"
    CONTENT = "content"
    GENERAL = "general"

class PreferenceConfidence(str, Enum):
    SUGGESTED = "suggested"   # AI thinks it spotted a pattern, needs more data
    LIKELY = "likely"         # Strong signal, presented to user for confirmation
    CONFIRMED = "confirmed"   # User explicitly confirmed the rule
    REJECTED = "rejected"     # User rejected the suggestion

class OutcomeScore(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    NEUTRAL = "neutral"
    POOR = "poor"
    FAILED = "failed"

# --- Core Models ---

class UserPreference(BaseModel):
    """A learned behavioral rule about the user."""
    id: str
    category: PreferenceCategory
    rule: str                       # Human-readable: "No meetings on Tuesdays"
    rule_key: str                   # Machine-readable: "no_meetings_tuesday"
    conditions: Dict[str, Any] = Field(default_factory=dict)  # e.g., {"day": "tuesday", "type": "meeting"}
    confidence: PreferenceConfidence = PreferenceConfidence.SUGGESTED
    signal_count: int = 1           # How many times the pattern was observed
    first_observed: datetime = Field(default_factory=datetime.utcnow)
    last_observed: datetime = Field(default_factory=datetime.utcnow)
    source: str = "observation"     # "observation", "explicit", "inferred"

class ActionOutcome(BaseModel):
    """The result of a specific AI-initiated action."""
    id: str
    task_id: str
    agent_id: str
    action_type: str                # e.g., "social_post", "email_campaign", "crm_sync"
    platform: str                   # e.g., "twitter", "linkedin", "hubspot"
    params: Dict[str, Any] = Field(default_factory=dict)
    score: OutcomeScore = OutcomeScore.NEUTRAL
    metrics: Dict[str, float] = Field(default_factory=dict)  # e.g., {"engagement_rate": 0.05, "clicks": 120}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    context: Dict[str, Any] = Field(default_factory=dict)    # e.g., {"day_of_week": "monday", "time": "10:00"}

class LearnedPattern(BaseModel):
    """An AI-derived optimization insight from aggregated outcomes."""
    id: str
    category: str                   # e.g., "content_timing", "email_subject", "deal_follow_up"
    insight: str                    # Human-readable: "LinkedIn posts at 10am get 2x engagement"
    recommendation: str             # Actionable: "Schedule LinkedIn posts between 9-11am"
    supporting_data: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = 0.0   # 0.0 to 1.0
    sample_size: int = 0            # Number of data points
    first_derived: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True
