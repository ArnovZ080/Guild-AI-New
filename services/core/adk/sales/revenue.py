"""
Revenue Agent.
Consolidates legacy UpsellCrossSellAgent + ProposalWriterAgent + PricingAgent
into a single revenue-focused agent.
"""
import json
import logging
from typing import Dict, Any, List, Optional
from services.core.llm import default_llm
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Revenue Growth Strategist for a small business.
You combine expertise in upselling, cross-selling, proposal writing, and pricing strategy.

Your capabilities:
1. UPSELL/CROSS-SELL: Identify expansion opportunities in existing accounts
2. PROPOSALS: Create persuasive, tailored business proposals
3. PRICING: Analyze and optimize pricing strategy
4. FORECASTING: Revenue prediction and growth scenario planning

Be specific, ROI-focused, and customer-centric. Always respond as JSON."""


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

    @classmethod
    async def find_upsell_opportunities(cls, customer: Dict[str, Any],
                                         products: Dict[str, Any]) -> Dict[str, Any]:
        """Identify upsell and cross-sell opportunities for a customer."""
        prompt = f"""Analyze this customer for upsell/cross-sell opportunities:
Customer: {json.dumps(customer)}
Product portfolio: {json.dumps(products)}

Return JSON with: opportunities (list with product, rationale, estimated_revenue, 
timing, approach_strategy), risk_factors (list), 
total_potential_revenue, priority_recommendation."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def generate_proposal(cls, client: Dict[str, Any],
                                 project: Dict[str, Any],
                                 pricing: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a tailored business proposal."""
        prompt = f"""Create a business proposal:
Client: {json.dumps(client)}
Project requirements: {json.dumps(project)}
Pricing guidelines: {json.dumps(pricing or {})}

Return JSON with: title, executive_summary, problem_statement, 
proposed_solution, deliverables (list), timeline, 
investment (with breakdown), roi_projection, 
next_steps, terms."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def optimize_pricing(cls, product: Dict[str, Any],
                                market_data: Optional[Dict[str, Any]] = None,
                                competitor_pricing: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze and optimize product pricing strategy."""
        prompt = f"""Optimize pricing strategy:
Product: {json.dumps(product)}
Market data: {json.dumps(market_data or {})}
Competitor pricing: {json.dumps(competitor_pricing or {})}

Return JSON with: recommended_price, pricing_model (flat/tiered/usage/freemium),
price_tiers (list), competitive_position, value_metrics, 
psychological_pricing_tactics, projected_revenue_impact."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def forecast_revenue(cls, historical: Dict[str, Any],
                                pipeline: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate revenue forecast based on historical data and pipeline."""
        prompt = f"""Create a revenue forecast:
Historical performance: {json.dumps(historical)}
Current pipeline: {json.dumps(pipeline or {})}

Return JSON with: forecast_30d, forecast_90d, forecast_12m, 
growth_rate, confidence_level, risk_factors (list), 
growth_levers (list with lever, potential_impact), 
scenarios (optimistic, baseline, pessimistic)."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

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
    name="RevenueAgent",
    category="Sales",
    capabilities=["find_upsell_opportunities", "generate_proposal", "optimize_pricing", "forecast_revenue"],
    description="Expert in revenue expansion — upselling, proposals, pricing, and forecasting.",
    agent_class=RevenueAgent
))
