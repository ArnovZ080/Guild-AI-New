"""
Revenue Agent.
Consolidates legacy UpsellCrossSellAgent + ProposalWriterAgent + PricingAgent
into a single revenue-focused agent.
"""
import json
import logging
from services.core.utils.json_extractor import extract_json_from_llm_response
from typing import Dict, Any, List, Optional
from services.core.llm import default_llm
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability

logger = logging.getLogger(__name__)

# Deprecated in favor of build_system_prompt


class RevenueAgent(BaseAgent):
    """
    Expert in revenue expansion — upselling, proposals, pricing, and forecasting.
    
    Replaces legacy:
    - UpsellCrossSellAgent (143 lines)
    - ProposalWriterAgent (209 lines)
    - PricingAgent (~200 lines)
    """

    agent_name = "RevenueAgent"
    agent_type = "Sales"
    capabilities = [
        "find_upsell_opportunities", "generate_proposal",
        "optimize_pricing", "forecast_revenue"
    ]

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        kwargs = input_data.get("kwargs", {})
        kwargs["context"] = context
        if command == "find_upsell_opportunities":
            return await self.find_upsell_opportunities(**kwargs)
        elif command == "generate_proposal":
            return await self.generate_proposal(**kwargs)
        elif command == "optimize_pricing":
            return await self.optimize_pricing(**kwargs)
        elif command == "forecast_revenue":
            return await self.forecast_revenue(**kwargs)
        else:
            raise ValueError(f"Unknown command for RevenueAgent: {command}")

    async def find_upsell_opportunities(self, customer: Dict[str, Any],
                                         products: Dict[str, Any],
                                         context: Optional[Dict] = None) -> Dict[str, Any]:
        """Identify upsell and cross-sell opportunities for a customer."""
        prompt = f"""Analyze this customer for upsell/cross-sell opportunities:
Customer: {json.dumps(customer)}
Product portfolio: {json.dumps(products)}

timing, approach_strategy), risk_factors (list), 
total_potential_revenue, priority_recommendation.

Think step by step about matching unmet needs with product capabilities."""

        base_prompt = "You are a Revenue Operations Strategist focusing on account expansion."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def generate_proposal(self, client: Dict[str, Any],
                                 project: Dict[str, Any],
                                 pricing: Optional[Dict[str, Any]] = None,
                                 context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a tailored business proposal."""
        prompt = f"""Create a business proposal:
Client: {json.dumps(client)}
Project requirements: {json.dumps(project)}
Pricing guidelines: {json.dumps(pricing or {})}

Return JSON with: title, executive_summary, problem_statement, 
proposed_solution, deliverables (list), timeline, 
investment (with breakdown), roi_projection, 
next_steps, terms.

Think step by step to ensure value proposition matches client requirements."""

        base_prompt = "You are an expert Proposal Writer that focuses on ROI and value."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def optimize_pricing(self, product: Dict[str, Any],
                                market_data: Optional[Dict[str, Any]] = None,
                                competitor_pricing: Optional[Dict[str, Any]] = None,
                                context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze and optimize product pricing strategy."""
        prompt = f"""Optimize pricing strategy:
Product: {json.dumps(product)}
Market data: {json.dumps(market_data or {})}
Competitor pricing: {json.dumps(competitor_pricing or {})}

recommended_price, pricing_model (flat/tiered/usage/freemium),
price_tiers (list), competitive_position, value_metrics, 
psychological_pricing_tactics, projected_revenue_impact.

Think step by step on anchoring strategies and value perception."""

        base_prompt = "You are a SaaS Pricing Strategy Expert."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def forecast_revenue(self, historical: Dict[str, Any],
                                pipeline: Optional[Dict[str, Any]] = None,
                                context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate revenue forecast based on historical data and pipeline."""
        prompt = f"""Create a revenue forecast:
Historical performance: {json.dumps(historical)}
Current pipeline: {json.dumps(pipeline or {})}

forecast_30d, forecast_90d, forecast_12m, 
growth_rate, confidence_level, risk_factors (list), 
growth_levers (list with lever, potential_impact), 
scenarios (optimistic, baseline, pessimistic).

Think step by step computing conservative vs optimistic paths."""

        base_prompt = "You are a Data-Driven Revenue Forecaster."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete revenue request",
            "opportunities": [],
            "risk_factors": [],
            "title": "Fallback Proposal",
            "executive_summary": "Proposal failed.",
            "deliverables": [],
            "investment": {},
            "recommended_price": 0,
            "price_tiers": [],
            "forecast_30d": 0,
            "growth_levers": [],
            "scenarios": {}
        }

    def _parse_json(self, response: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(response, fallback=self._get_fallback_response())

# Register Agent
AgentRegistry.register(AgentCapability(
    name="RevenueAgent",
    category="Sales",
    capabilities=["find_upsell_opportunities", "generate_proposal", "optimize_pricing", "forecast_revenue"],
    description="Expert in revenue expansion — upselling, proposals, pricing, and forecasting.",
    agent_class=RevenueAgent
))
