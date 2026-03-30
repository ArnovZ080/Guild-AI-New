"""
Growth Agent.
Consolidates legacy SEO agents, PaidAdsAgent, and EventMarketingAgent
into a single growth-focused agent for channel optimization.
"""
import json
import logging
from services.core.utils.json_extractor import extract_json_from_llm_response
from typing import Dict, Any, List, Optional
from services.core.llm import default_llm
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_DEPRECATED = """You are a Growth Marketing Specialist for a small business.
You combine expertise in SEO, paid advertising, social media growth, and event marketing.

Your capabilities:
1. SEO: Technical audits, keyword research, on-page optimization, link building strategy
2. PAID ADS: Google Ads, Facebook/Instagram ads, LinkedIn ads — budgeting, targeting, copy
3. SOCIAL: Organic growth strategy, community building, influencer partnerships
4. EVENTS: Webinar planning, event marketing, virtual summit strategy

Be specific with metrics, budgets, and timelines. Always respond as JSON."""


class GrowthAgent(BaseAgent):
    """
    Expert in multi-channel growth — SEO, paid acquisition, social, and events.
    
    Replaces legacy:
    - SEOAgent (~350 lines)
    - SEOBrandOptimizer (~300 lines)
    - PaidAdsAgent (~400 lines)
    - EventMarketingAgent (~350 lines)
    """

    agent_name = "GrowthAgent"
    agent_type = "Marketing"
    capabilities = [
        "seo_audit", "keyword_research", "plan_ads_campaign",
        "social_strategy", "plan_event", "growth_roadmap"
    ]

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        kwargs = input_data.get("kwargs", {})
        
        # Inject context if available
        if context and "context" not in kwargs:
            kwargs["context"] = context
            
        if command == "seo_audit":
            return await self.seo_audit(**kwargs)
        elif command == "keyword_research":
            return await self.keyword_research(**kwargs)
        elif command == "plan_ads_campaign":
            return await self.plan_ads_campaign(**kwargs)
        elif command == "social_strategy":
            return await self.social_strategy(**kwargs)
        elif command == "plan_event":
            return await self.plan_event(**kwargs)
        elif command == "growth_roadmap":
            return await self.growth_roadmap(**kwargs)
        else:
            raise ValueError(f"Unknown command for GrowthAgent: {command}")

    async def seo_audit(self, website: str,
                        current_metrics: Optional[Dict[str, Any]] = None,
                        context: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform a comprehensive SEO audit."""
        base_prompt = "You are a Growth Marketing Specialist for a small business combining expertise in SEO, paid advertising, social media growth, and event marketing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Perform an SEO audit for: {website}
Current metrics: {json.dumps(current_metrics or {})}

Return JSON with: overall_score (0-100), technical_issues (list with issue, severity, fix),
on_page_improvements (list), content_gaps (list), 
backlink_opportunities (list), local_seo_status,
priority_actions (top 5 with expected_impact), estimated_timeline.

Think step by step evaluating each metric."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def keyword_research(self, business: str, niche: str,
                                competitors: Optional[List[str]] = None,
                                context: Optional[Dict] = None) -> Dict[str, Any]:
        """Research and recommend target keywords."""
        base_prompt = "You are a Growth Marketing Specialist for a small business combining expertise in SEO, paid advertising, social media growth, and event marketing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Keyword research for: {business} in {niche}
Competitors: {json.dumps(competitors or [])}

Return JSON with: primary_keywords (list with keyword, search_volume_estimate, difficulty, intent),
long_tail_keywords (list), content_cluster_map (pillar with subtopics),
quick_wins (low competition, high intent), competitor_gaps.

Think step by step finding niche opportunities."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def plan_ads_campaign(self, objective: str, budget: float,
                                 audience: Dict[str, Any],
                                 platforms: Optional[List[str]] = None,
                                 context: Optional[Dict] = None) -> Dict[str, Any]:
        """Plan a paid advertising campaign across platforms."""
        base_prompt = "You are a Growth Marketing Specialist for a small business combining expertise in SEO, paid advertising, social media growth, and event marketing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Plan a paid advertising campaign:
Objective: {objective}
Budget: ${budget}
Target audience: {json.dumps(audience)}
Platforms: {json.dumps(platforms or ["google", "facebook"])}

Return JSON with: campaign_name, platform_allocation (dict with platform: budget),
ad_sets (list with platform, targeting, ad_copy, cta, landing_page_theme),
bidding_strategy, kpis, estimated_results (impressions, clicks, conversions, cpa),
optimization_schedule, a_b_test_plan.

Think step by step distributing the budget optimally."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def social_strategy(self, business: Dict[str, Any],
                               platforms: Optional[List[str]] = None,
                               goals: Optional[Dict[str, Any]] = None,
                               context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create an organic social media growth strategy."""
        base_prompt = "You are a Growth Marketing Specialist for a small business combining expertise in SEO, paid advertising, social media growth, and event marketing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Create a social media growth strategy:
Business: {json.dumps(business)}
Platforms: {json.dumps(platforms or ["linkedin", "twitter", "instagram"])}
Goals: {json.dumps(goals or {})}

Return JSON with: platform_strategies (dict per platform with posting_frequency, 
content_types, best_times, hashtag_strategy, engagement_tactics),
content_calendar_7d (list), growth_hacks (list),
community_building_plan, influencer_strategy, kpis.

Think step by step aligning content with audience preferences."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def plan_event(self, event_type: str, objective: str,
                          audience: Dict[str, Any],
                          budget: Optional[float] = None,
                          context: Optional[Dict] = None) -> Dict[str, Any]:
        """Plan a marketing event (webinar, workshop, summit, etc.)."""
        base_prompt = "You are a Growth Marketing Specialist for a small business combining expertise in SEO, paid advertising, social media growth, and event marketing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Plan a marketing event:
