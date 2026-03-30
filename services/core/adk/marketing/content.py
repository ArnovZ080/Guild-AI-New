"""
Content Marketing Agent.
Consolidates legacy ContentIntelligenceAgent + ContentStrategist + ContentRepurposerAgent
into a single content powerhouse.
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


class ContentMarketingAgent(BaseAgent):
    """
    Expert in full-lifecycle content marketing.
    
    Replaces legacy:
    - ContentIntelligenceAgent (~400 lines)
    - ContentStrategist (~500 lines)
    - ContentRepurposerAgent (~300 lines)
    """

    agent_name = "ContentMarketingAgent"
    agent_type = "Marketing"
    capabilities = [
        "create_strategy", "generate_content", "optimize_seo",
        "repurpose_content", "build_calendar", "analyze_performance"
    ]

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        kwargs = input_data.get("kwargs", {})
        kwargs["context"] = context
        if command == "create_strategy":
            return await self.create_strategy(**kwargs)
        elif command == "generate_content":
            return await self.generate_content(**kwargs)
        elif command == "optimize_seo":
            return await self.optimize_seo(**kwargs)
        elif command == "repurpose":
            return await self.repurpose(**kwargs)
        elif command == "analyze_performance":
            return await self.analyze_performance(**kwargs)
        else:
            raise ValueError(f"Unknown command for ContentMarketingAgent: {command}")

    async def create_strategy(self, business: Dict[str, Any],
                               audience: Dict[str, Any],
                               goals: Optional[Dict[str, Any]] = None,
                               context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a comprehensive content strategy."""
        prompt = f"""Create a content marketing strategy:
Business: {json.dumps(business)}
Target audience: {json.dumps(audience)}
Goals: {json.dumps(goals or {})}

Return JSON with: strategy_name, pillars (list with topic, subtopics, target_keywords),
content_types (list with type, frequency, channel), editorial_calendar_30d (list with week, topics),
kpis, distribution_plan, estimated_time_investment.

Think step by step to map goals to specific topics."""

        base_prompt = "You are a Content Marketing Strategist for a small business. You combine expertise in content strategy, creation, SEO optimization, and repurposing."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def generate_content(self, topic: str, content_type: str = "blog_post",
                                audience: Optional[Dict[str, Any]] = None,
                                seo_keywords: Optional[List[str]] = None,
                                tone: str = "professional",
                                context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a piece of content."""
        prompt = f"""Create a {content_type} about: {topic}
Target audience: {json.dumps(audience or {})}
SEO keywords to include: {json.dumps(seo_keywords or [])}
Tone: {tone}

Return JSON with: title, meta_description, content (full text), 
word_count, seo_score (0-100), tags (list), 
social_snippets (twitter, linkedin, instagram).

Ensure all writing STRICTLY ADHERES to the provided Brand Voice if given in the context. Think step by step about the flow and structure of the content."""

        base_prompt = "You are an expert Copywriter. You write engaging, high-converting content across formats."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def optimize_seo(self, content: str, target_keywords: List[str], context: Optional[Dict] = None) -> Dict[str, Any]:
        """SEO-optimize existing content."""
        # Truncate content if too long for prompt
        content_preview = content[:3000] + "..." if len(content) > 3000 else content
        prompt = f"""SEO-optimize this content for these keywords: {json.dumps(target_keywords)}

Content: {content_preview}

Return JSON with: optimized_title, optimized_meta_description, 
heading_structure (list), keyword_density, 
internal_link_suggestions (list), schema_markup_type,
improvements_made (list), estimated_seo_score (0-100).

Think step by step about strategically placing keywords naturally."""

        base_prompt = "You are a Technical SEO Content Optimizer."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def repurpose(self, original_content: str,
                        target_formats: Optional[List[str]] = None,
                        context: Optional[Dict] = None) -> Dict[str, Any]:
        """Repurpose content into multiple formats."""
        formats = target_formats or [
            "twitter_thread", "linkedin_post", "email_newsletter",
            "infographic_outline", "video_script", "podcast_notes"
        ]
        content_preview = original_content[:3000] + "..." if len(original_content) > 3000 else original_content
        prompt = f"""Repurpose this content into these formats: {json.dumps(formats)}

Original: {content_preview}

Return JSON with each format as a key, containing the repurposed content.
Also include: repurposing_notes, distribution_timeline.

Think step by step to adapt the core message to the unique format constraints."""

        base_prompt = "You are a Content Editor skilled at multi-channel adaptation."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def analyze_performance(self, content_metrics: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze content performance and recommend improvements."""
        prompt = f"""Analyze this content performance data:
{json.dumps(content_metrics, indent=2)}

Return JSON with: top_performing (list), underperforming (list),
trends, content_gaps, recommendations (list with action, expected_impact),
next_content_suggestions (list).

Think step by step to map engagement metrics to strategic gaps."""

        base_prompt = "You are a Content Analyst."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete content marketing request",
            "strategy_name": "Fallback Strategy",
            "pillars": [],
            "content_types": [],
            "title": "Fallback Title",
            "content": "Content generation failed.",
            "optimized_title": "Fallback",
            "improvements_made": [],
            "top_performing": []
        }

    def _parse_json(self, response: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(response, fallback=self._get_fallback_response())

# Register Agent
AgentRegistry.register(AgentCapability(
    name="ContentMarketingAgent",
    category="Marketing",
    capabilities=["create_strategy", "generate_content", "optimize_seo", "repurpose_content", "analyze_performance"],
    description="Expert in full-lifecycle content marketing.",
    agent_class=ContentMarketingAgent
))
