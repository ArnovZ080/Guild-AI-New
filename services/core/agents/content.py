from typing import Any, Dict, List, Optional
import json
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm

class ContentStrategistAgent(BaseAgent):
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        business_objectives = input_data.get("business_objectives") or [input_data.get("objective")] or [input_data.get("intent")] or [input_data.get("goal")]
        target_audience = input_data.get("target_audience") or input_data.get("audience") or {}
        
        if not any(business_objectives):
             # If strictly nothing, but we have a generic goal from input_data, use that
             if isinstance(input_data, str):
                 business_objectives = [input_data]
             else:
                 raise ValueError("ContentStrategistAgent requires 'business_objectives', 'objective', or 'goal'")

        trend_context = input_data.get("trend_context") or {}
        
        sys_prompt = "You are a Chief Content Strategist. Develop a comprehensive content strategy."
        user_prompt = f"""
        Business Objectives: {business_objectives}
        Target Audience: {json.dumps(target_audience)}
        Trend Context: {json.dumps(trend_context)}
        
        Generate a JSON object with:
        1. strategy_summary (incorporating trends where relevant)
        2. content_calendar (4 weeks)
        3. performance_framework
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        try:
             # Basic cleanup if the LLM adds markdown blocks
            clean_response = response.replace("```json", "").replace("```", "")
            return json.loads(clean_response)
        except json.JSONDecodeError:
            self.logger.error("Failed to parse LLM response as JSON")
            return {"raw_response": response}

class CopywriterAgent(BaseAgent):
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        objective = input_data.get("objective") or input_data.get("intent") or input_data.get("goal") or input_data.get("copy_objective")
        audience = input_data.get("audience") or input_data.get("target_audience") or "General Audience"
        # If content_strategy is not provided, look for it in dependency results if available
        content_strategy = input_data.get("content_strategy", "General Brand Awareness")
        
        if not objective:
             if isinstance(input_data, str):
                 objective = input_data
             else:
                 raise ValueError("CopywriterAgent requires 'objective'")

        sys_prompt = "You are a world-class Copywriter. Write high-converting copy."
        user_prompt = f"""
        Objective: {objective}
        Audience: {audience}
        Strategy Context: {content_strategy}
        
        Output Format:
        - Title
        - Body
        - Key Takeaways
        - Tone of Voice
        """

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        return {"copy": response}

# Register Agents
AgentRegistry.register(AgentCapability(
    name="ContentStrategistAgent",
    category="Content",
    capabilities=["content_strategy", "calendar_creation"],
    description="Generates comprehensive content strategies and calendars.",
    agent_class=ContentStrategistAgent
))

AgentRegistry.register(AgentCapability(
    name="CopywriterAgent",
    category="Content",
    capabilities=["copywriting", "content_creation"],
    description="Generates high-converting copy based on strategies.",
    agent_class=CopywriterAgent
))
