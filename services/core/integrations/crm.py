from typing import Dict, Any, List, Optional
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, Field

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    UNQUALIFIED = "unqualified"
    WON = "won"
    LOST = "lost"

class Contact(BaseModel):
    """Standardized contact format"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    status: LeadStatus = LeadStatus.NEW
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Deal(BaseModel):
    """Standardized deal format"""
    id: str
    title: str
    amount: float
    currency: str = "USD"
    stage: str
    status: Optional[str] = None
    contact_id: Optional[str] = None
    owner_id: Optional[str] = None
    probability: float = 0.0
    expected_close_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
