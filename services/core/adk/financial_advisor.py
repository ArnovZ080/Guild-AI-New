from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
import json
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm

@dataclass
class FinancialReport:
    """Financial analysis report"""
    profit_loss_summary: Dict[str, Any]
    cash_flow_projection: Dict[str, Any]
    investment_recommendations: List[str]
    risk_assessment: Dict[str, Any]
    action_plan: List[Dict[str, str]]
    key_metrics: Dict[str, float]
    health_score: float  # 0-100

class FinancialAdvisorAgent(BaseAgent):
    """
    Enhanced Financial Advisor Agent
    Ported from legacy ADK for comprehensive financial analysis.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command", "analyze")
        
        if command == "analyze":
            return await self.analyze_business_finances(input_data, context)
        elif command == "forecast":
            return await self.forecast_revenue(input_data)
        elif command == "budget":
            return await self.generate_budget_plan(input_data, context)
        else:
            raise ValueError(f"Unknown command for FinancialAdvisorAgent: {command}")

    async def analyze_business_finances(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive financial analysis using LLM
        """
        try:
            # Context usually comes from the orchestrator (Source of Truth)
            business_context = context or {}
            
            # Input data might contain specific financial data override
            financial_data = input_data.get("financial_data", {})
            
            business = business_context.get("business", {})
            financial = business_context.get("financial", {})
            goals = business_context.get("goals", {})
            
            # Build comprehensive prompt
            sys_prompt = f"You are a sophisticated Financial Advisor for a {business.get('type', 'business')}."
            user_prompt = f"""
            **Current Financial State:**
            - Business Type: {business.get('type', 'Not specified')}
            - Industry: {business.get('industry', 'Not specified')}
            - Pricing Strategy: {financial.get('pricing_status', 'Not specified')}
            - Marketing Budget: {financial.get('marketing_budget', 'Not specified')}
            - Revenue Goals: {financial.get('revenue_goals', 'Not specified')}
            - 3-Month Priority: {goals.get('priority_3months', 'Not specified')}
            
            **Additional Data:**
            {json.dumps(financial_data) if financial_data else 'No additional transaction data provided.'}
            
            **Provide a comprehensive financial analysis in this JSON format:**
            {{
                "profit_loss_summary": {{
                    "current_monthly_revenue": <number>,
                    "projected_monthly_revenue": <number>,
                    "monthly_expenses": <number>,
                    "net_profit_margin": <percentage_number>
                }},
                "cash_flow_projection": {{
                    "next_month": <number>,
                    "next_quarter": <number>,
                    "next_year": <number>,
                    "confidence_level": <0-1>
                }},
                "investment_recommendations": [
                    "Actionable recommendation 1",
                    "Actionable recommendation 2"
                ],
                "risk_assessment": {{
                    "overall_risk_level": "low|medium|high",
                    "key_risks": ["risk 1", "risk 2"],
                    "mitigation_strategies": ["strategy 1", "strategy 2"]
                }},
                "action_plan": [
                    {{"priority": "high", "action": "Action 1", "timeline": "This week"}},
                    {{"priority": "medium", "action": "Action 2", "timeline": "This month"}}
                ],
                "key_metrics": {{
                    "burn_rate": <monthly amount>,
                    "runway_months": <number>,
                    "break_even_point": <amount>,
                    "growth_rate": <percentage>
                }},
                "health_score": <0-100>
            }}
            
            Be specific with numbers. If exact data matches are missing, estimate reasonably based on industry standards for this business type.
            """
            
            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ])
            
            # Parse report
            data = self._extract_json(response)
            return data
            
        except Exception as e:
            self.logger.error(f"Financial analysis failed: {e}")
            return {"error": str(e)}

    async def forecast_revenue(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Forecast revenue based on growth strategy"""
        current_revenue = input_data.get("current_revenue", 0)
        growth_strategy = input_data.get("growth_strategy", "linear growth")
        timeframe_months = input_data.get("timeframe_months", 12)
        
        sys_prompt = "You are a Financial Analyst specializing in revenue forecasting."
        user_prompt = f"""
        **Current Monthly Revenue:** ${current_revenue}
        **Growth Strategy:** {growth_strategy}
        **Forecast Period:** {timeframe_months} months
        
        **Provide monthly revenue projections:**
        Response format: {{"projections": [{{"month": 1, "revenue": 5000, "growth_rate": 0.05}}], "assumptions": ["assumption 1"], "confidence": 0.75}}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def generate_budget_plan(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate optimized budget allocation"""
        monthly_revenue = input_data.get("monthly_revenue", 0)
        business_goals = input_data.get("business_goals", "sustainability")
        business_context = context or {}
        business_type = business_context.get("business", {}).get("type", "business")
        
        sys_prompt = f"You are a Financial Advisor for a {business_type}."
        user_prompt = f"""
        **Monthly Revenue:** ${monthly_revenue}
        **Business Goals:** {business_goals}
        
        **Create an optimized monthly budget allocation.**
        Response format: {{"categories": [{{"name": "Marketing", "percentage": 30, "amount": 1500, "reasoning": "..."}}], "total": {monthly_revenue}}}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from response"""
        try:
            if "```json" in text:
                json_str = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                json_str = text.split("```")[1].split("```")[0].strip()
            elif "{" in text:
                # Naive attempt to find outer brackets
                start = text.index("{")
                end = text.rindex("}") + 1
                json_str = text[start:end]
            else:
                self.logger.warning("No JSON found in LLM response")
                return {"raw_response": text}
            
            return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"JSON extraction failed: {e}")
            return {"error": "Failed to parse JSON", "raw_response": text}

# Register Agent
AgentRegistry.register(AgentCapability(
    name="FinancialAdvisorAgent",
    category="Finance",
    capabilities=["analyze_finances", "forecast_revenue", "budget_planning"],
    description="Provides comprehensive financial analysis, forecasting, and budget planning.",
    agent_class=FinancialAdvisorAgent
))
