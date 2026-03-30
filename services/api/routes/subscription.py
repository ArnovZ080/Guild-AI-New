"""
Paystack Subscription Routes

POST /api/subscription/initialize — Create Paystack checkout
POST /api/subscription/webhook    — Handle Paystack webhook events
GET  /api/subscription/status     — Get current subscription status
"""
import logging
import hashlib
import hmac
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.core.db.base import get_db
from services.core.db.models import UserAccount, Subscription
from services.core.config import settings
from services.api.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

# Plan configurations
PLANS = {
    "starter": {
        "amount": 4900,  # cents ($49)
        "token_budget": 2_000_000,
        "content_limit": 50,
        "video_limit": 0,
        "platform_limit": 3,
    },
    "growth": {
        "amount": 14900,  # cents ($149)
        "token_budget": 10_000_000,
        "content_limit": 200,
        "video_limit": 10,
        "platform_limit": -1,  # unlimited
    },
    "scale": {
        "amount": 29900,  # cents ($299)
        "token_budget": 30_000_000,
        "content_limit": 500,
        "video_limit": 30,
        "platform_limit": -1,  # unlimited
    },
}


class InitializeRequest(BaseModel):
    plan: str  # starter, growth, scale


class SubscriptionStatus(BaseModel):
    plan: str
    status: str
    content_used: int
    content_limit: int
    video_used: int
    video_limit: int
    token_budget: int
    tokens_used: int


@router.post("/initialize")
async def initialize_subscription(
    request: InitializeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    """Initialize a Paystack subscription checkout."""
    if request.plan not in PLANS:
        raise HTTPException(status_code=400, detail=f"Invalid plan: {request.plan}")

    plan_config = PLANS[request.plan]

    if not settings.PAYSTACK_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Payment processing not configured")

    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.paystack.co/transaction/initialize",
            json={
                "email": current_user.email,
                "amount": plan_config["amount"],
                "metadata": {
                    "user_id": current_user.id,
                    "plan": request.plan,
                },
                "callback_url": f"{settings.ALLOWED_ORIGINS[0]}/subscription/callback",
            },
            headers={
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            },
        )

    data = response.json()
    if not data.get("status"):
        raise HTTPException(status_code=502, detail="Paystack initialization failed")

    return {
        "authorization_url": data["data"]["authorization_url"],
        "reference": data["data"]["reference"],
    }


@router.post("/webhook")
async def paystack_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle Paystack webhook events."""
    body = await request.body()
    signature = request.headers.get("x-paystack-signature", "")

    if settings.PAYSTACK_SECRET_KEY:
        expected = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode(),
            body,
            hashlib.sha512,
        ).hexdigest()
        if signature != expected:
            raise HTTPException(status_code=403, detail="Invalid webhook signature")

    import json
    event = json.loads(body)
    event_type = event.get("event")

    if event_type == "charge.success":
        data = event.get("data", {})
        metadata = data.get("metadata", {})
        user_id = metadata.get("user_id")
        plan = metadata.get("plan")

        if user_id and plan and plan in PLANS:
            plan_config = PLANS[plan]

            result = await db.execute(
                select(Subscription).where(Subscription.user_id == user_id)
            )
            sub = result.scalars().first()

            if not sub:
                sub = Subscription(user_id=user_id)
                db.add(sub)

            sub.plan = plan
            sub.status = "active"
            sub.paystack_id = data.get("reference")
            sub.token_budget = plan_config["token_budget"]
            sub.tokens_used_month = 0
            sub.content_count_month = 0
            sub.video_count_month = 0

            user_result = await db.execute(
                select(UserAccount).where(UserAccount.id == user_id)
            )
            user = user_result.scalars().first()
            if user:
                user.subscription_tier = plan

            await db.commit()
            logger.info("Subscription activated: user=%s plan=%s", user_id, plan)

    return {"status": "ok"}


@router.get("/status", response_model=SubscriptionStatus)
async def get_subscription_status(
    db: AsyncSession = Depends(get_db),
    current_user: UserAccount = Depends(get_current_user),
):
    """Get the current user's subscription status."""
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == current_user.id)
    )
    sub = result.scalars().first()

    if not sub:
        return SubscriptionStatus(
            plan="free",
            status="active",
            content_used=0,
            content_limit=5,
            video_used=0,
            video_limit=0,
            token_budget=100_000,
            tokens_used=0,
        )

    plan_config = PLANS.get(sub.plan, PLANS["starter"])

    return SubscriptionStatus(
        plan=sub.plan,
        status=sub.status,
        content_used=sub.content_count_month or 0,
        content_limit=plan_config["content_limit"],
        video_used=sub.video_count_month or 0,
        video_limit=plan_config["video_limit"],
        token_budget=sub.token_budget or 0,
        tokens_used=sub.tokens_used_month or 0,
    )
