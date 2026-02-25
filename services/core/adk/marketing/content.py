"""
Content Marketing Agent.
Consolidates legacy ContentIntelligenceAgent + ContentStrategist + ContentRepurposerAgent
into a single content powerhouse.
"""
import json
import logging
from typing import Dict, Any, List, Optional
from services.core.llm import default_llm
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Content Marketing Strategist for a small business.
You combine expertise in content strategy, creation, SEO optimization, and repurposing.

Your capabilities:
1. STRATEGY: Build content calendars, editorial plans, and pillar/cluster content maps
2. CREATE: Generate blog posts, social media copy, email sequences, and landing pages
3. OPTIMIZE: SEO-optimize content with keywords, meta descriptions, and structure
4. REPURPOSE: Transform one piece of content into 10+ formats across channels
5. ANALYZE: Evaluate content performance and recommend improvements

Be creative, data-driven, and brand-aware. Always respond as JSON."""


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

    @classmethod
    async def create_strategy(cls, business: Dict[str, Any],
                               audience: Dict[str, Any],
                               goals: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a comprehensive content strategy."""
        prompt = f"""Create a content marketing strategy:
Business: {json.dumps(business)}
Target audience: {json.dumps(audience)}
Goals: {json.dumps(goals or {})}

Return JSON with: strategy_name, pillars (list with topic, subtopics, target_keywords),
content_types (list with type, frequency, channel), editorial_calendar_30d (list with week, topics),
kpis, distribution_plan, estimated_time_investment."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def generate_content(cls, topic: str, content_type: str = "blog_post",
                                audience: Optional[Dict[str, Any]] = None,
                                seo_keywords: Optional[List[str]] = None,
                                tone: str = "professional") -> Dict[str, Any]:
        """Generate a piece of content."""
        prompt = f"""Create a {content_type} about: {topic}
Target audience: {json.dumps(audience or {})}
SEO keywords to include: {json.dumps(seo_keywords or [])}
Tone: {tone}

Return JSON with: title, meta_description, content (full text), 
word_count, seo_score (0-100), tags (list), 
social_snippets (twitter, linkedin, instagram)."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def optimize_seo(cls, content: str, target_keywords: List[str]) -> Dict[str, Any]:
        """SEO-optimize existing content."""
        # Truncate content if too long for prompt
        content_preview = content[:3000] + "..." if len(content) > 3000 else content
        prompt = f"""SEO-optimize this content for these keywords: {json.dumps(target_keywords)}

Content: {content_preview}

Return JSON with: optimized_title, optimized_meta_description, 
heading_structure (list), keyword_density, 
internal_link_suggestions (list), schema_markup_type,
improvements_made (list), estimated_seo_score (0-100)."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def repurpose(cls, original_content: str,
                        target_formats: Optional[List[str]] = None) -> Dict[str, Any]:
        """Repurpose content into multiple formats."""
        formats = target_formats or [
            "twitter_thread", "linkedin_post", "email_newsletter",
            "infographic_outline", "video_script", "podcast_notes"
        ]
        content_preview = original_content[:3000] + "..." if len(original_content) > 3000 else original_content
        prompt = f"""Repurpose this content into these formats: {json.dumps(formats)}

Original: {content_preview}

Return JSON with each format as a key, containing the repurposed content.
Also include: repurposing_notes, distribution_timeline."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return cls._parse_json(response)

    @classmethod
    async def analyze_performance(cls, content_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content performance and recommend improvements."""
        prompt = f"""Analyze this content performance data:
{json.dumps(content_metrics, indent=2)}

Return JSON with: top_performing (list), underperforming (list),
trends, content_gaps, recommendations (list with action, expected_impact),
next_content_suggestions (list)."""

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
    name="ContentMarketingAgent",
    category="Marketing",
    capabilities=["create_strategy", "generate_content", "optimize_seo", "repurpose_content", "analyze_performance"],
    description="Expert in full-lifecycle content marketing.",
    agent_class=ContentMarketingAgent
))
