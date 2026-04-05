"""
JudgeAgent — Quality Gatekeeper

Generates task-specific rubrics, evaluates content through the EvaluatorLeague,
and coordinates revision loops. Every piece of content passes through the Judge
before it reaches the user.
"""
import json
import logging
from typing import Any, Dict, Optional, List

from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.agents.evaluator import evaluator_league
from services.core.llm import default_llm, ModelTier

logger = logging.getLogger(__name__)


class JudgeAgent(BaseAgent):
    """
    The quality gatekeeper for ALL content.

    Workflow:
    1. generate_rubric() — create scoring criteria for this content type
    2. evaluate_content() — score content against the rubric
    3. If fail: request_revision() — generate targeted revision instructions
    4. Repeat up to max_retries
    """

    MAX_RETRIES = 3

    def __init__(self):
        super().__init__(AgentConfig(
            name="JudgeAgent",
            description="Quality assurance — rubric generation, content evaluation, revision coordination",
        ))

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        action = input_data.get("action", "evaluate_content") if isinstance(input_data, dict) else "evaluate_content"

        if action == "generate_rubric":
            return await self.generate_rubric(
                content_type=input_data.get("content_type", "general"),
                platform=input_data.get("platform", ""),
                business_identity=input_data.get("business_identity", {}),
            )
        elif action == "evaluate_content":
            rubric = input_data.get("rubric")
            if not rubric:
                rubric = await self.generate_rubric(
                    content_type=input_data.get("content_type", "general"),
                    platform=input_data.get("platform", ""),
                    business_identity=input_data.get("business_identity", {}),
                )
            return await self.evaluate_content(
                content=input_data.get("content", {}),
                rubric=rubric,
                business_identity=input_data.get("business_identity", {}),
            )
        elif action == "request_revision":
            return await self.request_revision(
                content=input_data.get("content", {}),
                evaluation=input_data.get("evaluation", {}),
            )
        else:
            return {"error": f"Unknown action: {action}"}

    async def generate_rubric(
        self,
        content_type: str,
        platform: str,
        business_identity: dict,
    ) -> dict:
        """
        Generate a scoring rubric specific to content type and platform.

        Returns criteria with weights, minimum pass score, and max retries.
        """
        prompt = f"""You are a quality assurance expert. Generate a scoring rubric for evaluating the following content.

Content Type: {content_type}
Platform: {platform}
Business Context: {json.dumps(business_identity, default=str)[:1000]}

Generate a rubric with 4-6 criteria. Each criterion should have:
- name: lowercase_with_underscores
- weight: decimal (all weights must sum to 1.0)
- description: what to evaluate

Set minimum_pass_score between 0.70 and 0.85 based on how critical quality is for this content type.

Return ONLY valid JSON:
{{
    "criteria": [
        {{"name": "brand_voice", "weight": 0.25, "description": "Matches brand tone and vocabulary"}},
        ...
    ],
    "minimum_pass_score": 0.80,
    "max_retries": 3
}}"""

        try:
            response = await default_llm.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                tier=ModelTier.FLASH,
            )
            rubric = json.loads(response.strip().strip("`").replace("json\n", "").strip())

            # Validate structure
            if "criteria" not in rubric:
                raise ValueError("Missing criteria")
            rubric.setdefault("minimum_pass_score", 0.80)
            rubric.setdefault("max_retries", self.MAX_RETRIES)
            return rubric

        except Exception as e:
            logger.error("Rubric generation failed: %s. Using default rubric.", e)
            return self._default_rubric(content_type, platform)

    async def evaluate_content(
        self,
        content: dict,
        rubric: dict,
        business_identity: dict,
    ) -> dict:
        """
        Evaluate content against the rubric.

        Returns scores per criterion, overall score, pass/fail, and revision instructions if failed.
        """
        criteria_text = "\n".join(
            f"- {c['name']} (weight {c['weight']}): {c['description']}"
            for c in rubric.get("criteria", [])
        )

        prompt = f"""You are a content quality evaluator. Score this content against the rubric.

CONTENT:
{json.dumps(content, default=str)[:2000]}

BUSINESS CONTEXT:
{json.dumps(business_identity, default=str)[:800]}

RUBRIC CRITERIA:
{criteria_text}

For each criterion, provide a score (0.0 to 1.0) and brief feedback.

Return ONLY valid JSON:
{{
    "scores": [
        {{"name": "criterion_name", "score": 0.85, "feedback": "Brief assessment"}},
        ...
    ],
    "overall_feedback": "Summary of evaluation"
}}"""

        try:
            response = await default_llm.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                tier=ModelTier.FLASH,
            )
            evaluation = json.loads(response.strip().strip("`").replace("json\n", "").strip())
        except Exception as e:
            logger.error("Content evaluation failed: %s", e)
            evaluation = {"scores": [], "overall_feedback": f"Evaluation error: {e}"}

        # Calculate weighted score
        criteria_map = {c["name"]: c["weight"] for c in rubric.get("criteria", [])}
        total_score = 0.0
        total_weight = 0.0
        scored_criteria = []

        for s in evaluation.get("scores", []):
            weight = criteria_map.get(s["name"], 0.0)
            total_score += s["score"] * weight
            total_weight += weight
            scored_criteria.append({**s, "weight": weight})

        overall_score = total_score / total_weight if total_weight > 0 else 0.5
        min_pass = rubric.get("minimum_pass_score", 0.80)
        passed = overall_score >= min_pass

        result = {
            "passed": passed,
            "overall_score": round(overall_score, 3),
            "minimum_pass_score": min_pass,
            "criteria_scores": scored_criteria,
            "overall_feedback": evaluation.get("overall_feedback", ""),
        }

        if not passed:
            revision = await self.request_revision(content, result)
            result["revision_instructions"] = revision

        return result

    async def request_revision(
        self,
        content: dict,
        evaluation: dict,
    ) -> dict:
        """Generate specific revision instructions for the creating agent."""
        failing_criteria = [
            c for c in evaluation.get("criteria_scores", [])
            if c.get("score", 1.0) < 0.7
        ]

        prompt = f"""Based on this evaluation, generate specific, actionable revision instructions.

CONTENT:
{json.dumps(content, default=str)[:1500]}

FAILING CRITERIA:
{json.dumps(failing_criteria, default=str)}

OVERALL FEEDBACK:
{evaluation.get('overall_feedback', '')}

Return ONLY valid JSON:
{{
    "revision_instructions": [
        {{"criterion": "name", "action": "Specific instruction on what to change"}},
        ...
    ],
    "priority": "high/medium/low"
}}"""

        try:
            response = await default_llm.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                tier=ModelTier.FLASH,
            )
            return json.loads(response.strip().strip("`").replace("json\n", "").strip())
        except Exception as e:
            logger.error("Revision request generation failed: %s", e)
            return {
                "revision_instructions": [{"criterion": "general", "action": "Please improve overall quality"}],
                "priority": "medium",
            }

    def _default_rubric(self, content_type: str, platform: str) -> dict:
        """Fallback rubric when LLM generation fails."""
        return {
            "criteria": [
                {"name": "brand_voice", "weight": 0.25, "description": "Matches brand tone and vocabulary"},
                {"name": "icp_targeting", "weight": 0.25, "description": "Addresses target audience pain points"},
                {"name": "content_quality", "weight": 0.25, "description": "Well-structured, clear, engaging"},
                {"name": "platform_optimization", "weight": 0.25, "description": f"Optimized for {platform or content_type}"},
            ],
            "minimum_pass_score": 0.80,
            "max_retries": self.MAX_RETRIES,
        }


# Register
AgentRegistry.register(
    AgentCapability(
        name="JudgeAgent",
        category="quality",
        capabilities=["generate_rubric", "evaluate_content", "request_revision", "audit_agent"],
        description="Quality assurance — rubric generation, content evaluation, revision coordination",
    ),
    agent_class=JudgeAgent,
)
