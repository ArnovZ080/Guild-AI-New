from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Optional
from datetime import datetime
import os
from ...core.agents.subscription_models import WaitlistEntry
from ...core.security.env_validator import EnvironmentValidator

router = APIRouter(prefix="/waitlist", tags=["Waitlist"])

# Mock database state for now (will be replaced by persistent DB in future phase)
_waitlist_db: List[WaitlistEntry] = []

@router.post("/join")
async def join_waitlist(entry: WaitlistEntry):
    # Check if already exists
    if any(e.email == entry.email for e in _waitlist_db):
        # Find existing position
        pos = next(i for i, e in enumerate(_waitlist_db) if e.email == entry.email) + 1
        return {"message": "Already on waitlist", "position": pos}
    
    entry.position = len(_waitlist_db) + 1
    _waitlist_db.append(entry)
    return {"message": "Success", "position": entry.position}

@router.post("/check-beta-access")
async def check_beta_access(email: str = Body(..., embed=True)):
    # 1. Check environment variables (BETA_TESTER_EMAILS)
    beta_emails = os.getenv("BETA_TESTER_EMAILS", "").split(",")
    if email in [e.strip() for e in beta_emails]:
        return {"has_beta_access": True, "source": "env"}
    
    # 2. Check mock DB
    entry = next((e for e in _waitlist_db if e.email == email), None)
    if entry and entry.status == "invited":
        return {"has_beta_access": True, "source": "db"}
    
    return {"has_beta_access": False}

@router.get("/list")
async def list_waitlist():
    # Admin only check would go here
    return _waitlist_db

@router.post("/grant-beta-access")
async def grant_beta_access(email: str = Body(..., embed=True)):
    entry = next((e for e in _waitlist_db if e.email == email), None)
    if entry:
        entry.status = "invited"
        return {"message": f"Beta access granted to {email}"}
    
    # If not in waitlist, create a manual entry
    new_entry = WaitlistEntry(email=email, status="invited", position=0)
    _waitlist_db.append(new_entry)
    return {"message": f"Beta access granted to {email} (Manual)"}
