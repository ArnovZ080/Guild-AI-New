"""
Predictive Action Engine.
Generates proactive "Next Best Action" recommendations for customers
using LLM analysis, customer journey data, and historical outcome data.
"""
import logging
import json
import uuid
from typing import Dict, Any, List, Optional
from .models import (
    ActionType, ActionPriority, NextBestAction, JourneyStage, CustomerJourney
)
from .journey_tracker import JourneyTracker
from services.core.learning.outcome_tracker import OutcomeTracker
from services.core.llm import default_llm

logger = logging.getLogger(__name__)

# --- Action Pattern Configuration ---

ACTION_PATTERNS = {
    ActionType.ENGAGEMENT:      {"base_impact": 65, "base_success": 0.75, "urgency_boost": 15},
    ActionType.RETENTION:       {"base_impact": 85, "base_success": 0.68, "urgency_boost": 30},
    ActionType.UPSELL:          {"base_impact": 120, "base_success": 0.45, "urgency_boost": 5},
    ActionType.SUPPORT:         {"base_impact": 70, "base_success": 0.82, "urgency_boost": 25},
    ActionType.ONBOARDING:      {"base_impact": 90, "base_success": 0.78, "urgency_boost": 10},
    ActionType.TRAINING:        {"base_impact": 55, "base_success": 0.70, "urgency_boost": 0},
    ActionType.FEATURE_ADOPTION:{"base_impact": 75, "base_success": 0.65, "urgency_boost": 10},
    ActionType.COMMUNITY:       {"base_impact": 40, "base_success": 0.60, "urgency_boost": 0},
    ActionType.FEEDBACK:        {"base_impact": 35, "base_success": 0.55, "urgency_boost": 0},
}

# Segment -> preferred action types
SEGMENT_ACTIONS = {
    "new":        [ActionType.ONBOARDING, ActionType.TRAINING, ActionType.FEATURE_ADOPTION],
    "active":     [ActionType.ENGAGEMENT, ActionType.FEATURE_ADOPTION, ActionType.COMMUNITY],
    "at_risk":    [ActionType.RETENTION, ActionType.SUPPORT, ActionType.FEEDBACK],
    "power_user": [ActionType.UPSELL, ActionType.COMMUNITY, ActionType.FEEDBACK],
}

AGENT_MAPPING = {
    ActionType.ENGAGEMENT:       "MarketingAgent",
    ActionType.RETENTION:        "CustomerSuccessAgent",
    ActionType.UPSELL:           "SalesAgent",
    ActionType.SUPPORT:          "CustomerSupportAgent",
    ActionType.ONBOARDING:       "OnboardingAgent",
    ActionType.TRAINING:         "TrainingAgent",
    ActionType.FEATURE_ADOPTION: "CustomerSuccessAgent",
    ActionType.COMMUNITY:        "CommunityAgent",
    ActionType.FEEDBACK:         "CustomerSuccessAgent",
}


