from typing import Any, Dict, List, Optional
from datetime import datetime
import json
from pydantic import BaseModel, Field

from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
from services.core.utils.json_extractor import extract_json_from_llm_response

# --- Data Models ---

class CustomerProfile(BaseModel):
    customer_id: str
    name: str
    email: str
    segment: str
    lifetime_value: float
    churn_risk: str  # "low", "medium", "high"
    sentiment_score: float
    last_activity: datetime = Field(default_factory=datetime.now)

class CustomerSegment(BaseModel):
    segment_id: str
    name: str
    criteria: Dict[str, Any]
    customer_count: int
    recommended_actions: List[str]

# --- Agent Implementation ---

class CustomerIntelligenceAgent(BaseAgent):
    """
    Customer Intelligence Agent
    Manages customer relationships, retention, and insights.
    Ported from legacy codebase.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command", "analyze")
        
        if command == "analyze":
            return await self.run_comprehensive_strategy(input_data, context)
        elif command == "segment":
            return await self.analyze_segments(input_data)
        elif command == "churn_prediction":
            return await self.predict_churn(input_data)
        else:
            return await self.run_comprehensive_strategy(input_data, context)

    async def run_comprehensive_strategy(self, input_data: Dict[str, Any], context: Optional[Dict] = None):
        try:
            self.logger.info("Starting comprehensive customer intelligence analysis...")
            objective = input_data.get("objective", "Improve customer retention and satisfaction.")
            
            # Interface natively with the IntegrationRegistry and ADK
            data_sources = {
                "crm": "native_crm_bridge_active",
                "support": "native_support_bridge_active",
                "social": "native_social_bridge_active"
            }
            
            # 1. Generate Strategy via LLM
            cust_strategy = await self._generate_strategy_llm(objective, data_sources, context)
            
            # 2. Simulate Execution results
            segments = await self.analyze_segments(input_data)
            churn_risk = await self.predict_churn(input_data)
            
            return {
                "agent": "CustomerIntelligenceAgent",
                "strategy": cust_strategy,
                "segments": segments,
                "churn_risk_analysis": churn_risk,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Customer Analysis failed: {e}", exc_info=True)
            return {"error": str(e)}

    async def _generate_strategy_llm(self, objective: str, data_sources: Dict, context: Optional[Dict] = None) -> Dict:
        """Generates comprehensive strategy using LLM."""
        base_prompt = "You are the Customer Intelligence Agent, responsible for customer success and retention. You utilize frameworks like RFM (Recency, Frequency, Monetary value) and NPS analysis to map customer journeys and prevent churn."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        user_prompt = f"""
        **Objective:** {objective}
        **Data Sources:** {json.dumps(data_sources)}
        
        **Task:**
        Create a customer intelligence strategy including data unification, journey mapping, and retention tactics.
        
        **Output Format (JSON):**
        Return a JSON object exactly matching this structure:
        {{
            "strategy_analysis": "Overview of approach",
            "data_unification": ["step 1", "step 2"],
            "journey_tracking": {{"milestones": []}},
            "retention_management": {{"tactics": []}}
        }}
        
        Think step by step extracting actionable insights."""
        
        try:
            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ])
            return self._extract_json(response)
        except Exception as e:
            return {"error": f"LLM generation failed: {e}"}

    async def analyze_segments(self, input_data: Dict) -> List[Dict]:
        """Analyze customer base and create segments (Simulated)."""
        # In real system, query DB/CRM.
        return [
            CustomerSegment(
                segment_id="seg_001", name="High Value Loyalists", 
                criteria={"ltv": ">1000", "tenure": ">12m"}, customer_count=150,
                recommended_actions=["VIP Support", "Early Access"]
            ).dict(),
            CustomerSegment(
                segment_id="seg_002", name="At-Risk Churn", 
                criteria={"last_activity": ">30d", "sentiment": "negative"}, customer_count=45,
                recommended_actions=["Re-engagement Campaign", "Direct Outreach"]
            ).dict()
        ]

    async def predict_churn(self, input_data: Dict) -> Dict:
        """Predict churn risk (Simulated)."""
        return {
            "overall_churn_risk": "medium",
            "risk_factors": ["low_engagement", "support_ticket_spike"],
            "at_risk_count": 45,
            "prevention_strategy": "Launch automated win-back sequence for 'At-Risk Churn' segment."
        }
        
    @classmethod
    def _get_fallback_response(cls) -> Dict[str, Any]:
        return {
            "strategy_analysis": "Fallback strategy due to generation failure",
            "data_unification": [],
            "journey_tracking": {},
            "retention_management": {}
        }
        
    def _extract_json(self, text: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(text, fallback=self._get_fallback_response())

# Register Result
AgentRegistry.register(AgentCapability(
    name="CustomerIntelligenceAgent",
    category="Customer",
    capabilities=["analyze_customers", "segmentation", "churn_prediction"],
    description="Customer success manager for retention, segmentation, and churn prediction.",
    agent_class=CustomerIntelligenceAgent
))
