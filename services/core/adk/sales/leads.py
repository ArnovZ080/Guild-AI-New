"""
Lead Agent.
Consolidates legacy LeadPersonalizationAgent (714 lines) into focused lead
qualification, scoring, and personalized outreach generation.
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


class LeadAgent(BaseAgent):
    """
    Expert in lead intelligence — qualification, scoring, and personalization.
    
    Replaces legacy:
    - LeadPersonalizationAgent (714 lines)
    """

    agent_name = "LeadAgent"
    agent_type = "Sales"
    capabilities = [
        "qualify_lead", "score_leads", "personalize_outreach",
        "segment_leads", "batch_personalize"
    ]

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        kwargs = input_data.get("kwargs", {})
        kwargs["context"] = context
        if command == "qualify":
            return await self.qualify(**kwargs)
        elif command == "score":
            return self.score(**kwargs)
        elif command == "personalize":
            return await self.personalize(**kwargs)
        elif command == "batch_personalize":
            return await self.batch_personalize(**kwargs)
        else:
            raise ValueError(f"Unknown command for LeadAgent: {command}")

    async def qualify(self, lead: Dict[str, Any],
                      icp: Optional[Dict[str, Any]] = None,
                      context: Optional[Dict] = None) -> Dict[str, Any]:
        """Qualify a lead against the Ideal Customer Profile."""
        prompt = f"""Qualify this lead against our ICP:
Lead: {json.dumps(lead)}
ICP criteria: {json.dumps(icp or {"industry": "any", "company_size": "1-500", "budget": "any"})}

Return JSON with: qualified (bool), score (0-100), fit_analysis, 
strengths (list), gaps (list), recommended_action, priority (hot/warm/cold).

Think step by step about firmographic and ICP alignment."""

        base_prompt = "You are a Lead Intelligence Specialist. You score and qualify leads based on intent and fit."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    def score(self, lead: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Fast heuristic lead scoring (no LLM needed)."""
        score = 0
        factors = []

        # Firmographic signals
        if lead.get("company_size", 0) > 10:
            score += 15
            factors.append("Company size > 10")
        if lead.get("industry") in ["technology", "saas", "finance", "healthcare"]:
            score += 20
            factors.append(f"Industry match: {lead.get('industry')}")
        if lead.get("title", "").lower() in ["ceo", "cto", "cfo", "vp", "director", "head", "founder"]:
            score += 25
            factors.append(f"Decision-maker title: {lead.get('title')}")

        # Behavioral signals
        if lead.get("website_visits", 0) > 3:
            score += 15
            factors.append(f"{lead.get('website_visits')} website visits")
        if lead.get("content_downloads", 0) > 0:
            score += 15
            factors.append("Downloaded content")
        if lead.get("demo_requested"):
            score += 30
            factors.append("Demo requested")
        if lead.get("email_opens", 0) > 2:
            score += 10
            factors.append("Engaged with emails")

        # Priority
        if score >= 70:
            priority = "hot"
        elif score >= 40:
            priority = "warm"
        else:
            priority = "cold"

        return {
            "lead_score": min(100, score),
            "priority": priority,
            "scoring_factors": factors,
            "recommended_action": {
                "hot": "Immediate outreach — schedule call",
                "warm": "Nurture with targeted content",
                "cold": "Add to awareness campaign",
            }[priority]
        }

    async def personalize(self, lead: Dict[str, Any], channel: str = "email",
                          product: Optional[Dict[str, Any]] = None,
                          sender: Optional[Dict[str, Any]] = None,
                          context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a deeply personalized outreach message."""
        prompt = f"""Create a personalized {channel} outreach message.

Lead: {json.dumps(lead)}
Product/Service: {json.dumps(product or {})}
Sender info: {json.dumps(sender or {})}

Use these sales psychology principles:
- Reciprocity: Offer value before asking
- Social proof: Reference similar companies
- Scarcity: Create genuine urgency if applicable
- Authority: Establish expertise subtly

Return JSON with: subject (for email), message, personalization_points (list),
psychology_principles_used (list), follow_up_timing, call_to_action.

Think step by step about which psychological principles map best to this lead's profile."""

        base_prompt = "You are a Sales Copywriter expert in highly-personalized B2B outreach."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def batch_personalize(self, leads: List[Dict[str, Any]],
                                channel: str = "email",
                                product: Optional[Dict[str, Any]] = None,
                                context: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Personalize outreach for multiple leads."""
        results = []
        for lead in leads:
            scored = self.score(lead, context=context)
            if scored["priority"] != "cold":
                personalized = await self.personalize(lead, channel, product, context=context)
                results.append({
                    "lead": lead.get("name", lead.get("email", "unknown")),
                    "score": scored,
                    "outreach": personalized,
                })
        return results

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete lead intelligence",
            "qualified": False,
            "score": 0,
            "fit_analysis": "Fallback analysis",
            "strengths": [],
            "gaps": [],
            "recommended_action": "None",
            "priority": "cold",
            "subject": "Missing Subject",
            "message": "Fallback message",
            "personalization_points": []
        }

    def _parse_json(self, response: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(response, fallback=self._get_fallback_response())

# Register Agent
AgentRegistry.register(AgentCapability(
    name="LeadAgent",
    category="Sales",
    capabilities=["qualify_lead", "score_leads", "personalize_outreach", "segment_leads", "batch_personalize"],
    description="Expert in lead intelligence — qualification, scoring, and personalization.",
    agent_class=LeadAgent
))