class PredictiveEngine:
    """
    Generates Next Best Action recommendations by combining:
    1. Customer journey data (stage, health, risk)
    2. Action pattern heuristics (segment-based scoring)
    3. Historical outcome data (what actually worked)
    4. LLM analysis for nuanced recommendations
    """

    # --- Public API ---

    @classmethod
    async def generate_actions(cls, db: Optional[Any], user_id: str, customer_id: str) -> List[NextBestAction]:
        """Generate ranked Next Best Action recommendations for a customer."""
        journey = await JourneyTracker.get_journey(db, user_id, customer_id)
        if not journey:
            logger.warning(f"PredictiveEngine: No journey data for {customer_id}")
            return []

        segment = cls._identify_segment(journey)
        preferred_actions = SEGMENT_ACTIONS.get(segment, SEGMENT_ACTIONS["active"])

        actions = []
        for action_type in preferred_actions:
            action = cls._build_action(customer_id, action_type, journey, segment)
            actions.append(action)

        # Sort by composite score: urgency * confidence * impact
        actions.sort(key=lambda a: a.urgency * a.confidence * a.expected_impact, reverse=True)
        return actions

    @classmethod
    async def get_proactive_tasks(cls, db: Optional[Any], user_id: str) -> List[NextBestAction]:
        """Scan all customers and return the top urgent actions globally."""
        all_actions = []
        for journey in await JourneyTracker.get_all_journeys(db, user_id):
            customer_actions = await cls.generate_actions(db, user_id, journey.customer_id)
            if customer_actions:
                all_actions.append(customer_actions[0])  # Top action per customer

        # Global sort by urgency
        all_actions.sort(key=lambda a: a.urgency * a.confidence, reverse=True)
        return all_actions[:20]  # Top 20 most urgent

    @classmethod
    async def generate_actions_llm(cls, db: Optional[Any], user_id: str, customer_id: str) -> List[NextBestAction]:
        """Use LLM for deeper, context-aware action generation."""
        journey = await JourneyTracker.get_journey(db, user_id, customer_id)
        if not journey:
            return []

        # Get best-performing strategies from adaptive learning
        best_strategy = await OutcomeTracker.get_best_strategy(db, user_id, "engagement")
        strategy_context = f"\nBest performing strategy: {best_strategy}" if best_strategy else ""

        sys_prompt = """You are a Customer Success strategist. Analyze the customer journey and recommend 3 specific actions.
Return JSON array, each with: action_type, priority (critical/high/medium/low), title, description, execution_steps (list), risk_factors (list)."""

        journey_summary = {
            "customer_id": customer_id,
            "current_stage": journey.current_stage.value,
            "health": journey.health,
            "churn_risk": journey.churn_risk,
            "journey_score": journey.journey_score,
            "days_in_stage": journey.days_in_stage,
            "total_touchpoints": len(journey.touchpoints),
            "milestones_reached": [m.event for m in journey.milestones],
        }

        user_prompt = f"""Customer Journey Data:
{json.dumps(journey_summary, indent=2)}
{strategy_context}

Generate 3 specific, actionable recommendations to improve this customer's health and move them to the next stage."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])

        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "[" in response:
                json_str = response[response.index("["):response.rindex("]") + 1]
            else:
                return []

            raw = json.loads(json_str)
            actions = []
            for item in raw:
                action_type = ActionType(item.get("action_type", "engagement"))
                actions.append(NextBestAction(
                    customer_id=customer_id,
                    action_type=action_type,
                    priority=ActionPriority(item.get("priority", "medium")),
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    confidence=0.7,
                    expected_impact=ACTION_PATTERNS.get(action_type, {}).get("base_impact", 50),
                    urgency=50.0,
                    assigned_agent=AGENT_MAPPING.get(action_type, "CustomerSuccessAgent"),
                    execution_steps=item.get("execution_steps", []),
                    risk_factors=item.get("risk_factors", []),
                ))
            return actions
        except Exception as e:
            logger.error(f"LLM action generation failed: {e}")
            return []

    # --- Internal ---

    @classmethod
    def _identify_segment(cls, journey: CustomerJourney) -> str:
        if journey.total_duration_days < 30:
            return "new"
        elif journey.churn_risk > 0.5:
            return "at_risk"
        elif journey.journey_score > 80:
            return "power_user"
        return "active"

    @classmethod
    def _build_action(cls, customer_id: str, action_type: ActionType,
                      journey: CustomerJourney, segment: str) -> NextBestAction:
        pattern = ACTION_PATTERNS.get(action_type, {})

        # Confidence: base success rate adjusted by journey health
        health_factor = {"excellent": 1.1, "good": 1.0, "warning": 0.85, "critical": 0.7}
        confidence = pattern.get("base_success", 0.5) * health_factor.get(journey.health, 1.0)
        confidence = min(1.0, max(0.0, confidence))

        # Impact: base impact adjusted by journey score
        impact = pattern.get("base_impact", 50) * (journey.journey_score / 100.0 + 0.5)
        impact = min(100.0, impact)

        # Urgency: base urgency + churn-based boost
        urgency = 50.0 + pattern.get("urgency_boost", 0)
        if journey.churn_risk > 0.7:
            urgency += 30
        elif journey.churn_risk > 0.4:
            urgency += 15
        urgency = min(100.0, urgency)

        # Priority from composite score
        composite = (urgency + impact) / 2
        if composite >= 80:
            priority = ActionPriority.CRITICAL
        elif composite >= 65:
            priority = ActionPriority.HIGH
        elif composite >= 45:
            priority = ActionPriority.MEDIUM
        else:
            priority = ActionPriority.LOW

        return NextBestAction(
            customer_id=customer_id,
            action_type=action_type,
            priority=priority,
            title=f"{action_type.value.replace('_', ' ').title()} Action",
            description=f"Recommended for {segment} customer in {journey.current_stage.value} stage",
            confidence=round(confidence, 2),
            expected_impact=round(impact, 1),
            urgency=round(urgency, 1),
            assigned_agent=AGENT_MAPPING.get(action_type, "CustomerSuccessAgent"),
            execution_steps=[
                f"Analyze {action_type.value} opportunity",
                f"Prepare {action_type.value} strategy",
                f"Execute via {AGENT_MAPPING.get(action_type, 'CustomerSuccessAgent')}",
                "Monitor outcome and record results",
            ],
            risk_factors=cls._assess_risks(journey, action_type),
        )

    @classmethod
    def _assess_risks(cls, journey: CustomerJourney, action_type: ActionType) -> List[str]:
        risks = []
        if journey.health == "critical":
            risks.append("Customer in critical health — proceed with care")
        if journey.churn_risk > 0.7:
            risks.append("High churn risk — retention should be prioritized")
        if action_type == ActionType.UPSELL and journey.health != "excellent":
            risks.append("Upsell not recommended unless customer health is excellent")
        support_count = sum(1 for tp in journey.touchpoints if tp.type.value == "support_ticket")
        if support_count > 3:
            risks.append(f"Customer has {support_count} support tickets — address issues first")
        return risks