Type: {event_type}
Objective: {objective}
Target audience: {json.dumps(audience)}
Budget: {f'${budget}' if budget else 'flexible'}

Return JSON with: event_name, format, agenda (list with time, topic, speaker_type),
promotion_plan (channels and timeline), registration_strategy,
follow_up_sequence, success_metrics, estimated_attendance,
content_repurposing_plan.

Think step by step orchestrating the event lifecycle."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def growth_roadmap(self, business: Dict[str, Any],
                              current_channels: Optional[Dict[str, Any]] = None,
                              budget: Optional[float] = None,
                              context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a comprehensive growth roadmap across all channels."""
        base_prompt = "You are a Growth Marketing Specialist for a small business combining expertise in SEO, paid advertising, social media growth, and event marketing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Create a 90-day growth roadmap:
Business: {json.dumps(business)}
Current channels: {json.dumps(current_channels or {})}
Monthly budget: {f'${budget}' if budget else 'flexible'}

Return JSON with: growth_goal, channel_priority (ranked list with channel, rationale, budget_allocation),
month_1 (list of actions), month_2 (list), month_3 (list),
quick_wins (list), key_experiments (list), 
expected_outcomes (traffic, leads, revenue).

Think step by step prioritizing high-impact channels."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete growth request",
            "overall_score": 0,
            "technical_issues": [],
            "on_page_improvements": [],
            "content_gaps": [],
            "primary_keywords": [],
            "campaign_name": "Fallback Campaign",
            "platform_strategies": {},
            "event_name": "Fallback Event",
            "agenda": [],
            "growth_goal": "Optimize strategy",
            "channel_priority": []
        }

    def _parse_json(self, response: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(response, fallback=self._get_fallback_response())

# Register Agent
AgentRegistry.register(AgentCapability(
    name="GrowthAgent",
    category="Marketing",
    capabilities=["seo_audit", "keyword_research", "plan_ads_campaign", "social_strategy", "plan_event", "growth_roadmap"],
    description="Expert in multi-channel growth — SEO, paid acquisition, social, and events.",
    agent_class=GrowthAgent
))
