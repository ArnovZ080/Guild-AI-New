"""
Campaign Agent.
Handles marketing campaign orchestration, automation sequences,
A/B testing, and cross-channel analytics.
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



class CampaignAgent(BaseAgent):
    """
    Expert in campaign management — orchestration, automation, testing, and analytics.
    
    Replaces legacy:
    - MarketingAgent (~300 lines)
    - EnhancedMarketingAgent (~500 lines)
    - EnhancedMarketingAgency (~600 lines)
    """

    agent_name = "CampaignAgent"
    agent_type = "Marketing"
    capabilities = [
        "design_campaign", "build_automation", "design_ab_test",
        "analyze_campaign", "optimize_campaign", "attribution_report"
    ]

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        kwargs = input_data.get("kwargs", {})
        kwargs["context"] = context
        if command == "design_campaign":
            return await self.design_campaign(**kwargs)
        elif command == "build_automation":
            return await self.build_automation(**kwargs)
        elif command == "design_ab_test":
            return await self.design_ab_test(**kwargs)
        elif command == "analyze_campaign":
            return await self.analyze_campaign(**kwargs)
        elif command == "optimize_campaign":
            return await self.optimize_campaign(**kwargs)
        else:
            raise ValueError(f"Unknown command for CampaignAgent: {command}")

    async def design_campaign(self, objective: str, audience: Dict[str, Any],
                               channels: Optional[List[str]] = None,
                               budget: Optional[float] = None,
                               duration_days: int = 30,
                               context: Optional[Dict] = None) -> Dict[str, Any]:
        """Design a complete marketing campaign."""
        prompt = f"""Design a marketing campaign:
Objective: {objective}
Audience: {json.dumps(audience)}
Channels: {json.dumps(channels or ["email", "social", "content"])}
Budget: {f'${budget}' if budget else 'flexible'}
Duration: {duration_days} days

Return JSON with: campaign_name, theme, channels (list with channel, role, budget_pct),
timeline (list with week, activities, milestones), 
messaging_framework (value_prop, key_messages, cta),
content_needed (list), success_metrics, 
launch_checklist (list), risk_mitigation.

First, think step by step to build a cohesive campaign strategy."""
        
        base_prompt = "You are a Marketing Campaign Manager for a small business. You combine expertise in campaign orchestration, marketing automation, A/B testing, and analytics."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def build_automation(self, trigger: str, objective: str,
                                audience_segment: str,
                                steps: int = 5,
                                context: Optional[Dict] = None) -> Dict[str, Any]:
        """Build a marketing automation sequence (email drip, nurture, etc.)."""
        prompt = f"""Create a {steps}-step marketing automation sequence:
Trigger event: {trigger}
Objective: {objective}
Audience segment: {audience_segment}

Return JSON with: sequence_name, trigger_event, 
steps (list with day, channel, subject, content_summary, cta, 
personalization_tokens, exit_conditions),
branching_rules (list), conversion_goal, 
estimated_conversion_rate, optimization_notes.

Think step by step about the user journey before defining the steps."""

        base_prompt = "You are an expert Automation Specialist building high-converting email and SMS sequences."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def design_ab_test(self, element: str, hypothesis: str,
                              current_version: Optional[str] = None,
                              context: Optional[Dict] = None) -> Dict[str, Any]:
        """Design an A/B test for a marketing element."""
        prompt = f"""Design an A/B test:
Element to test: {element}
Hypothesis: {hypothesis}
Current version (control): {current_version or 'Not provided'}

Return JSON with: test_name, hypothesis, control_description, 
variants (list with name, change, rationale),
primary_metric, secondary_metrics (list), 
sample_size_needed, duration_days, 
significance_threshold, implementation_notes.

Think step by step ensuring statistical rigor."""

        base_prompt = "You are a Conversion Rate Optimization (CRO) expert."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def analyze_campaign(self, campaign_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze campaign performance across channels."""
        prompt = f"""Analyze this campaign's performance:
{json.dumps(campaign_data, indent=2)}

Return JSON with: overall_roi, channel_performance (dict per channel with metrics),
top_performing_content, underperforming_elements,
audience_insights, optimization_recommendations (list with action, expected_impact),
next_campaign_suggestions.

Think step by step through the cross-channel attribution before answering."""

        base_prompt = "You are a Marketing Data Analyst expert in deciphering campaign ROI."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def optimize_campaign(self, campaign: Dict[str, Any],
                                 performance: Dict[str, Any],
                                 context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate real-time optimization recommendations for a running campaign."""
        prompt = f"""Optimize this running campaign based on performance data:
Campaign: {json.dumps(campaign)}
Performance so far: {json.dumps(performance)}

Return JSON with: immediate_actions (list with action, channel, rationale),
budget_reallocation (dict), messaging_adjustments (list),
audience_refinements, content_swaps (list), 
expected_improvement, risk_assessment.

Think step by step on what tweaks will generate the highest immediate impact."""

        base_prompt = "You are a Campaign Optimizer known for rescuing underperforming ads instantly."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete campaign request",
            "campaign_name": "Fallback Campaign",
            "channels": [],
            "timeline": [],
            "messaging_framework": {},
            "content_needed": [],
            "sequence_name": "Fallback Sequence",
            "steps": [],
            "test_name": "Fallback Test",
            "variants": [],
            "optimization_recommendations": []
        }

    def _parse_json(self, response: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(response, fallback=self._get_fallback_response())

# Register Agent
AgentRegistry.register(AgentCapability(
    name="CampaignAgent",
    category="Marketing",
    capabilities=["design_campaign", "build_automation", "design_ab_test", "analyze_campaign", "optimize_campaign"],
    description="Handles marketing campaign orchestration, automation sequences, A/B testing, and cross-channel analytics.",
    agent_class=CampaignAgent
))
