from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from services.core.db.base import get_db
from services.core.db.models import UserAccount, HostedPage, FormSubmission
from services.api.middleware.auth import get_current_user

router = APIRouter(tags=["Funnels"])

class GenerateFunnelRequest(BaseModel):
    objective: str
    title: str
    slug: str

@router.get("/funnels")
async def list_funnels(
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    result = await db.execute(
        select(HostedPage)
        .where(HostedPage.user_id == current_user.id)
        .order_by(HostedPage.created_at.desc())
    )
    pages = result.scalars().all()
    return pages

@router.post("/funnels/generate")
async def generate_funnel(
    req: GenerateFunnelRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    from services.core.adk.marketing.funnel_builder import FunnelBuilderAgent
    
    agent = FunnelBuilderAgent()
    html_content = await agent.generate_landing_page(current_user.id, req.objective, db=db)
    
    import secrets
    page = HostedPage(
        user_id=current_user.id,
        title=req.title,
        slug=req.slug,
        page_type="lead_capture",
        html_content=html_content,
        form_id=secrets.token_urlsafe(12),
        status="published" # Let's auto publish for now
    )
    
    db.add(page)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
        
    return page

@router.get("/funnels/{page_id}")
async def get_funnel(
    page_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user)
):
    result = await db.execute(
        select(HostedPage)
        .where(HostedPage.id == page_id, HostedPage.user_id == current_user.id)
    )
    page = result.scalars().first()
    if not page:
        raise HTTPException(status_code=404, detail="Funnel not found")
        
    # Get submissions
    subs_result = await db.execute(
        select(FormSubmission).where(FormSubmission.page_id == page.id).order_by(FormSubmission.created_at.desc())
    )
    subs = subs_result.scalars().all()
    
    return {
        "page": page,
        "submissions": subs
    }
