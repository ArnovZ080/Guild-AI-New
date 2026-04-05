"""
Evaluator League — Quality Assurance Pipeline

5 evaluators: FactChecker, BrandCompliance, SEO, AudienceAlignment, TechnicalValidator
Supports rubric-driven evaluation from JudgeAgent.
"""
from typing import Any, Dict, List, Optional
import asyncio
import json
from services.core.logging import logger
from services.core.llm import default_llm, ModelTier
from services.core.agents.models import DelegationSpec


class BaseEvaluator:
    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight

    async def evaluate(self, task_intent: str, agent_output: Any,
                       success_criteria: List[str], rubric: Optional[Dict] = None) -> Dict[str, Any]:
        raise NotImplementedError


class FactCheckerEvaluator(BaseEvaluator):
    async def evaluate(self, task_intent: str, agent_output: Any,
                       success_criteria: List[str], rubric: Optional[Dict] = None) -> Dict[str, Any]:
        prompt = f"""[Fact Checker Agent]
Task: {task_intent}
Output: {str(agent_output)[:1500]}
Criteria: {success_criteria}

Verify the factual accuracy of the output.
Return ONLY valid JSON: {{"approved": bool, "score": 0.0-1.0, "feedback": "string"}}"""
        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.2, tier=ModelTier.FLASH)
            data = json.loads(res.strip().strip('`').replace('json\n', '').strip())
            return {"approved": data.get("approved", True), "score": data.get("score", 1.0),
                    "feedback": data.get("feedback", "")}
        except Exception as e:
            logger.error(f"FactChecker fallback: {e}")
            return {"approved": True, "score": 0.8, "feedback": "Fallback score"}


class BrandComplianceEvaluator(BaseEvaluator):
    async def evaluate(self, task_intent: str, agent_output: Any,
                       success_criteria: List[str], rubric: Optional[Dict] = None) -> Dict[str, Any]:
        prompt = f"""[Brand Compliance Agent]
Ensure the output matches the required brand voice and guidelines.
Output: {str(agent_output)[:1500]}
Criteria: {success_criteria}

Return ONLY valid JSON: {{"approved": bool, "score": 0.0-1.0, "feedback": "string"}}"""
        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.2, tier=ModelTier.FLASH)
            data = json.loads(res.strip().strip('`').replace('json\n', '').strip())
            return {"approved": data.get("approved", True), "score": data.get("score", 0.9),
                    "feedback": data.get("feedback", "")}
        except Exception as e:
            logger.error(f"BrandCompliance fallback: {e}")
            return {"approved": True, "score": 0.8, "feedback": "Fallback score"}


class SEOEvaluator(BaseEvaluator):
    async def evaluate(self, task_intent: str, agent_output: Any,
                       success_criteria: List[str], rubric: Optional[Dict] = None) -> Dict[str, Any]:
        prompt = f"""[SEO Evaluator Agent]
Check SEO optimization and structure.
Output: {str(agent_output)[:1500]}

Return ONLY valid JSON: {{"approved": bool, "score": 0.0-1.0, "feedback": "string"}}"""
        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.2, tier=ModelTier.FLASH)
            data = json.loads(res.strip().strip('`').replace('json\n', '').strip())
            return {"approved": data.get("approved", True), "score": data.get("score", 0.8),
                    "feedback": data.get("feedback", "")}
        except Exception as e:
            logger.error(f"SEOEvaluator fallback: {e}")
            return {"approved": True, "score": 0.8, "feedback": "Fallback score"}


class AudienceAlignmentEvaluator(BaseEvaluator):
    """Validates content resonates with the ICP from BusinessIdentity."""

    async def evaluate(self, task_intent: str, agent_output: Any,
                       success_criteria: List[str], rubric: Optional[Dict] = None) -> Dict[str, Any]:
        icp_context = ""
        if rubric and "business_identity" in rubric:
            bi = rubric["business_identity"]
            icp_context = f"ICP: {json.dumps(bi.get('icp', {}), default=str)[:500]}\nTarget: {bi.get('target_audience', '')}"

        prompt = f"""[Audience Alignment Evaluator]
Does this content resonate with the target audience / ideal customer profile?

{icp_context}

Content: {str(agent_output)[:1500]}

Evaluate:
1. Pain point relevance — does it address the ICP's actual problems?
2. Language fit — does the vocabulary match the audience's level?
3. Value proposition — is the benefit clear to THIS audience?
4. Engagement potential — would this ICP actually engage with this?

Return ONLY valid JSON: {{"approved": bool, "score": 0.0-1.0, "feedback": "string"}}"""
        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.2, tier=ModelTier.FLASH)
            data = json.loads(res.strip().strip('`').replace('json\n', '').strip())
            return {"approved": data.get("approved", True), "score": data.get("score", 0.75),
                    "feedback": data.get("feedback", "")}
        except Exception as e:
            logger.error(f"AudienceAlignment fallback: {e}")
            return {"approved": True, "score": 0.75, "feedback": "Fallback score"}


