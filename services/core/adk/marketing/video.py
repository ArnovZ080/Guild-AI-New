"""
Video Agent.
Covers video strategy, scripting, editing plans, and content repurposing —
closing the gap left by the legacy VideoEditorAgent.
"""
import json
import logging
from services.core.utils.json_extractor import extract_json_from_llm_response
from typing import Dict, Any, List, Optional
from services.core.llm import default_llm
from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_DEPRECATED = """You are a Video Production Strategist and Editor for a small business.
You combine expertise in video strategy, scriptwriting, editing workflows, and content repurposing.

Your capabilities:
1. SCRIPTING: Write video scripts for YouTube, TikTok, Reels, ads, and webinars
2. EDITING PLAN: Create detailed editing briefs with shot lists, transitions, and timing
3. STRATEGY: Plan video content calendars, channel growth, and SEO optimization
4. REPURPOSE: Transform long-form video into short clips with optimized hooks
5. THUMBNAILS: Design thumbnail concepts and title strategies for click-through

Be specific with timings, shot types, transitions, and platform best practices. Always respond as JSON."""


class VideoAgent(BaseAgent):
    """
    Expert in video production — scripting, editing plans, strategy, and repurposing.

    Replaces legacy:
    - VideoEditorAgent
    """

    agent_name = "VideoAgent"
    agent_type = "Marketing"
    capabilities = [
        "write_script", "create_editing_plan", "video_strategy",
        "repurpose_video", "design_thumbnail"
    ]

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command")
        kwargs = input_data.get("kwargs", {})
        
        # Inject context if available
        if context and "context" not in kwargs:
            kwargs["context"] = context

        if command == "write_script":
            return await self.write_script(**kwargs)
        elif command == "create_editing_plan":
            return await self.create_editing_plan(**kwargs)
        elif command == "video_strategy":
            return await self.video_strategy(**kwargs)
        elif command == "repurpose_video":
            return await self.repurpose_video(**kwargs)
        elif command == "design_thumbnail":
            return await self.design_thumbnail(**kwargs)
        else:
            raise ValueError(f"Unknown command for VideoAgent: {command}")

    async def write_script(self, topic: str,
                            format: str = "youtube",
                            duration_minutes: int = 10,
                            audience: Optional[Dict[str, Any]] = None,
                            tone: str = "engaging",
                            context: Optional[Dict] = None) -> Dict[str, Any]:
        """Write a complete video script with hooks, segments, and CTAs."""
        base_prompt = "You are a Video Production Strategist and Editor for a small business combining expertise in video strategy, scriptwriting, editing workflows, and content repurposing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Write a video script:
Topic: {topic}
Format: {format}
Target duration: {duration_minutes} minutes
Audience: {json.dumps(audience or {{}})}
Tone: {tone}

Return JSON with:
- title: compelling title optimized for {format}
- hook: first 5-second attention grabber
- intro: 15-30 second intro establishing value
- segments: list with segment_name, duration_seconds, script_text, visual_notes, b_roll_suggestions
- cta: call to action with placement timing
- outro: closing segment
- total_word_count: estimated word count
- seo_tags: list of relevant tags
- description: platform-optimized description

Think step by step segmenting the script for maximum engagement."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def create_editing_plan(self, script: Dict[str, Any],
                                    style: str = "professional",
                                    tools: Optional[List[str]] = None,
                                    context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a detailed editing brief from a script or raw footage description."""
        base_prompt = "You are a Video Production Strategist and Editor for a small business combining expertise in video strategy, scriptwriting, editing workflows, and content repurposing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Create a video editing plan:
Script/Content: {json.dumps(script)}
Visual style: {style}
Editing tools: {json.dumps(tools or ["premiere", "davinci"])}

Return JSON with:
- timeline: list of segments with timecode, content, transition_in, transition_out
- color_grading: mood, LUT suggestions, color palette
- motion_graphics: list of lower thirds, titles, and graphics needed
- audio_plan: music_mood, sfx_list, voiceover_notes
- b_roll_shots: list with description, duration, source_suggestion
- export_specs: resolution, fps, codec, platform_specific_exports
- estimated_editing_hours: float

Think step by step visualizing the final edit structure."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def video_strategy(self, business: Dict[str, Any],
                               platforms: Optional[List[str]] = None,
                               goals: Optional[Dict[str, Any]] = None,
                               context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a comprehensive video content strategy."""
        base_prompt = "You are a Video Production Strategist and Editor for a small business combining expertise in video strategy, scriptwriting, editing workflows, and content repurposing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Create a video content strategy:
