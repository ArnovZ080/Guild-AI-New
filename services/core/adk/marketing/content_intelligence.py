from typing import Any, Dict, List, Optional
from datetime import datetime
import json
from pydantic import BaseModel, Field

from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
from services.core.utils.json_extractor import extract_json_from_llm_response

# --- Data Models ---

class ContentMetric(BaseModel):
    platform: str
    content_id: str
    type: str
    engagement_rate: float
    ctr: float
    reach: int
    sentiment: str
    published_at: datetime = Field(default_factory=datetime.now)

class ContentStrategy(BaseModel):
    theme: str
    target_audience: str
    platforms: List[str]
    pillars: List[str]
    recommended_formats: List[str]

# --- Agent Implementation ---

class ContentIntelligenceAgent(BaseAgent):
    """
    Content Intelligence Agent
    Manages content performance tracking, cross-platform strategy, and content gap analysis.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command", "analyze_content")
        
        if command == "analyze_content":
            return await self.analyze_performance(input_data, context)
        elif command == "generate_strategy":
            return await self.generate_strategy(input_data, context)
        else:
            return await self.analyze_performance(input_data, context)

    async def analyze_performance(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze content performance across channels."""
        self.logger.info("Starting content intelligence analysis...")
        
        prompt = f"""You are the Content Intelligence Agent.
Analyze the following content performance criteria and provide insights on engagement, ROI, and content gaps.
Input: {json.dumps(input_data)}

Return JSON with keys: 'top_performing_themes', 'underperforming_platforms', 'content_gaps', 'roi_analysis'.

Think step by step before emitting the JSON structure.
"""
        try:
            base_prompt = "You are the expert Content Intelligence Agent. You analyze complex engagement metrics to uncover high-ROI opportunities."
            sys_prompt = self.build_system_prompt(base_prompt, context)
            
            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ])
            analysis = self._extract_json(response)
            return {
                "status": "success",
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Content Analysis failed: {e}")
            return {"error": str(e)}

    async def generate_strategy(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a multi-platform content strategy."""
        objective = input_data.get("objective", "Increase brand awareness and lead generation.")
        
        prompt = f"""You are the Content Intelligence Agent.
Generate a holistic content strategy.
Objective: {objective}

Return JSON matching this structure:
{{
    "theme": "string",
    "target_audience": "string",
    "platforms": ["string"],
    "pillars": ["string"],
    "recommended_formats": ["string"]
}}

Think step by step about the specific audiences and platforms before generating the strategy.
"""
        try:
            base_prompt = "You are the expert Content Intelligence Agent. You build data-backed core content strategies."
            sys_prompt = self.build_system_prompt(base_prompt, context)
            
            response = await default_llm.chat_completion([
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ])
            strategy_data = self._extract_json(response)
            strategy = ContentStrategy(**strategy_data)
            return {
                "status": "success",
                "strategy": strategy.model_dump(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Strategy generation failed: {e}")
            return {"error": str(e)}

    @classmethod
    def _get_fallback_response(cls) -> Dict[str, Any]:
        return {
            "error": "Failed to generate content intelligence",
            "top_performing_themes": [],
            "underperforming_platforms": [],
            "content_gaps": [],
            "roi_analysis": {},
            "theme": "Fallback Theme",
            "target_audience": "General Audience",
            "platforms": [],
            "pillars": [],
            "recommended_formats": []
        }

    def _extract_json(self, text: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(text, fallback=self._get_fallback_response())

# Register Result
AgentRegistry.register(AgentCapability(
    name="ContentIntelligenceAgent",
    category="Intelligence",
    capabilities=["analyze_content", "content_strategy", "performance_tracking"],
    description="Content performance tracking, cross-platform strategy, and content gap analysis.",
    agent_class=ContentIntelligenceAgent
))
