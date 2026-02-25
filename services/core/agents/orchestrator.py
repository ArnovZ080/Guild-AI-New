from typing import Any, Dict, List, Optional, Set
import json
import asyncio
import uuid
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from services.core.agents.base import BaseAgent, AgentConfig
from services.core.agents.registry import AgentRegistry, AgentCapability
from services.core.agents.models import DelegationSpec, DelegationPlan, AuthorityLevel, TaskStatus, RiskLevel, Project
from services.core.llm import default_llm
from services.core.agents.evaluator import evaluator_league
from services.core.agents.identity import identity_manager
from services.core.agents.projects import project_manager
from services.core.agents.authorization import auth_queue
from services.core.learning.adaptive_service import AdaptiveLearningService
from services.core.learning.outcome_tracker import OutcomeTracker
from services.core.customers.predictive_engine import PredictiveEngine
from services.core.workflows.executor import WorkflowExecutor
from services.core.workflows.templates import register_all_templates

# Ensure all agents are registered
import services.core.adk as adk
from services.core.agents import content, research, triggers, evaluator
from services.core.agents.models import AgentEvent, AgentEventType, DelegationSpec, DelegationPlan, AuthorityLevel, TaskStatus, RiskLevel, Project, ProjectMilestone
from services.core.utils.event_bus import event_bus