Business: {json.dumps(business)}
Platforms: {json.dumps(platforms or ["youtube", "tiktok", "instagram"])}
Goals: {json.dumps(goals or {{}})}

Return JSON with:
- content_pillars: list with pillar_name, description, video_formats
- posting_schedule: per-platform frequency and best times
- content_calendar_30d: list with week, platform, video_type, topic, format
- seo_strategy: keyword targeting, title patterns, description templates
- growth_tactics: list of platform-specific growth hacks
- equipment_recommendations: camera, lighting, audio, software
- kpis: metrics to track per platform
- estimated_monthly_production_hours: float

Think step by step about channel audience differentiation."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def repurpose_video(self, source_video: Dict[str, Any],
                                target_platforms: Optional[List[str]] = None,
                                context: Optional[Dict] = None) -> Dict[str, Any]:
        """Transform a long-form video into platform-optimized short clips."""
        platforms = target_platforms or ["tiktok", "instagram_reels", "youtube_shorts", "linkedin"]
        
        base_prompt = "You are a Video Production Strategist and Editor for a small business combining expertise in video strategy, scriptwriting, editing workflows, and content repurposing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Repurpose this video into short-form content:
Source video: {json.dumps(source_video)}
Target platforms: {json.dumps(platforms)}

Return JSON with:
- clips: list with clip_name, start_time, end_time, hook_text,
  platform, aspect_ratio, caption, hashtags, edit_notes
- platform_adaptations: per-platform adjustments (captions, speed, music)
- content_atoms: smallest reusable content pieces (quotes, stats, tips)
- distribution_schedule: posting order and timing across platforms
- estimated_clips_count: int

Think step by step selecting the most engaging clips."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    async def design_thumbnail(self, video_title: str,
                                 video_topic: str,
                                 platform: str = "youtube",
                                 context: Optional[Dict] = None) -> Dict[str, Any]:
        """Design thumbnail concepts with AI image prompts."""
        base_prompt = "You are a Video Production Strategist and Editor for a small business combining expertise in video strategy, scriptwriting, editing workflows, and content repurposing."
        sys_prompt = self.build_system_prompt(base_prompt, context)
        
        prompt = f"""Design a click-worthy thumbnail for:
Title: {video_title}
Topic: {video_topic}
Platform: {platform}

Return JSON with:
- concepts: list of 3 thumbnails, each with:
  - concept_name, visual_description, text_overlay
  - image_prompt: AI generation prompt for the background/scene
  - color_scheme: dominant colors
  - composition: layout description (rule of thirds, etc.)
- title_alternatives: 3 alternative video titles for A/B testing
- best_practices: platform-specific thumbnail tips
- dimensions: recommended size

Think step by step applying color psychology and curiosity gaps."""

        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ])
        return self._parse_json(response)

    def _get_fallback_response(self) -> Dict[str, Any]:
        return {
            "error": "Failed to complete video request",
            "title": "Video Draft",
            "segments": [],
            "timeline": [],
            "content_pillars": [],
            "clips": [],
            "concepts": []
        }

    def _parse_json(self, response: str) -> Dict[str, Any]:
        return extract_json_from_llm_response(response, fallback=self._get_fallback_response())

# Register Agent
AgentRegistry.register(AgentCapability(
    name="VideoAgent",
    category="Marketing",
    capabilities=["write_script", "create_editing_plan", "video_strategy", "repurpose_video", "design_thumbnail"],
    description="Expert in video production — scripting, editing plans, strategy, and repurposing.",
    agent_class=VideoAgent
))
