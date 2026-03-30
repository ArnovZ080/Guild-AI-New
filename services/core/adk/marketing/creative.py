"""
Creative Agent.
Covers image generation, visual asset creation, and brand design —
closing the gap left by the legacy ImageGenerationAgent.
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


class CreativeAgent(BaseAgent):
    """
    Expert in visual content — AI image prompting, brand design, and ad creatives.

    Replaces legacy:
    - ImageGenerationAgent
    """

    agent_name = "CreativeAgent"
    agent_type = "Marketing"
    capabilities = [
        "generate_image_prompt", "design_brand_identity",
        "create_ad_visuals", "visual_strategy", "batch_generate"
    ]

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        kwargs = input_data.get("kwargs", {})
        kwargs["context"] = context
        if command == "generate_image_prompt":
            return await self.generate_image_prompt(**kwargs)
        elif command == "design_brand_identity":
            return await self.design_brand_identity(**kwargs)
        elif command == "create_ad_visuals":
            return await self.create_ad_visuals(**kwargs)
        elif command == "visual_strategy":
            return await self.visual_strategy(**kwargs)
        elif command == "batch_generate":
            return await self.batch_generate(**kwargs)
        else:
            raise ValueError(f"Unknown command for CreativeAgent: {command}")

    async def generate_image_prompt(self, concept: str,
                                     style: str = "photorealistic",
                                     platform: str = "general",
                                     dimensions: Optional[str] = None,
                                     context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate optimized prompts for AI image generation tools."""
        prompt = f"""Create an AI image generation prompt for:
Concept: {concept}
Style: {style}
Platform: {platform}
Dimensions: {dimensions or 'flexible'}

Return JSON with:
- dall_e_prompt: optimized prompt for DALL-E (max 400 chars, descriptive)
- midjourney_prompt: optimized prompt for Midjourney (with style params like --ar, --v)
- stable_diffusion_prompt: optimized prompt with positive and negative prompts
- recommended_dimensions: width x height for chosen platform
- style_keywords: list of style modifiers used
- variations: 3 alternative concept angles

Think step by step about the visual composition and lighting before generating the prompts."""

        base_prompt = "You are a prompt engineering expert for visual AI models."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def design_brand_identity(self, business: Dict[str, Any],
                                      values: Optional[List[str]] = None,
                                      industry: Optional[str] = None,
                                      context: Optional[Dict] = None) -> Dict[str, Any]:
        """Design a complete brand identity system."""
        prompt = f"""Design a brand identity system for:
Business: {json.dumps(business)}
Core values: {json.dumps(values or [])}
Industry: {industry or 'general'}

Return JSON with:
- color_palette: primary, secondary, accent, neutral (hex codes + names)
- typography: heading_font, body_font, accent_font (with Google Fonts suggestions)
- logo_concept: description of 3 logo directions with rationale
- mood_board_keywords: list of visual themes and textures
- brand_patterns: suggested graphic patterns or motifs
- photography_style: guidelines for brand photos
- icon_style: line/filled/outlined with examples

Think step by step to ensure the brand identity aligns perfectly with the core values and industry conventions."""

        base_prompt = "You are a Brand Identity Designer."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def create_ad_visuals(self, campaign_objective: str,
                                  platform: str,
                                  audience: Dict[str, Any],
                                  brand_guidelines: Optional[Dict[str, Any]] = None,
                                  context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate ad creative concepts with image prompts."""
        prompt = f"""Create ad visual concepts for:
Objective: {campaign_objective}
Platform: {platform}
Audience: {json.dumps(audience)}
Brand guidelines: {json.dumps(brand_guidelines or {{}})}

Return JSON with:
- concepts: list of 3 ads, each with:
  - concept_name, visual_description, headline, cta
  - image_prompt: ready-to-use AI image generation prompt
  - dimensions: recommended size for platform
  - color_treatment: colors and overlays
- platform_specs: required dimensions and format for {platform}
- a_b_test_recommendation: which elements to test

Think step by step about the hook and visual hierarchy for the target platform."""

        base_prompt = "You are an Art Director focusing on high-converting social media creatives."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def visual_strategy(self, business: Dict[str, Any],
                                platforms: Optional[List[str]] = None,
                                content_pillars: Optional[List[str]] = None,
                                context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a visual content strategy and calendar."""
        prompt = f"""Create a visual content strategy for:
Business: {json.dumps(business)}
Platforms: {json.dumps(platforms or ["instagram", "linkedin", "website"])}
Content pillars: {json.dumps(content_pillars or [])}

Return JSON with:
- visual_identity_summary: brand visual direction
- platform_guidelines: per-platform visual specs and best practices
- content_calendar_7d: list with day, platform, visual_type, concept, image_prompt
- templates_needed: list of reusable visual templates to create
- tools_recommended: list of design/AI tools for the workflow

Think step by step about creating a cohesive visual narrative across platforms."""

        base_prompt = "You are a Visual Content Strategist."
        sys_prompt = self.build_system_prompt(base_prompt, context)

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def batch_generate(self, concepts: List[str],
                              style: str = "photorealistic",
                              platform: str = "general",
                              context: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Generate image prompts for multiple concepts at once."""
        results = []
        for concept in concepts:
            result = await self.generate_image_prompt(concept, style, platform, dimensions=None, context=context)
            results.append({"concept": concept, "prompts": result})
        return results

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete creative request",
            "dall_e_prompt": "Fallback prompt",
            "midjourney_prompt": "Fallback prompt",
            "stable_diffusion_prompt": "Fallback prompt",
            "color_palette": {},
            "concepts": [],
            "visual_identity_summary": "Fallback summary",
            "platform_guidelines": {}
        }

    def _parse_json(self, response: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(response, fallback=self._get_fallback_response())

# Register Agent
AgentRegistry.register(AgentCapability(
    name="CreativeAgent",
    category="Marketing",
    capabilities=["generate_image_prompt", "design_brand_identity", "create_ad_visuals", "visual_strategy", "batch_generate"],
    description="Expert in visual content — AI image prompting, brand design, and ad creatives.",
    agent_class=CreativeAgent
))