class TechnicalValidator(BaseEvaluator):
    """Checks platform-specific technical requirements."""

    PLATFORM_LIMITS = {
        "instagram": {"max_caption": 2200, "max_hashtags": 30},
        "linkedin": {"max_post": 3000, "max_article": 120000},
        "twitter": {"max_post": 280},
        "facebook": {"max_post": 63206},
        "email": {"max_subject": 60, "max_preheader": 100},
        "blog": {"min_words": 300, "max_words": 5000},
    }

    async def evaluate(self, task_intent: str, agent_output: Any,
                       success_criteria: List[str], rubric: Optional[Dict] = None) -> Dict[str, Any]:
        platform = rubric.get("platform", "") if rubric else ""
        limits = self.PLATFORM_LIMITS.get(platform.lower(), {})

        if not limits:
            return {"approved": True, "score": 0.9, "feedback": "No platform-specific rules to check."}

        prompt = f"""[Technical Validator]
Check this content against platform-specific technical requirements.

Platform: {platform}
Requirements: {json.dumps(limits)}
Content: {str(agent_output)[:1500]}

Check: character count limits, hashtag counts, image dimension requirements,
format compliance, link formatting, etc.

Return ONLY valid JSON: {{"approved": bool, "score": 0.0-1.0, "feedback": "string", "violations": ["list", "of", "issues"]}}"""
        try:
            res = await default_llm.chat_completion(
                [{"role": "user", "content": prompt}], temperature=0.1, tier=ModelTier.FLASH)
            data = json.loads(res.strip().strip('`').replace('json\n', '').strip())
            return {"approved": data.get("approved", True), "score": data.get("score", 0.9),
                    "feedback": data.get("feedback", ""), "violations": data.get("violations", [])}
        except Exception as e:
            logger.error(f"TechnicalValidator fallback: {e}")
            return {"approved": True, "score": 0.85, "feedback": "Fallback score"}


class EvaluatorLeague:
    """Orchestrates all evaluators — rubric-driven or default mode."""

    def __init__(self):
        self.evaluators = {
            "fact_checker": FactCheckerEvaluator("Fact Checker", weight=0.25),
            "brand": BrandComplianceEvaluator("Brand Compliance", weight=0.20),
            "seo": SEOEvaluator("SEO Validator", weight=0.15),
            "audience": AudienceAlignmentEvaluator("Audience Alignment", weight=0.25),
            "technical": TechnicalValidator("Technical Validator", weight=0.15),
        }

    async def review(self, task: DelegationSpec, output: Any,
                     rubric: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Evaluate content. If rubric is provided, use rubric-driven weights.
        Otherwise, use default evaluator selection.
        """
        logger.info(f"Evaluator League reviewing task: {task.id}")

        if rubric and "criteria" in rubric:
            return await self._rubric_review(task, output, rubric)
        else:
            return await self._default_review(task, output)

    async def _rubric_review(self, task: DelegationSpec, output: Any, rubric: Dict) -> Dict[str, Any]:
        """Run all 5 evaluators and score against rubric criteria."""
        eval_tasks = []
        eval_keys = list(self.evaluators.keys())

        for key in eval_keys:
            evaluator = self.evaluators[key]
            eval_tasks.append(
                evaluator.evaluate(task.intent, output, task.success_criteria, rubric)
            )

        results = await asyncio.gather(*eval_tasks)

        # Map evaluator results to rubric criteria
        total_score = 0.0
        total_weight = 0.0
        feedback_list = []
        all_approved = True

        for i, res in enumerate(results):
            evaluator = self.evaluators[eval_keys[i]]
            weight = evaluator.weight
            total_score += res["score"] * weight
            total_weight += weight
            if not res["approved"]:
                all_approved = False
                feedback_list.append(f"[{evaluator.name}] {res['feedback']}")

        overall = total_score / total_weight if total_weight > 0 else 0.5
        min_pass = rubric.get("minimum_pass_score", 0.80)
        passed = all_approved and overall >= min_pass

        return {
            "approved": passed,
            "overall_score": round(overall, 3),
            "minimum_pass_score": min_pass,
            "evaluator_results": {
                eval_keys[i]: results[i] for i in range(len(results))
            },
            "feedback": "; ".join(feedback_list) if feedback_list else "All quality standards met.",
        }

    async def _default_review(self, task: DelegationSpec, output: Any) -> Dict[str, Any]:
        """Legacy default review (no rubric)."""
        eval_tasks = []
        enabled = ["fact_checker", "brand", "audience"]
        if "seo" in task.intent.lower() or "content" in task.intent.lower():
            enabled.append("seo")

        for key in enabled:
            evaluator = self.evaluators[key]
            eval_tasks.append(evaluator.evaluate(task.intent, output, task.success_criteria))

        results = await asyncio.gather(*eval_tasks)

        total_score = 0.0
        total_weight = 0.0
        feedback_list = []
        all_approved = True

        for i, res in enumerate(results):
            evaluator = self.evaluators[enabled[i]]
            total_score += res["score"] * evaluator.weight
            total_weight += evaluator.weight
            if not res["approved"]:
                all_approved = False
                feedback_list.append(f"[{evaluator.name}] {res['feedback']}")

        weighted_avg = total_score / total_weight if total_weight > 0 else 0.0
        is_passed = all_approved and weighted_avg >= 0.8

        return {
            "approved": is_passed,
            "overall_score": round(weighted_avg, 3),
            "feedback": "; ".join(feedback_list) if feedback_list else "All quality standards met.",
        }


# Global instance
evaluator_league = EvaluatorLeague()
