from typing import Any, Dict, List, Optional
from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
import json

class TeamCultureAgent(BaseAgent):
    """
    Team Culture Agent
    Consolidates legacy Skill Development and Wellbeing Workload functionalities.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        
        if command == "analyze_workload":
            return await self.analyze_workload(input_data, context)
        elif command == "recommend_interventions":
            return await self.recommend_interventions(input_data, context)
        elif command == "design_learning_path":
            return await self.design_learning_path(input_data, context)
        else:
            raise ValueError(f"Unknown command for TeamCultureAgent: {command}")

    async def analyze_workload(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Assess team burnout risk based on utilization metrics."""
        team_metrics = input_data.get("metrics", {})
        
        sys_prompt = "You are an Organizational Psychologist. Analyze workload data to determine team health."
        user_prompt = f"""
        **Team Metrics:**
        {json.dumps(team_metrics)}
        
        **Response Format:**
        {{
            "burnout_risk_level": "critical|high|medium|low",
            "overutilized_members": ["string"],
            "underutilized_members": ["string"],
            "productivity_impact": "string",
            "health_score": <0-100>
        }}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def recommend_interventions(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Suggest wellbeing improvements for the team."""
        burnout_factors = input_data.get("burnout_factors", [])
        budget = input_data.get("budget", 0)
        
        sys_prompt = "You are a Head of People & Culture. Recommend interventions to improve team wellbeing."
        user_prompt = f"""
        **Identified Burnout Factors:** {json.dumps(burnout_factors)}
        **Available Budget:** {budget}
        
        **Response Format:**
        {{
            "immediate_actions": ["string"],
            "long_term_strategies": ["string"],
            "estimated_cost": <num>,
            "expected_roi_metrics": ["string"]
        }}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def design_learning_path(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create training programs based on skills gaps."""
        current_skills = input_data.get("current_skills", [])
        required_skills = input_data.get("required_skills", [])
        
        sys_prompt = "You are a Learning & Development Expert. Create personalized learning paths."
        user_prompt = f"""
        **Current Skills:** {json.dumps(current_skills)}
        **Target Skills needed:** {json.dumps(required_skills)}
        
        **Response Format:**
        {{
            "skills_gap_analysis": "string",
            "learning_modules": [
                {{"module_name": "string", "focus": "string", "duration_hours": <num>}}
            ],
            "recommended_resources": ["string"],
            "success_criteria": ["string"]
        }}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    def _extract_json(self, text: str) -> Dict[str, Any]:
        try:
            if "```json" in text:
                json_str = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                json_str = text.split("```")[1].split("```")[0].strip()
            else:
                json_str = text[text.find("{"):text.rfind("}")+1]
            return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"JSON extraction failed: {e}")
            return {"error": "Failed to parse JSON", "raw_response": text}

AgentRegistry.register(AgentCapability(
    name="TeamCultureAgent",
    category="HR",
    capabilities=["analyze_workload", "recommend_interventions", "design_learning_path"],
    description="Monitors team wellbeing, manages workload risks, and designs skill development programs.",
    agent_class=TeamCultureAgent
))
