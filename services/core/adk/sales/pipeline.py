"""
Sales Pipeline Agent.
Consolidates legacy SalesFunnelAgent + OutboundSalesAgent into one focused agent.
Handles funnel design, optimization, outreach strategy, and campaign planning.
"""
import json
import logging
from services.core.utils.json_extractor import extract_json_from_llm_response
from typing import Dict, Any, List, Optional
from services.core.llm import default_llm
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.customers.journey_tracker import JourneyTracker
from services.core.customers.models import JourneyStage

logger = logging.getLogger(__name__)

# Deprecated in favor of build_system_prompt


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
        kwargs["context"] = context
        if command == "design_funnel":
            return await self.design_funnel(**kwargs)
        elif command == "optimize_funnel":
            return await self.optimize_funnel(**kwargs)
        elif command == "create_outreach":
            return await self.create_outreach(**kwargs)
        elif command == "plan_campaign":
            return await self.plan_campaign(**kwargs)
        elif command == "analyze_pipeline":
            return await self.analyze_pipeline(context=context)
        else:
            raise ValueError(f"Unknown command for SalesPipelineAgent: {command}")

    async def design_funnel(self, objective: str, target_audience: Dict[str, Any],
                            product: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Design a complete sales funnel for a product/objective."""
        prompt = f"""Design a sales funnel for the following:
Objective: {objective}
Target audience: {json.dumps(target_audience)}
Product: {json.dumps(product)}

Return JSON with: funnel_name, stages (list with name, goal, tactics, conversion_target, content_needed), 
estimated_timeline, kpis, budget_recommendation.

Think step by step to build a seamless customer journey."""

        base_prompt = "You are a Sales Pipeline Strategist and Funnel Architect."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def optimize_funnel(self, performance_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze funnel performance and generate optimization recommendations."""
        prompt = f"""Analyze this funnel performance and provide optimization recommendations:
{json.dumps(performance_data, indent=2)}

Return JSON with: bottlenecks (list), recommendations (list with stage, action, expected_impact),
priority_actions (top 3), estimated_improvement.

Think step by step to identify the stages with highest drop-off and easiest fixes."""

        base_prompt = "You are a Conversion Rate Optimization Specialist focusing on sales funnels."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def create_outreach(self, lead: Dict[str, Any], channel: str = "email",
                              product_info: Optional[Dict[str, Any]] = None,
                              context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a personalized outreach message for a lead."""
        prompt = f"""Create a personalized {channel} outreach for this lead:
Lead: {json.dumps(lead)}
Product: {json.dumps(product_info or {})}

Return JSON with: subject (if email), message, personalization_notes,
follow_up_schedule (list of days and actions), call_to_action.

Think step by step about positioning the product to solve their specific pain points."""

        base_prompt = "You are a top-tier Sales Development Representative."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def plan_campaign(self, leads: List[Dict[str, Any]],
                            goals: Dict[str, Any],
                            context: Optional[Dict] = None) -> Dict[str, Any]:
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
metrics_to_track, estimated_results.

Think step by step about creating coherent multi-channel touchpoints."""

        base_prompt = "You are an Outbound Campaign Architect."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def analyze_pipeline(self, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze the current sales pipeline using customer journey data."""
        user_id = context.get("user_id", "default_user") if context else "default_user"
        db = context.get("db") if context else None
        
        analytics = await JourneyTracker.get_analytics(db, user_id)
        at_risk = await JourneyTracker.get_at_risk_customers(db, user_id)

        return {
            "pipeline_health": analytics,
            "at_risk_count": len(at_risk),
            "at_risk_customers": [
                {"id": j.customer_id, "churn_risk": j.churn_risk, "stage": j.current_stage.value}
                for j in at_risk[:10]
            ],
            "stage_distribution": analytics.get("stage_distribution", {}),
            "recommendations": self._pipeline_recommendations(analytics),
        }

    def _pipeline_recommendations(self, analytics: Dict[str, Any]) -> List[str]:
        recs = []
        stages = analytics.get("stage_distribution", {})
        if stages.get("awareness", 0) > stages.get("consideration", 0) * 3:
            recs.append("Top of funnel is bloated — focus on conversion from awareness to consideration")
        if stages.get("churn", 0) > 0:
            recs.append(f"{stages['churn']} churned customers — run retention workflows")
        if analytics.get("avg_churn_risk", 0) > 0.4:
            recs.append("Average churn risk is high — prioritize customer success outreach")
        return recs or ["Pipeline looks healthy — continue current strategy"]

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete pipeline request",
            "funnel_name": "Fallback Funnel",
            "stages": [],
            "bottlenecks": [],
            "recommendations": [],
            "subject": "Missing Subject",
            "message": "Outreach message fallback",
            "campaign_name": "Fallback Campaign",
            "sequence": []
        }

    def _parse_json(self, response: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(response, fallback=self._get_fallback_response())

# Register Agent
AgentRegistry.register(AgentCapability(
    name="SalesPipelineAgent",
    category="Sales",
    capabilities=["design_funnel", "optimize_funnel", "create_outreach", "plan_campaign", "analyze_pipeline", "forecast_revenue"],
    description="Expert in sales process optimization, combining funnel strategy with outbound sales development.",
    agent_class=SalesPipelineAgent
))
