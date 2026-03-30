from typing import Any, Dict, List, Optional
from datetime import datetime
import json
from pydantic import BaseModel, Field

from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
from services.core.utils.json_extractor import extract_json_from_llm_response

# --- Data Models ---

class MarketingCampaign(BaseModel):
    campaign_id: str
    objective: str
    strategy: Dict[str, Any]
    content_plan: Dict[str, List[str]]
    schedule: List[Dict[str, Any]]
    budget_allocation: Dict[str, float]
    estimated_reach: int
    status: str = "draft"

# --- Agent Implementation ---

class MarketingStrategistAgent(BaseAgent):
    """
    Marketing Strategist Agent
    Creates comprehensive multi-channel marketing campaigns.
    Ported from legacy EnhancedMarketingAgency.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command", "create_campaign")
        
        if command == "create_campaign":
            return await self.create_comprehensive_campaign(input_data, context)
        elif command == "optimize_budget":
            return await self.optimize_budget(input_data)
        else:
            return await self.create_comprehensive_campaign(input_data, context)

    async def create_comprehensive_campaign(self, input_data: Dict[str, Any], context: Optional[Dict] = None):
        try:
            self.logger.info("Starting comprehensive marketing campaign creation...")
            
            objective = input_data.get("objective", "Increase brand awareness")
            campaign_type = input_data.get("campaign_type", "multi_channel") # social, email, ads, multi_channel
            budget = input_data.get("budget", 1000.0)
            
            # Context usually contains brand/business info
            business_context = context or {}
            
            # 1. Generate Strategy
            strategy = await self._generate_strategy(objective, campaign_type, budget, business_context)
            
            # 2. Generate Content Plan (Simulated/LLM)
            content_plan = await self._generate_content_plan(objective, campaign_type, strategy, business_context)
            
            # 3. Generate Schedule
            schedule = self._generate_schedule(campaign_type, strategy)
            
            # 4. Allocate Budget
            budget_allocation = self._optimize_budget_allocation(budget, campaign_type)
            
            return {
                "agent": "MarketingStrategistAgent",
                "campaign": MarketingCampaign(
                    campaign_id=f"camp_{int(datetime.now().timestamp())}",
                    objective=objective,
                    strategy=strategy,
                    content_plan=content_plan,
                    schedule=schedule,
                    budget_allocation=budget_allocation,
                    estimated_reach=strategy.get("estimated_reach", 0)
                ).dict(),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Campaign creation failed: {e}", exc_info=True)
            return {"error": str(e)}

    async def _generate_strategy(self, objective: str, campaign_type: str, budget: float, context: Dict) -> Dict:
        """Generate strategic plan using LLM."""
        brand = context.get("brand", {})
        business = context.get("business", {})
        
        sys_prompt = self.build_system_prompt("You are a Senior Marketing Strategist.", context)
        user_prompt = f"""
        **Objective:** {objective}
        **Type:** {campaign_type}
        **Budget:** ${budget}
        **Business:** {business.get('type', 'Unknown')}
        **Brand Voice:** {brand.get('voice_tone', 'Professional')}
        
        **Task:**
        Create a marketing strategy including objectives, messaging framework, channel mix, and estimated results.
        
        **Output Format (JSON):**
        Return JSON with keys: 'objectives', 'messaging_framework', 'channel_mix', 'estimated_reach' (integer), 'estimated_conversions' (integer).
        
        Think step by step structuring the optimal strategy."""
        
        try:
            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ])
            return self._extract_json(response)
        except Exception as e:
            return {"error": f"Strategy generation failed: {e}"}

    async def _generate_content_plan(self, objective: str, campaign_type: str, strategy: Dict, context: Dict) -> Dict:
        """Generate content ideas using LLM."""
        brand = context.get("brand", {})
        
        sys_prompt = self.build_system_prompt("You are a Creative Content Director.", context)
        user_prompt = f"""
        **Objective:** {objective}
        **Campaign Type:** {campaign_type}
        **Messaging:** {json.dumps(strategy.get('messaging_framework', {}))}
        **Brand Voice:** {brand.get('voice_tone', 'Professional')}
        
        **Task:**
        Generate content ideas for the campaign.
        
        **Output Format (JSON):**
        Return JSON with keys: 'social_posts' (list of strings), 'email_subjects' (list of strings), 'ad_headlines' (list of strings).
        
        Think step by step tailoring ideas to the brand voice and phrasing."""
        
        try:
            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ])
            return self._extract_json(response)
        except Exception as e:
            return {}

    def _generate_schedule(self, campaign_type: str, strategy: Dict) -> List[Dict]:
        """Create simple schedule (Ported logic)."""
        schedule = []
        # Simplified for migration: just returning a sample structure
        start_date = datetime.now()
        schedule.append({"date": start_date.isoformat(), "channel": "social", "type": "announcement"})
        return schedule

    def _optimize_budget_allocation(self, total_budget: float, campaign_type: str) -> Dict[str, float]:
        """Optimize budget (Ported logic)."""
        if campaign_type == "social":
            return {
                "content_creation": total_budget * 0.30,
                "paid_ads": total_budget * 0.50,
                "influencer_outreach": total_budget * 0.10,
                "tools": total_budget * 0.10
            }
        elif campaign_type == "email":
             return {
                "email_platform": total_budget * 0.20,
                "content_creation": total_budget * 0.40,
                "list_growth": total_budget * 0.30,
                "tools": total_budget * 0.10
            }
        else:
             return {
                "social_media": total_budget * 0.35,
                "email_marketing": total_budget * 0.25,
                "content_creation": total_budget * 0.25,
                "tools": total_budget * 0.15
            }

    async def optimize_budget(self, input_data: Dict) -> Dict:
        """Wrapper for direct budget optimization call."""
        budget = input_data.get("budget", 1000.0)
        ctype = input_data.get("campaign_type", "multi_channel")
        return self._optimize_budget_allocation(budget, ctype)

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete strategy generation",
            "objectives": "Increase base metrics",
            "messaging_framework": {"primary": "Value proposition"},
            "channel_mix": ["Digital", "Direct"],
            "estimated_reach": 0,
            "estimated_conversions": 0,
            "social_posts": [],
            "email_subjects": [],
            "ad_headlines": []
        }

    def _extract_json(self, text: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(text, fallback=self._get_fallback_response())

# Register Result
AgentRegistry.register(AgentCapability(
    name="MarketingStrategistAgent",
    category="Marketing",
    capabilities=["create_campaign", "optimize_budget", "marketing_strategy"],
    description="Full-service marketing agency for campaign creation, strategy, and budget optimization.",
    agent_class=MarketingStrategistAgent
))
