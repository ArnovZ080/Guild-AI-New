from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import json
from pydantic import BaseModel, Field

from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm

# --- Data Models (converted to Pydantic for better serialization) ---

class BusinessMetric(BaseModel):
    metric_id: str
    name: str
    value: float
    unit: str
    trend: str
    category: str
    source: str
    timestamp: datetime = Field(default_factory=datetime.now)
    importance_score: float
    target_value: Optional[float] = None
    benchmark_value: Optional[float] = None
    period: str = "monthly"

class KPIMetric(BaseModel):
    kpi_id: str
    name: str
    current_value: float
    previous_value: float
    target_value: float
    unit: str
    category: str
    trend_direction: str  # "up", "down", "stable"
    trend_percentage: float
    status: str  # "excellent", "good", "warning", "critical"
    calculation_method: str
    data_sources: List[str]
    last_updated: datetime = Field(default_factory=datetime.now)
    business_impact: str  # "high", "medium", "low"

class DashboardInsight(BaseModel):
    insight_id: str
    title: str
    description: str
    category: str
    urgency: str
    action_required: bool
    recommendation: str
    supporting_data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)

class BusinessAlert(BaseModel):
    alert_id: str
    type: str
    severity: str
    title: str
    description: str
    action_required: bool
    related_metrics: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)

# --- Agent Implementation ---

