from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AccountTier(str, Enum):
    FREE = "free"
    STARTER = "starter"
    GROWTH = "growth"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    TRIALING = "trialing"

class SubscriptionPlan(BaseModel):
    id: str
    name: str
    price_usd: float
    agent_limit: int
    credits_monthly: int
    extra_agent_price_usd: float
    daily_rental_usd: float
    features: List[str] = Field(default_factory=list)

class HiredAgent(BaseModel):
    agent_id: str
    hired_until: datetime
    auto_renew: bool = True

class UserSubscription(BaseModel):
    user_id: str
    tier: AccountTier = AccountTier.FREE
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    renewal_date: Optional[datetime] = None
    hired_agents: List[HiredAgent] = Field(default_factory=list)
    credits_used: int = 0
    credits_limit: int = 100
    
class WaitlistEntry(BaseModel):
    email: str
    full_name: Optional[str] = None
    company: Optional[str] = None
    use_case: Optional[str] = None
    status: str = "pending" # pending, invited, converted
    created_at: datetime = Field(default_factory=datetime.now)
    position: Optional[int] = None
