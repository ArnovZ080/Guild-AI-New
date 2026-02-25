"""
Campaign Agent.
Handles marketing campaign orchestration, automation sequences,
A/B testing, and cross-channel analytics.
"""
import json
import logging
from typing import Dict, Any, List, Optional
from services.core.llm import default_llm
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Marketing Campaign Manager for a small business.
You combine expertise in campaign orchestration, marketing automation, A/B testing, and analytics.

Your capabilities:
1. ORCHESTRATE: Design and manage multi-channel marketing campaigns
2. AUTOMATE: Build email sequences, drip campaigns, and trigger-based workflows
3. TEST: Design and analyze A/B tests for messages, subject lines, and landing pages
4. ANALYZE: Cross-channel attribution, ROI tracking, and performance optimization

Be data-driven, specific with metrics, and focused on ROI. Always respond as JSON."""


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

    @classmethod
    async def design_campaign(cls, objective: str, audience: Dict[str, Any],
                               channels: Optional[List[str]] = None,
                               budget: Optional[float] = None,
                               duration_days: int = 30) -> Dict[str, Any]:
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
launch_checklist (list), risk_mitigation."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def build_automation(cls, trigger: str, objective: str,
                                audience_segment: str,
                                steps: int = 5) -> Dict[str, Any]:
        """Build a marketing automation sequence (email drip, nurture, etc.)."""
        prompt = f"""Create a {steps}-step marketing automation sequence:
Trigger event: {trigger}
Objective: {objective}
Audience segment: {audience_segment}

Return JSON with: sequence_name, trigger_event, 
steps (list with day, channel, subject, content_summary, cta, 
personalization_tokens, exit_conditions),
branching_rules (list), conversion_goal, 
estimated_conversion_rate, optimization_notes."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def design_ab_test(cls, element: str, hypothesis: str,
                              current_version: Optional[str] = None) -> Dict[str, Any]:
        """Design an A/B test for a marketing element."""
        prompt = f"""Design an A/B test:
Element to test: {element}
Hypothesis: {hypothesis}
Current version (control): {current_version or 'Not provided'}

Return JSON with: test_name, hypothesis, control_description, 
variants (list with name, change, rationale),
primary_metric, secondary_metrics (list), 
sample_size_needed, duration_days, 
significance_threshold, implementation_notes."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def analyze_campaign(cls, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze campaign performance across channels."""
        prompt = f"""Analyze this campaign's performance:
{json.dumps(campaign_data, indent=2)}

Return JSON with: overall_roi, channel_performance (dict per channel with metrics),
top_performing_content, underperforming_elements,
audience_insights, optimization_recommendations (list with action, expected_impact),
next_campaign_suggestions."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def optimize_campaign(cls, campaign: Dict[str, Any],
                                 performance: Dict[str, Any]) -> Dict[str, Any]:
        """Generate real-time optimization recommendations for a running campaign."""
        prompt = f"""Optimize this running campaign based on performance data:
Campaign: {json.dumps(campaign)}
Performance so far: {json.dumps(performance)}

Return JSON with: immediate_actions (list with action, channel, rationale),
budget_reallocation (dict), messaging_adjustments (list),
audience_refinements, content_swaps (list), 
expected_improvement, risk_assessment."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    def _parse_json(cls, response: str) -> Dict[str, Any]:
        try:
            if "```json" in response:
                return json.loads(response.split("```json")[1].split("```")[0].strip())
            elif "{" in response:
                return json.loads(response[response.index("{"):response.rindex("}") + 1])
        except Exception:
            pass
        return {"raw_response": response}

# Register Agent
AgentRegistry.register(AgentCapability(
    name="CampaignAgent",
    category="Marketing",
    capabilities=["design_campaign", "build_automation", "design_ab_test", "analyze_campaign", "optimize_campaign"],
    description="Handles marketing campaign orchestration, automation sequences, A/B testing, and cross-channel analytics.",
    agent_class=CampaignAgent
))
