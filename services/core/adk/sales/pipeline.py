"""
Sales Pipeline Agent.
Consolidates legacy SalesFunnelAgent + OutboundSalesAgent into one focused agent.
Handles funnel design, optimization, outreach strategy, and campaign planning.
"""
import json
import logging
from typing import Dict, Any, List, Optional
from services.core.llm import default_llm
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.customers.journey_tracker import JourneyTracker
from services.core.customers.models import JourneyStage

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Sales Pipeline Strategist for a small business.
You combine deep expertise in sales funnel optimization and outbound sales development.

Your capabilities:
1. FUNNEL DESIGN: Create and optimize conversion funnels (Awareness → Purchase)
2. OUTREACH: Design multi-channel outreach campaigns (email, LinkedIn, cold call)
3. OPTIMIZATION: Analyze funnel performance, identify bottlenecks, recommend improvements
4. PIPELINE MANAGEMENT: Track deals, forecast revenue, manage pipeline health

Always respond with actionable, data-driven recommendations formatted as JSON."""


class SalesPipelineAgent(BaseAgent):
    """
    Expert in sales process optimization, combining funnel strategy
    with outbound sales development.
    
    Replaces legacy:
    - SalesFunnelAgent (764 lines)
    - OutboundSalesAgent (541 lines)
    """

    agent_name = "SalesPipelineAgent"
    agent_type = "Sales"
    capabilities = [
        "design_funnel", "optimize_funnel", "create_outreach",
        "plan_campaign", "analyze_pipeline", "forecast_revenue"
    ]

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        kwargs = input_data.get("kwargs", {})
        if command == "design_funnel":
            return await self.design_funnel(**kwargs)
        elif command == "optimize_funnel":
            return await self.optimize_funnel(**kwargs)
        elif command == "create_outreach":
            return await self.create_outreach(**kwargs)
        elif command == "plan_campaign":
            return await self.plan_campaign(**kwargs)
        elif command == "analyze_pipeline":
            return await self.analyze_pipeline()
        else:
            raise ValueError(f"Unknown command for SalesPipelineAgent: {command}")

    @classmethod
    async def design_funnel(cls, objective: str, target_audience: Dict[str, Any],
                            product: Dict[str, Any]) -> Dict[str, Any]:
        """Design a complete sales funnel for a product/objective."""
        prompt = f"""Design a sales funnel for the following:
Objective: {objective}
Target audience: {json.dumps(target_audience)}
Product: {json.dumps(product)}

Return JSON with: funnel_name, stages (list with name, goal, tactics, conversion_target, content_needed), 
estimated_timeline, kpis, budget_recommendation."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def optimize_funnel(cls, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze funnel performance and generate optimization recommendations."""
        prompt = f"""Analyze this funnel performance and provide optimization recommendations:
{json.dumps(performance_data, indent=2)}

Return JSON with: bottlenecks (list), recommendations (list with stage, action, expected_impact),
priority_actions (top 3), estimated_improvement."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def create_outreach(cls, lead: Dict[str, Any], channel: str = "email",
                              product_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a personalized outreach message for a lead."""
        prompt = f"""Create a personalized {channel} outreach for this lead:
Lead: {json.dumps(lead)}
Product: {json.dumps(product_info or {})}

Return JSON with: subject (if email), message, personalization_notes,
follow_up_schedule (list of days and actions), call_to_action."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def plan_campaign(cls, leads: List[Dict[str, Any]],
                            goals: Dict[str, Any]) -> Dict[str, Any]:
        """Plan a multi-channel outbound campaign for a list of leads."""
        lead_summary = [
            {"name": l.get("name", ""), "company": l.get("company", ""),
             "score": l.get("lead_score", 0)} for l in leads[:20]
        ]
        prompt = f"""Plan a multi-channel outbound campaign:
Leads ({len(leads)} total, top shown): {json.dumps(lead_summary)}
Campaign goals: {json.dumps(goals)}

Return JSON with: campaign_name, channels, segments (list), 
sequence (list of touchpoints with day, channel, action),
metrics_to_track, estimated_results."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def analyze_pipeline(cls) -> Dict[str, Any]:
        """Analyze the current sales pipeline using customer journey data."""
        analytics = JourneyTracker.get_analytics()
        at_risk = JourneyTracker.get_at_risk_customers()

        return {
            "pipeline_health": analytics,
            "at_risk_count": len(at_risk),
            "at_risk_customers": [
                {"id": j.customer_id, "churn_risk": j.churn_risk, "stage": j.current_stage.value}
                for j in at_risk[:10]
            ],
            "stage_distribution": analytics.get("stage_distribution", {}),
            "recommendations": cls._pipeline_recommendations(analytics),
        }

    @classmethod
    def _pipeline_recommendations(cls, analytics: Dict[str, Any]) -> List[str]:
        recs = []
        stages = analytics.get("stage_distribution", {})
        if stages.get("awareness", 0) > stages.get("consideration", 0) * 3:
            recs.append("Top of funnel is bloated — focus on conversion from awareness to consideration")
        if stages.get("churn", 0) > 0:
            recs.append(f"{stages['churn']} churned customers — run retention workflows")
        if analytics.get("avg_churn_risk", 0) > 0.4:
            recs.append("Average churn risk is high — prioritize customer success outreach")
        return recs or ["Pipeline looks healthy — continue current strategy"]

    @classmethod
    def _parse_json(cls, response: str) -> Dict[str, Any]:
        try:
            if "```json" in response:
                return json.loads(response.split("```json")[1].split("```")[0].strip())
            elif "{" in response:
                return json.loads(response[response.index("{"):response.rindex("}") + 1])
        except Exception:
            pass
        return {"raw_response": response}

# Register Agent
AgentRegistry.register(AgentCapability(
    name="SalesPipelineAgent",
    category="Sales",
    capabilities=["design_funnel", "optimize_funnel", "create_outreach", "plan_campaign", "analyze_pipeline", "forecast_revenue"],
    description="Expert in sales process optimization, combining funnel strategy with outbound sales development.",
    agent_class=SalesPipelineAgent
))
