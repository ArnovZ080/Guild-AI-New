from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
from ...core.agents.subscription_models import (
    SubscriptionPlan, AccountTier, UserSubscription, HiredAgent
)
from ...core.integrations.paystack import paystack_client
import uuid

router = APIRouter(prefix="/subscription", tags=["Subscription"])

# Static Plan Definitions
PLANS = [
    SubscriptionPlan(
        id="starter", name="Starter", price_usd=49.0, agent_limit=5, 
        credits_monthly=500, extra_agent_price_usd=12.0, daily_rental_usd=1.50,
        features=["5 AI Agents", "500 credits", "Judge QA", "Basic Analytics"]
    ),
    SubscriptionPlan(
        id="growth", name="Growth", price_usd=99.0, agent_limit=10, 
        credits_monthly=1000, extra_agent_price_usd=11.0, daily_rental_usd=1.25,
        features=["10 AI Agents", "1000 credits", "36 Integrations", "Advanced Analytics"]
    ),
    SubscriptionPlan(
        id="professional", name="Professional", price_usd=199.0, agent_limit=25, 
        credits_monthly=2500, extra_agent_price_usd=10.0, daily_rental_usd=1.00,
        features=["25 AI Agents", "2500 credits", "Custom Workflows", "Priority Support"]
    ),
    SubscriptionPlan(
        id="enterprise", name="Enterprise", price_usd=499.0, agent_limit=100, 
        credits_monthly=10000, extra_agent_price_usd=8.0, daily_rental_usd=0.50,
        features=["All 100+ Agents", "10k credits", "API Access", "White Label"]
    ),
]

@router.get("/plans")
async def get_plans():
    return PLANS

@router.get("/info/{user_id}")
async def get_subscription_info(user_id: str):
    # Mock lookup
    return {
        "tier": "free",
        "status": "active",
        "credits": {"used": 20, "limit": 100}
    }

@router.post("/initialize")
async def initialize_payment(plan_id: str, email: str):
    plan = next((p for p in PLANS if p.id == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    reference = f"SUB-{uuid.uuid4().hex[:8]}"
    callback_url = "http://localhost:3000/subscription/verify" # Placeholder
    
    resp = await paystack_client.initialize_transaction(
        email=email,
        amount_usd=plan.price_usd,
        reference=reference,
        callback_url=callback_url
    )
    
    if resp.get("status"):
        return resp["data"]
    else:
        raise HTTPException(status_code=400, detail=resp.get("message", "Payment initialization failed"))

@router.post("/verify")
async def verify_payment(reference: str):
    resp = await paystack_client.verify_transaction(reference)
    if resp.get("status") and resp["data"].get("status") == "success":
        # In production: Update user tier in DB here
        return {"status": "success", "tier": "upgraded"}
    else:
        return {"status": "failed", "message": resp.get("message", "Verification failed")}