class OrchestratorAgent(BaseAgent):
    """
    The Orchestrator Agent analyzes a complex user request, breaks it down into
    tasks, assigns them to available agents, and orchestrates their execution.
    """
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        # Register autonomous workflow templates natively
        register_all_templates()
    
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        goal = input_data.get("goal")
        if not goal:
            raise ValueError("OrchestratorAgent requires a 'goal'")

        # 1. Enforce Persistent Business Context
        business_context = identity_manager.get_context_prompt()

        # 2. Discovery: Get available agents
        agents_desc = AgentRegistry.get_description_map()
        
        # 2.5 Inject Adaptive Learning Context
        adaptive_context = AdaptiveLearningService.get_context_for_orchestrator()

        # 2.6 Inject Proactive Customer Intelligence
        proactive_actions = PredictiveEngine.get_proactive_tasks()
        proactive_context = ""
        if proactive_actions:
            lines = ["## Proactive Actions Needed (Predictive Engine)"]
            for a in proactive_actions[:5]:
                lines.append(f"- [{a.priority.value.upper()}] {a.title} for customer {a.customer_id} (confidence: {a.confidence}, urgency: {a.urgency})")
            proactive_context = "\n".join(lines)

        # 3. Planning: Generate Delegation Plan with context-aware goal
        context_aware_objective = f"""
{business_context}

{adaptive_context}

{proactive_context}

USER OBJECTIVE:
{goal}
"""
        event_bus.emit(AgentEvent(
            agent_id=self.config.name,
            event_type=AgentEventType.THINKING,
            description="Orchestrator is drafting a new delegation plan.",
            how="Using LLM to decompose high-level goal into a dependency-mapped DAG.",
            why="Decomposition ensures complex objectives are addressed by specialized agents in a logical sequence.",
            progress=0.3
        ))
        plan = await self._generate_plan(context_aware_objective, agents_desc)
        
        # Pre-flight Planning Check
        require_preflight = input_data.get("require_preflight", False)
        if require_preflight:
            self.logger.info("Pre-flight plan generated. Awaiting user approval before execution.")
            return {
                "status": "pending_approval",
                "plan": plan.model_dump(),
                "message": "Pre-flight DAG execution graph generated. Awaiting user approval to trigger workforce."
            }

        # 3. Execution: Run the delegated tasks
        results = await self._execute_plan(plan, context or {})
        
        return {
            "status": "completed",
            "plan": plan.model_dump(),
            "results": results
        }

    async def execute_approved_plan(self, plan_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Executes a previously generated and user-approved DelegationPlan."""
        try:
            plan = DelegationPlan(**plan_data)
            self.logger.info("Executing user-approved pre-flight plan.")
            results = await self._execute_plan(plan, context or {})
            
            return {
                "status": "completed",
                "results": results
            }
        except Exception as e:
            self.logger.error(f"Failed to execute approved plan: {e}")
            return {"status": "failed", "error": str(e)}

    async def get_dashboard_snapshot(self) -> Dict[str, Any]:
        """
        Natively wires the core intelligences (Business, Customer) to provide a unified dashboard snapshot without legacy bridges.
        """
        bi_agent = self._instantiate_agent("BusinessIntelligenceAgent")
        ci_agent = self._instantiate_agent("CustomerIntelligenceAgent")
        
        snapshot = {}
        if bi_agent:
            snapshot["business_kpis"] = await bi_agent.process({"command": "get_snapshot"})
        
        if ci_agent:
            snapshot["customer_health"] = await ci_agent.process({"command": "churn_prediction"})
            
        return {
            "timestamp": datetime.now().isoformat(),
            "unified_snapshot": snapshot
        }

    async def create_strategic_roadmap(self, input_data: Any) -> Project:
        goal = input_data.get("goal")
        timeframe = input_data.get("timeframe", 90)
        
        identity = identity_manager.get_identity()
        identity_context = {
            "business_name": identity.business_name,
            "niche": identity.niche,
            "brand_voice": identity.brand_voice
        }
        
        sys_prompt = f"""You are a Silicon Valley Chief Strategy Officer. 
Your goal is to take a high-level business objective and break it into a {timeframe}-day strategic roadmap.

Business Profile: {json.dumps(identity_context)}

The roadmap must consist of 3 monthly milestones. Each milestone should have a clear theme, a focus description, and 3-5 specific success metrics.
Return JSON with a "milestones" key containing a list of objects with:
- title: string (e.g., "Month 1: Infrastructure & Foundation")
- focus: string (detailed description of the phase goal)
- metrics: list of strings (KPIs to track)
"""
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Create a roadmap for: {goal}"}
        ])
        
        try:
            # Clean and parse response
            clean_response = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_response)
            milestones_data = data.get("milestones", [])
            
            milestones = []
            for i, m_info in enumerate(milestones_data):
                period_days = (timeframe // len(milestones_data)) * (i + 1)
                target_date = (datetime.now() + timedelta(days=period_days)).strftime("%Y-%m-%d")
                
                milestones.append(ProjectMilestone(
                    id=f"m{i+1}_{uuid.uuid4().hex[:8]}",
                    title=m_info.get("title", f"Milestone {i+1}"),
                    focus=m_info.get("focus", ""),
                    metrics=m_info.get("metrics", []),
                    target_date=target_date
                ))
            
            project = project_manager.create_project(
                business_id=identity.business_name, 
                goal=goal, 
                timeframe_days=timeframe,
                milestones=milestones
            )
            return project
            
        except Exception as e:
            self.logger.error(f"Failed to generate strategic roadmap: {e}")
            self.logger.debug(f"LLM Response: {response}")
            # Fallback to simple creation
            return project_manager.create_project(identity.business_name, goal, timeframe)

    async def execute_milestone(self, project_id: str, milestone_id: str) -> Dict[str, Any]:
        project = project_manager.get_project(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        milestone = next((m for m in project.milestones if m.id == milestone_id), None)
        if not milestone:
            raise ValueError(f"Milestone {milestone_id} not found in project {project_id}")

        self.logger.info(f"Executing Milestone: {milestone.title}")
        
        # 1. Planning: Generate specific tasks for this milestone's focus
        agents_desc = AgentRegistry.get_description_map()
        sys_prompt = f"""You are a Silicon Valley Operations Lead.
Your goal is to break a high-level strategic milestone into a series of actionable agent tasks.

Project Goal: {project.goal}
Current Milestone: {milestone.title}
Phase Focus: {milestone.focus}
Success Metrics: {milestone.metrics}

Available Agents:
{agents_desc}

Create a detailed JSON delegation plan with an array of tasks. Refer to previous standards for task definitions.
"""
        plan = await self._generate_plan(milestone.focus, agents_desc)
        
        # 2. Execution
        results = await self._execute_plan(plan, {"project_id": project_id, "milestone_id": milestone_id})
        
        # 3. Update status
        milestone.status = TaskStatus.COMPLETED
        milestone.task_ids = [t.id for t in plan.tasks]
        
        return {
            "milestone": milestone.title,
            "results": results
        }

    async def _generate_plan(self, goal: str, agents_desc: str) -> DelegationPlan:
        sys_prompt = """You are an Expert Delegation Architect. 
Your goal is to break down complex user intent into a structured "Smart Contract" delegation plan. 

For each task, you must define:
- id: unique string
- intent: clear goal for the agent
- assigned_agent: best match from available list
- dependencies: previous task IDs
- boundaries: constraints and "do nots"
- authority_level: 'full', 'semi', or 'human'
- success_criteria: verifiable metrics for the Evaluator League
- rationale: why this agent for this specific task
- risk_level: 'low', 'medium', 'high', or 'critical'
- deadline: estimated relative time (e.g. "immediate", "short-term")
- resources: budget/token constraints as JSON map
- retry_limit: 1-5 depending on risk

Optimize for:
1. Speed (parallelize where possible)
2. Cost (use least expensive capable agent)
3. Quality (use high-trust agents for critical tasks)
"""
        user_prompt = f"""
        Objective: {goal}
        
        Available Agents (Reputation context):
        {agents_desc}
        
        Create a detailed JSON delegation plan with an array of tasks under the "tasks" key.
        """
        
        response = await default_llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        try:
            # Basic cleanup
            clean_response = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_response)
            
            # Extract tasks list regardless of wrapping key
            tasks_data = data.get("tasks", data) if isinstance(data, dict) else data
            
            if not isinstance(tasks_data, list):
                 raise ValueError("Invalid delegation plan format: tasks must be a list")
                 
            return DelegationPlan(tasks=[DelegationSpec(**t) for t in tasks_data])
                 
        except Exception as e:
            self.logger.error(f"Failed to parse delegation plan: {e}")
            self.logger.debug(f"Raw Response: {response}")
            # Robust Fallback: Return a simple one-task plan to keep the engine moving
            return DelegationPlan(tasks=[
                DelegationSpec(
                    id=f"fallback_{uuid.uuid4().hex[:4]}",
                    intent=f"Process component: {goal}",
                    assigned_agent="OrchestratorAgent",
                    rationale="LLM parsing failed, using automated fallback.",
                    resources={"budget": 0.0}
                )
            ])

    async def _execute_plan(self, plan: DelegationPlan, initial_context: Dict) -> Dict[str, Any]:
        results = {}
        pending_tasks = {t.id: t for t in plan.tasks}
        completed_tasks: Set[str] = set()
        
        # Track total budget and usage
        total_budget = sum(t.resources.get("budget", 0.0) for t in plan.tasks)
        current_spend = 0.0
        
        self.logger.info(f"Initiating Orchestration with total budget: {total_budget}")
        
        while pending_tasks:
            # Find runnable tasks based on dependency completion
            runnable = []
            for tid, task in pending_tasks.items():
                if all(dep in completed_tasks and results.get(dep) is not None for dep in task.dependencies):
                    runnable.append(task)
            
            if not runnable:
                if pending_tasks:
                    self.logger.error(f"Deadlock or unresolvable dependencies in pipeline. Pending: {list(pending_tasks.keys())}")
                    raise RuntimeError("Deadlock detected in delegation execution.")
                break
            
            # For Phase 2, we execute runnable tasks (could be parallelized further, but keep sequential for now for stability)
            task = runnable[0]
            
            # --- SMART CONTRACT ENFORCEMENT: Budget ---
            task_budget = task.resources.get("budget", 0.0)
            if task_budget > 0 and (current_spend + task_budget > total_budget):
                error_msg = f"Smart Contract Violation: Budget exceeded. Task {task.id} requires {task_budget}, current spend: {current_spend}/{total_budget}."
                self.logger.error(error_msg)
                task.status = TaskStatus.FAILED
                task.process_log.append(f"EXECUTION HALTED: {error_msg}")
                results[task.id] = {"error": "budget_exceeded", "details": error_msg}
                completed_tasks.add(task.id)
                del pending_tasks[task.id]
                continue

            self.logger.info(f"Delegating [Smart Contract {task.id}] -> {task.assigned_agent} | Auth: {task.authority_level}")
            event_bus.emit(AgentEvent(
                agent_id=self.config.name,
                event_type=AgentEventType.HANDOFF,
                description=f"Handoff: delegating '{task.intent}' to {task.assigned_agent}.",
                how=f"Transferring state and success criteria to {task.assigned_agent}.",
                why=f"Delegation targets the most suitable agent category for the specific task intent.",
                data={"task_id": task.id, "target_agent": task.assigned_agent},
                progress=current_spend / total_budget if total_budget > 0 else 0.5
            ))
            task.process_log.append(f"Orchestrator validated Smart Contract for {task.id}. Initializing {task.assigned_agent}.")
            
            # 0. Check for Human Authorization requirement
            if task.authority_level == AuthorityLevel.HUMAN:
                self.logger.info(f"Task {task.id} requires human approval. Creating auth request.")
                auth_req = auth_queue.create_request(
                    task_id=task.id,
                    agent_id=task.assigned_agent,
                    action_type="delegation",
                    description=f"Authorize {task.assigned_agent} to execute: {task.intent}",
                    params={"risk_level": task.risk_level, "success_criteria": task.success_criteria}
                )
                results[task.id] = {"status": TaskStatus.PENDING, "auth_required": True, "auth_id": auth_req.id}
                completed_tasks.add(task.id)
                del pending_tasks[task.id]
                continue

            agent_instance = self._instantiate_agent(task.assigned_agent)
            
            if agent_instance:
                retry_count = 0
                max_retries = task.retry_limit
                
                while retry_count <= max_retries:
                    # Build input with accumulated context
                    agent_input = {
                        "objective": task.intent,
                        "boundaries": task.boundaries,
                        "success_criteria": task.success_criteria,
                        "resources": task.resources,
                        "dependency_results": {dep: results[dep] for dep in task.dependencies},
                        "global_context": initial_context
                    }

                    try:
                        task_result = await agent_instance.run(agent_input)
                        
                        # Verification Step (Evaluator League)
                        review = await evaluator_league.review(task, task_result.data)
                        
                        # Store Transparency & Education Meta
                        task.process_log.extend(task_result.process_log)
                        task.educational_takeaway = task_result.educational_takeaway
                        task.cost_breakdown["tokens"] = task_result.cost
                        current_spend += task_result.cost
                        
                        if review["approved"]:
                            task.result = task_result
                            task.status = TaskStatus.COMPLETED
                            results[task.id] = task_result.data
                            task.process_log.append(f"Successfully verified by Evaluator League: {review['overall_score']}")

                            # Record outcome for Adaptive Learning
                            outcome_score = "excellent" if review.get("overall_score", 0) >= 90 else "good" if review.get("overall_score", 0) >= 70 else "neutral"
                            OutcomeTracker.record_outcome(
                                task_id=task.id,
                                agent_id=task.assigned_agent,
                                action_type=task.intent.split(":")[0] if ":" in task.intent else "general",
                                platform=task.intent.split(":")[1] if ":" in task.intent and len(task.intent.split(":")) > 1 else "internal",
                                params={"intent": task.intent, "boundaries": task.boundaries},
                                score=outcome_score,
                                metrics={"evaluator_score": review.get("overall_score", 0), "cost": task_result.cost},
                                context={"retry_count": retry_count}
                            )
                            break
                        else:
                            retry_count += 1
                            task.process_log.append(f"Verification failed: {review['feedback']}")
                            self.logger.warning(f"Task {task.id} failed verification (Attempt {retry_count}/{max_retries}).")
                            if retry_count > max_retries:
                                task.status = TaskStatus.FAILED
                                results[task.id] = {"error": "Failed verification after retries", "feedback": review["feedback"]}
                    except Exception as e:
                        self.logger.error(f"Delegation to {task.id} failed: {e}")
                        task.status = TaskStatus.FAILED
                        results[task.id] = {"error": str(e)}
                        break
            else:
                 self.logger.error(f"Agent {task.assigned_agent} not found.")
                 task.status = TaskStatus.FAILED
                 results[task.id] = {"error": "Agent not found"}

            completed_tasks.add(task.id)
            del pending_tasks[task.id]
            
        return results

    def _instantiate_agent(self, agent_name: str) -> Optional[BaseAgent]:
        capability = AgentRegistry.get(agent_name)
        if not capability or not capability.agent_class:
            return None
            
        # Standard configuration for the delegated agent instance
        config = AgentConfig(
            name=agent_name, 
            description=capability.description,
            model="gpt-4-turbo-preview"
        )
        
        return capability.agent_class(config)

# Register
AgentRegistry.register(AgentCapability(
    name="OrchestratorAgent",
    category="Orchestration",
    capabilities=["workflow_management", "task_delegation"],
    description="Breaks down complex goals and manages multi-agent workflows."
))
