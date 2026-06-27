from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.base import get_db
from services.core.db.models import HostedPage, FormSubmission, Contact
from services.core.logging import logger
from services.core.crm.capture import lead_capture
from datetime import datetime
import redis.asyncio as aioredis
from services.core.config import settings

router = APIRouter(tags=["Public Funnels"])

@router.get("/p/{slug}", response_class=HTMLResponse)
async def serve_funnel_page(slug: str, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HostedPage).where(HostedPage.slug == slug, HostedPage.status == "published"))
    page = result.scalars().first()
    
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
        
    # Increment view counter (Atomic)
    page.views += 1
    await db.commit()
    
    html = page.html_content
    # Inject actual form_id
    if page.form_id:
        html = html.replace("{{form_id}}", page.form_id)
        
    # Return with CSP headers
    response = HTMLResponse(content=html)
    # Restrict script-src to specific CDNs to prevent XSS via LLM eval injection
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' https: data:; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://use.fontawesome.com;"
    return response

@router.post("/api/public/form/{form_id}")
async def capture_form_submission(
    form_id: str, 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    ip = request.client.host if request.client else "unknown"
    rate_limit_key = f"rate_limit:form:{form_id}:{ip}"
    r = aioredis.from_url(settings.REDIS_URL)
    try:
        current = await r.incr(rate_limit_key)
        if current == 1:
            await r.expire(rate_limit_key, 60)
        if current > 10:
            raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
    finally:
        await r.aclose()
        
    # Retrieve form data
    form_data = await request.form()
    data_dict = dict(form_data)
    
    # Honeypot check (assume 'website' or 'address_line_2' is a honeypot field in the HTML if LLM adds it, or just basic bot check)
    if data_dict.get("honeypot") or data_dict.get("bot_field"):
        logger.warning(f"Bot detected on form {form_id}")
        return RedirectResponse(url="/", status_code=303)
        
    result = await db.execute(select(HostedPage).where(HostedPage.form_id == form_id))
    page = result.scalars().first()
    
    if not page:
        raise HTTPException(status_code=404, detail="Form not found")
        
    email = data_dict.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
        
    # Deduplication
    existing_sub = await db.execute(
        select(FormSubmission).where(
            FormSubmission.page_id == page.id, 
            FormSubmission.email == email
        )
    )
    if existing_sub.scalars().first():
        logger.info(f"Duplicate submission for {email} on page {page.id}")
        if page.redirect_url:
            return RedirectResponse(url=page.redirect_url, status_code=303)
        return HTMLResponse(content=f"<html><body><h1>{page.thank_you_message}</h1></body></html>")
        
    # Create submission
    sub = FormSubmission(
        page_id=page.id,
        email=email,
        name=data_dict.get("name") or data_dict.get("full_name"),
        phone=data_dict.get("phone"),
        custom_fields={k: v for k, v in data_dict.items() if k not in ["email", "name", "full_name", "phone"]},
        source_url=str(request.url),
        ip_country=request.headers.get("CF-IPCountry") or request.headers.get("X-Forwarded-For"),
        utm_source=data_dict.get("utm_source"),
        utm_medium=data_dict.get("utm_medium"),
        utm_campaign=data_dict.get("utm_campaign")
    )
    
    # Process into CRM Contact
    crm_result = await lead_capture.process_form_submission(db, page.user_id, {
        "source": "funnel",
        "name": data_dict.get("name") or data_dict.get("full_name"),
        "email": email,
        "form_name": page.title,
    })
    sub.contact_id = crm_result.get("contact_id")
    
    page.submissions += 1
    if page.views > 0:
        page.conversion_rate = (page.submissions / page.views) * 100
        
    db.add(sub)
    await db.commit()
    
    # Trigger nurture sequence or agent workflow asynchronously (to be implemented)
    
    if page.redirect_url:
        return RedirectResponse(url=page.redirect_url, status_code=303)
        
    return HTMLResponse(content=f"<html><head><script src='https://cdn.tailwindcss.com'></script></head><body class='bg-gray-50 flex items-center justify-center h-screen'><div class='bg-white p-8 rounded-2xl shadow-xl text-center'><h1 class='text-2xl font-bold text-gray-800 mb-4'>{page.thank_you_message}</h1><a href='#' onclick='history.back()' class='text-indigo-600 hover:underline'>Go Back</a></div></body></html>")