class BusinessIntelligenceAgent(BaseAgent):
    """
    Business Intelligence Agent
    Central coordinator of insights across the Guild ecosystem.
    Ported from legacy codebase.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command", "analyze")
        
        if command == "analyze":
            return await self.run_comprehensive_analysis(input_data, context)
        elif command == "get_snapshot":
            return self.generate_ceo_snapshot()
        else:
            # Default fallback
            return await self.run_comprehensive_analysis(input_data, context)

    async def run_comprehensive_analysis(self, input_data: Dict[str, Any], context: Optional[Dict] = None):
        try:
            self.logger.info("Starting comprehensive business intelligence analysis...")
            
            # Setup context parameters
            business_objective = input_data.get("objective", "Provide specific business intelligence for decision making.")
            
            # Interface natively with the Integration Registry and local agents
            data_sources = {
                "financial_agents": ["bookkeeping", "accounting"],
                "content_agents": ["ContentIntelligenceAgent", "CampaignAgent"],
                "customer_agents": ["CustomerIntelligenceAgent"],
                "status": "native_integration_active" 
            }
            
            # 1. Generate Strategy via LLM
            bi_strategy = await self._generate_bi_strategy_llm(business_objective, data_sources)
            
            # 2. Execute Strategy (Simulated execution logic from legacy)
            execution_result = await self._execute_bi_strategy(business_objective, bi_strategy)
            
            # 3. Generate Snapshot
            ceo_snapshot = self.generate_ceo_snapshot()
            
            return {
                "agent": "BusinessIntelligenceAgent",
                "strategy_type": "comprehensive_business_intelligence",
                "bi_strategy": bi_strategy,
                "execution_result": execution_result,
                "ceo_snapshot": ceo_snapshot,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            self.logger.error(f"BI analysis failed: {e}", exc_info=True)
            return {"error": str(e)}

    async def _generate_bi_strategy_llm(self, objective: str, data_sources: Dict) -> Dict:
        """Generates comprehensive strategy using LLM."""
        sys_prompt = "You are the Business Intelligence Agent, the central coordinator of insights for the Guild ecosystem."
        user_prompt = f"""
        **Business Objective:** {objective}
        **Data Sources:** {json.dumps(data_sources)}
        
        **Task:**
        Transform raw data into digestible, actionable intelligence.
        
        **Output Format (JSON):**
        Return a comprehensive JSON object with 'bi_strategy_analysis', 'data_aggregation', 'dashboard_curation', 'prioritization_engine', 'recommendation_system', and 'alert_system' keys.
        """
        
        try:
            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ])
            return self._extract_json(response)
        except Exception as e:
            self.logger.error(f"LLM strategy generation failed: {e}")
            return {"error": "Failed to generate strategy via LLM", "details": str(e)}

    async def _execute_bi_strategy(self, objective: str, strategy: Dict) -> Dict:
        """Execute the BI strategy interactively."""
        # In a real system, this would call other agents. 
        # For migration, we use the logic from the legacy agent which simulates aggregation.
        
        data_aggregation = strategy.get("data_aggregation", {})
        dashboard_curation = strategy.get("dashboard_curation", {})
        prioritization_engine = strategy.get("prioritization_engine", {})
        
        # Simulate aggregation
        metrics = await self._aggregate_cross_agent_data(data_aggregation)
        insights = await self._curate_dashboard_content(dashboard_curation, metrics)
        prioritized = await self._prioritize_insights(prioritization_engine, insights)
        
        return {
            "aggregated_metrics_count": len(metrics),
            "generated_insights": [i.dict() for i in prioritized],
        }

    async def _aggregate_cross_agent_data(self, config: Dict) -> List[BusinessMetric]:
        """Aggregate data (Simulated)."""
        # Ported hardcoded simulation from legacy agent for now
        return [
            BusinessMetric(
                metric_id="rev_001", name="Monthly Recurring Revenue", value=15000.0, unit="USD",
                trend="increasing", category="financial", source="bookkeeping_agent", importance_score=0.9
            ),
            BusinessMetric(
                metric_id="cac_001", name="Customer Acquisition Cost", value=45.0, unit="USD",
                trend="stable", category="customer", source="analytics_agent", importance_score=0.8
            ),
             BusinessMetric(
                metric_id="eff_001", name="Agent Efficiency Score", value=87.5, unit="percent",
                trend="stable", category="operational", source="workflow_manager", importance_score=0.6
            )
        ]

    async def _curate_dashboard_content(self, config: Dict, metrics: List[BusinessMetric]) -> List[DashboardInsight]:
        """Curate insights from metrics."""
        insights = []
        for metric in metrics:
            if metric.importance_score > 0.7:
                insights.append(DashboardInsight(
                    insight_id=f"insight_{metric.metric_id}",
                    title=f"{metric.name} Analysis",
                    description=f"{metric.name} is {metric.value} {metric.unit} ({metric.trend})",
                    category=metric.category,
                    urgency="high" if metric.importance_score > 0.8 else "medium",
                    action_required=metric.trend == "decreasing" and metric.category == "financial",
                    recommendation=f"Monitor {metric.name}",
                    supporting_data={"metric_value": metric.value}
                ))
        return insights

    async def _prioritize_insights(self, config: Dict, insights: List[DashboardInsight]) -> List[DashboardInsight]:
        """Simple pass-through for now, limited to 10."""
        return insights[:10]

    def generate_ceo_snapshot(self) -> Dict[str, Any]:
        """Generate CEO Snapshot with Core KPIs."""
        # Calculate KPIs (ported logic)
        kpis = self._calculate_core_kpis()
        
        return {
            "snapshot_date": datetime.now().isoformat(),
            "overall_health": "Good",
            "kpis": {k: v.dict() for k, v in kpis.items()},
            "summary": "Business is stable with increasing revenue trend."
        }

    def _calculate_core_kpis(self) -> Dict[str, KPIMetric]:
        """Calculate core KPIs (Logic ported from legacy)."""
        # In future, these inputs come from DB/Agents. For now, we keep the verified logic with sample data.
        current_revenue = 150000.0
        previous_revenue = 125000.0
        revenue_growth = ((current_revenue - previous_revenue) / previous_revenue) * 100
        
        return {
            "revenue_growth_rate": KPIMetric(
                kpi_id="rev_growth_001", name="Revenue Growth Rate", current_value=revenue_growth,
                previous_value=15.2, target_value=25.0, unit="percent", category="financial",
                trend_direction="up", trend_percentage=revenue_growth, status="good",
                calculation_method="growth_formula", data_sources=["bookkeeping"], business_impact="high"
            ),
             "net_profit_margin": KPIMetric(
                kpi_id="profit_margin_001", name="Net Profit Margin", current_value=26.6,
                previous_value=24.5, target_value=30.0, unit="percent", category="financial",
                trend_direction="up", trend_percentage=2.1, status="good",
                calculation_method="margin_formula", data_sources=["bookkeeping"], business_impact="high"
            )
        }
        
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Helper to extract JSON from LLM response."""
        try:
            if "```json" in text:
                json_str = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                json_str = text.split("```")[1].split("```")[0].strip()
            elif "{" in text:
                start = text.index("{")
                end = text.rindex("}") + 1
                json_str = text[start:end]
            else:
                return {}
            return json.loads(json_str)
        except Exception:
            return {}

# Register Result
AgentRegistry.register(AgentCapability(
    name="BusinessIntelligenceAgent",
    category="Intelligence",
    capabilities=["analyze_business", "ceo_snapshot", "kpi_tracking"],
    description="Central intelligence coordinator providing CEO snapshots, KPI tracking, and strategic insights.",
    agent_class=BusinessIntelligenceAgent
))
