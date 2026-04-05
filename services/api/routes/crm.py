"""CRM API Routes"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.base import get_db
from services.core.db.models import UserAccount, Contact
from services.api.middleware.auth import get_current_user
from services.core.adk.customer.crm import CRMAgent
from services.core.crm.capture import lead_capture

router = APIRouter()


class AddContactRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    source_platform: Optional[str] = None


class MoveStageRequest(BaseModel):
    stage: str


class EngagementWebhook(BaseModel):
    platform: str
    type: str = "engagement"
    content_item_id: Optional[str] = None
    engaged_user: dict = {}
    engagement_text: str = ""


@router.get("/contacts")
async def list_contacts(
    stage: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    query = select(Contact).where(Contact.user_id == current_user.id)
    if stage:
        query = query.where(Contact.pipeline_stage == stage)
    result = await db.execute(query.order_by(Contact.created_at.desc()).limit(100))
    contacts = list(result.scalars().all())
    return {"contacts": [{"id": c.id, "name": c.name, "email": c.email, "company": c.company,
                           "stage": c.pipeline_stage, "icp_score": c.icp_score,
                           "engagement_level": c.engagement_level} for c in contacts]}


@router.get("/contacts/{contact_id}")
async def get_contact(contact_id: str, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.user_id == current_user.id))
    contact = result.scalars().first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"id": contact.id, "name": contact.name, "email": contact.email, "company": contact.company,
            "stage": contact.pipeline_stage, "icp_score": contact.icp_score, "profile": contact.profile_data}


@router.post("/contacts")
async def add_contact(request: AddContactRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    crm = CRMAgent()
    result = await crm.add_contact(db, current_user.id, request.model_dump())
    return result


@router.put("/contacts/{contact_id}")
async def update_contact(contact_id: str, request: AddContactRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.user_id == current_user.id))
    contact = result.scalars().first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for k, v in request.model_dump(exclude_none=True).items():
        setattr(contact, k, v)
    await db.commit()
    return {"id": contact.id, "status": "updated"}


@router.get("/pipeline")
async def pipeline_summary(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    crm = CRMAgent()
    return await crm.get_pipeline_summary(db, current_user.id)


@router.post("/contacts/{contact_id}/stage")
async def move_stage(contact_id: str, request: MoveStageRequest, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    crm = CRMAgent()
    return await crm.move_stage(db, current_user.id, {"contact_id": contact_id, "new_stage": request.stage})


@router.get("/leads/new")
async def new_leads(db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    result = await db.execute(
        select(Contact).where(Contact.user_id == current_user.id, Contact.icp_score >= 0.7)
        .order_by(Contact.created_at.desc()).limit(20))
    leads = list(result.scalars().all())
    return {"leads": [{"id": c.id, "name": c.name, "icp_score": c.icp_score, "engagement_level": c.engagement_level} for c in leads]}


@router.post("/capture/engagement")
async def capture_engagement(request: EngagementWebhook, db: AsyncSession = Depends(get_db), current_user: UserAccount = Depends(get_current_user)):
    result = await lead_capture.process_engagement(db, current_user.id, request.platform, request.model_dump())
    return result
