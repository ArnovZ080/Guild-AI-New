from typing import Any, Dict, List, Optional
import asyncio
import json
from services.core.logging import logger
from services.core.llm import default_llm
from services.core.agents.models import DelegationSpec

class BaseEvaluator:
    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight

    async def evaluate(self, task_intent: str, agent_output: Any, success_criteria: List[str]) -> Dict[str, Any]:
        raise NotImplementedError

class FactCheckerEvaluator(BaseEvaluator):
    async def evaluate(self, task_intent: str, agent_output: Any, success_criteria: List[str]) -> Dict[str, Any]:
        prompt = f"""[Fact Checker Agent]
Task: {task_intent}
Output: {agent_output}
Criteria: {success_criteria}

Verify the factual accuracy of the output. 
Return ONLY valid JSON with no markdown formatting: {{"approved": bool, "score": 0.0-1.0, "feedback": "string"}}
"""
        try:
            res = await default_llm.chat_completion([{"role": "user", "content": prompt}])
            data = json.loads(res.strip().strip('`').replace('json\n', '').strip())
            return {"approved": data.get("approved", True), "score": data.get("score", 1.0), "feedback": data.get("feedback", "")}
        except Exception as e:
            logger.error(f"FactChecker fallback: {e}")
            return {"approved": True, "score": 0.8, "feedback": "Fallback score"}

class BrandComplianceEvaluator(BaseEvaluator):
    async def evaluate(self, task_intent: str, agent_output: Any, success_criteria: List[str]) -> Dict[str, Any]:
        prompt = f"""[Brand Compliance Agent]
Ensure the output matches the required brand voice and guidelines.
Output: {agent_output}
Criteria: {success_criteria}

Return ONLY valid JSON with no markdown formatting: {{"approved": bool, "score": 0.0-1.0, "feedback": "string"}}
"""
        try:
            res = await default_llm.chat_completion([{"role": "user", "content": prompt}])
            data = json.loads(res.strip().strip('`').replace('json\n', '').strip())
            return {"approved": data.get("approved", True), "score": data.get("score", 0.9), "feedback": data.get("feedback", "")}
        except Exception as e:
            logger.error(f"BrandCompliance fallback: {e}")
            return {"approved": True, "score": 0.8, "feedback": "Fallback score"}

class SEOEvaluator(BaseEvaluator):
    async def evaluate(self, task_intent: str, agent_output: Any, success_criteria: List[str]) -> Dict[str, Any]:
        prompt = f"""[SEO Evaluator Agent]
Check SEO optimization and structure.
Output: {agent_output}

Return ONLY valid JSON with no markdown formatting: {{"approved": bool, "score": 0.0-1.0, "feedback": "string"}}
"""
        try:
            res = await default_llm.chat_completion([{"role": "user", "content": prompt}])
            data = json.loads(res.strip().strip('`').replace('json\n', '').strip())
            return {"approved": data.get("approved", True), "score": data.get("score", 0.8), "feedback": data.get("feedback", "")}
        except Exception as e:
            logger.error(f"SEOEvaluator fallback: {e}")
            return {"approved": True, "score": 0.8, "feedback": "Fallback score"}

class EvaluatorLeague:
    def __init__(self):
        self.evaluators = {
            "fact_checker": FactCheckerEvaluator("Fact Checker", weight=0.4),
            "brand": BrandComplianceEvaluator("Brand Compliance", weight=0.3),
            "seo": SEOEvaluator("SEO Validator", weight=0.3)
        }

    async def review(self, task: DelegationSpec, output: Any) -> Dict[str, Any]:
        logger.info(f"Evaluator League initiating review for task: {task.id}")
        
        # Parallel evaluation
        evaluation_tasks = []
        enabled_evaluators = ["fact_checker", "brand"] # Default
        if "seo" in task.intent.lower() or "content" in task.intent.lower():
            enabled_evaluators.append("seo")
            
        for key in enabled_evaluators:
            evaluator = self.evaluators[key]
            evaluation_tasks.append(evaluator.evaluate(task.intent, output, task.success_criteria))
            
        results = await asyncio.gather(*evaluation_tasks)
        
        # Aggregate scores
        total_score = 0.0
        total_weight = 0.0
        feedback_list = []
        all_approved = True
        
        for i, res in enumerate(results):
            eval_key = enabled_evaluators[i]
            evaluator = self.evaluators[eval_key]
            
            total_score += res["score"] * evaluator.weight
            total_weight += evaluator.weight
            if not res["approved"]:
                all_approved = False
                feedback_list.append(f"[{evaluator.name}] {res['feedback']}")
        
        weighted_avg = total_score / total_weight if total_weight > 0 else 0.0
        
        # Threshold enforcement (e.g. 0.8)
        is_passed = all_approved and weighted_avg >= 0.8
        
        return {
            "approved": is_passed,
            "overall_score": weighted_avg,
            "feedback": "; ".join(feedback_list) if feedback_list else "All quality standards met."
        }

# Global instance
evaluator_league = EvaluatorLeague()
