from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool
    tier: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Chat / Orchestrator ---
class ChatRequest(BaseModel):
    goal: str
    require_preflight: bool = False
    context_overrides: Optional[dict] = None

class ChatResponse(BaseModel):
    status: str
    data: dict
    process_log: List[str] = []
    educational_takeaway: Optional[str] = None

# --- Agent Execution ---
class AgentExecuteRequest(BaseModel):
    input_data: dict
    context: Optional[dict] = None

# --- Projects ---
class ProjectCreate(BaseModel):
    goal: str

class ProjectResponse(BaseModel):
    id: str
    goal: str
    status: str
    class Config:
        from_attributes = True

# --- Workflows ---
class WorkflowExecuteRequest(BaseModel):
    params: Optional[dict] = None

class WorkflowApproveRequest(BaseModel):
    step_index: int
    approved: bool = True

# --- Integrations ---
class IntegrationConnectRequest(BaseModel):
    platform: str
    credentials: dict
