from typing import Any, Dict, List, Optional
from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.llm import default_llm
from services.core.utils.json_extractor import extract_json_from_llm_response
import json

class TalentAcquisitionAgent(BaseAgent):
    """
    Talent Acquisition Agent
    Consolidates legacy Hiring and Outsourcing functionalities.
    """
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        
        if command == "design_hiring_strategy":
            return await self.design_hiring_strategy(input_data, context)
        elif command == "create_job_description":
            return await self.create_job_description(input_data, context)
        elif command == "screen_cv":
            return await self.screen_cv(input_data, context)
        elif command == "manage_freelancers":
            return await self.manage_freelancers(input_data, context)
        else:
            raise ValueError(f"Unknown command for TalentAcquisitionAgent: {command}")

    async def design_hiring_strategy(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create comprehensive recruitment plans."""
        goals = input_data.get("recruitment_goals", {})
        budget = input_data.get("budget", 0)
        
        base_prompt = "You are an elite Talent Acquisition Strategist. You specialize in employer branding and optimizing recruitment funnels."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        user_prompt = f"""
        Design a hiring strategy for the following goals:
        **Goals:** {json.dumps(goals)}
        **Budget:** {budget}
        
        **Response Format:**
        Think step by step about the specific goals and budget before defining the channels and allocation. Return JSON exactly matching this structure:
        {{
            "strategy_overview": "string",
            "sourcing_channels": ["string"],
            "timeline_weeks": <num>,
            "budget_allocation": {{"job_boards": <num>, "agency_fees": <num>, "other": <num>}},
            "key_metrics": ["string"]
        }}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def create_job_description(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Draft JD based on company context and role requirements."""
        role_title = input_data.get("role_title", "Unknown Role")
        requirements = input_data.get("requirements", [])
        company_context = context or {}
        
        base_prompt = "You are an expert HR Copywriter. You write engaging, inclusive, and branded job descriptions that attract top talent."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        user_prompt = f"""
        **Role Title:** {role_title}
        **Requirements:** {json.dumps(requirements)}
        **Company Context:** {json.dumps(company_context.get('business', 'Unknown'))}
        
        **Response Format:**
        Think step by step about how to structure the responsibilities and benefits to appeal to the target candidate, then return JSON:
        {{
            "job_title": "string",
            "department": "string",
            "mission_summary": "string",
            "responsibilities": ["string"],
            "qualifications": ["string"],
            "benefits": ["string"]
        }}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def screen_cv(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Score candidates against job requirements."""
        cv_text = input_data.get("cv_text", "")
        job_requirements = input_data.get("job_requirements", [])
        
        base_prompt = "You are a Technical Recruiter filtering resumes. You excel at extracting signal from noise and maintaining objective scoring criteria."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        user_prompt = f"""
        **Job Requirements:** {json.dumps(job_requirements)}
        
        **Candidate CV:**
        {cv_text[:4000]} # Truncated
        
        **Response Format:**
        Think step by step about the gaps in the candidate's CV against the requirements before assigning a match_score. Return JSON:
        {{
            "candidate_name": "string",
            "skills_matched": ["string"],
            "skills_missing": ["string"],
            "experience_summary": "string",
            "match_score": <0-100>,
            "recommendation": "proceed|reject|hold"
        }}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    async def manage_freelancers(self, input_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process contractor proposals and setup contracts."""
        project_scope = input_data.get("project_scope", "")
        proposals = input_data.get("proposals", [])
        
        base_prompt = "You are a Freelance Management Specialist. You are skilled at evaluating independent contractors, setting up clear milestones, and maximizing project ROI."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        user_prompt = f"""
        Evaluate these freelance proposals against the project scope.
        **Scope:** {project_scope}
        
        **Proposals:**
        {json.dumps(proposals)}
        
        **Response Format:**
        Think step by step about comparing the proposals based on both cost and expertise, then return JSON:
        {{
            "top_candidate": "string",
            "evaluation_summary": "string",
            "recommended_budget": <num>,
            "contract_milestones": ["string"]
        }}
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        return self._extract_json(response)

    @classmethod
    def _get_fallback_response(cls) -> Dict[str, Any]:
        return {
            "error": "Failed to complete talent acquisition request",
            "strategy_overview": "Strategy generation failed",
            "sourcing_channels": [],
            "budget_allocation": {},
            "key_metrics": [],
            "job_title": "Role setup failed",
            "responsibilities": [],
            "candidate_name": "Unknown",
            "skills_matched": [],
            "top_candidate": "Unknown"
        }

    def _extract_json(self, text: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(text, fallback=self._get_fallback_response())

AgentRegistry.register(AgentCapability(
    name="TalentAcquisitionAgent",
    category="HR",
    capabilities=["design_hiring_strategy", "create_job_description", "screen_cv", "manage_freelancers"],
    description="Manages recruitment, CV screening, and freelancer outsourcing processes.",
    agent_class=TalentAcquisitionAgent
))
