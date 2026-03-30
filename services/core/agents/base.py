from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from pydantic import BaseModel
from services.core.logging import logger
from services.core.agents.models import TaskResult, TaskStatus, AgentEvent, AgentEventType
from services.core.utils.event_bus import event_bus

class AgentConfig(BaseModel):
    name: str
    description: str
    model: str = "gpt-4-turbo-preview"
    tools: List[str] = []
    metadata: Dict[str, Any] = {}

class BaseAgent(ABC):
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logger.getChild(f"agent.{config.name}")

    @abstractmethod
    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        """
        Core logic for the agent. Must be implemented by subclasses.
        """
        pass

    @classmethod
    def build_system_prompt(cls, base_prompt: str, context: Optional[Dict] = None) -> str:
        """Appends business context and constraints to the base system prompt."""
        from services.core.utils.knowledge_injector import KnowledgeInjector
        
        business_context = KnowledgeInjector.get_business_context_prompt(context)
        
        quality_constraints = """
## Quality & Constraints
1. **Chain of Thought**: Before generating your final JSON output, internally think step-by-step about how to solve the user's request, considering the provided context.
2. **Alignment**: Ensure your response strictly aligns with the brand voice and business context.
3. **Actionability**: Provide specific, actionable advice or content, not generic filler. If you lack context, explicitly state what is missing.
4. **Output Format**: **ALWAYS** return a properly formatted JSON object as your final output.
"""
        return f"{base_prompt}\n\n{business_context}\n{quality_constraints}"

    @classmethod
    def _get_fallback_response(cls) -> Dict[str, Any]:
        """Override in subclasses to provide a valid minimal schema response."""
        return {"error": "Failed to generate proper response", "status": "failed"}

    async def run(self, input_data: Any, context: Optional[Dict] = None) -> TaskResult:
        """
        Wrapper around process to handle logging, errors, and common middleware.
        Ensures output is a structured TaskResult for Theater/Education.
        """
        self.logger.info(f"Starting execution for agent {self.config.name}")
        
        # Initial Theater Entry
        db = context.get("db") if context else None
        await event_bus.emit(AgentEvent(
            agent_id=self.config.name,
            event_type=AgentEventType.STARTED,
            description=f"Agent {self.config.name} started execution.",
            how=f"Instantiating {self.config.name} with model {self.config.model}.",
            why=self.config.description or f"Executing task assigned to {self.config.name}.",
            progress=0.1
        ), db=db)
        
        process_log = [f"{self.config.name} initiated: Analyzing objective."]
        
        try:
            # We want to make sure process gets the context, which it already does
            result_data = await self.process(input_data, context)
            
            # If the result is already a TaskResult, return it
            if isinstance(result_data, TaskResult):
                await event_bus.emit(AgentEvent(
                    agent_id=self.config.name,
                    event_type=AgentEventType.COMPLETED,
                    description=f"Agent {self.config.name} completed the task.",
                    how=f"Task result returned status: {result_data.status}",
                    why=f"Successful execution of {self.config.name} logic.",
                    progress=1.0
                ), db=db)
                return result_data
                
            # Otherwise, package it
            self.logger.info(f"Completed execution for agent {self.config.name}")
            
            await event_bus.emit(AgentEvent(
                agent_id=self.config.name,
                event_type=AgentEventType.COMPLETED,
                description=f"Agent {self.config.name} completed the task.",
                how=f"Final packaging of TaskResult.",
                why=f"Logical completion of agent-specific processing.",
                progress=1.0
            ), db=db)
            
            return TaskResult(
                data=result_data,
                status=TaskStatus.COMPLETED,
                process_log=process_log + [f"{self.config.name} completed the task."],
                educational_takeaway=f"Lesson from {self.config.name}: Focus on quality and consistency in {self.config.name} processes."
            )
            
        except Exception as e:
            self.logger.error(f"Error in agent {self.config.name}: {str(e)}", exc_info=True)
            await event_bus.emit(AgentEvent(
                agent_id=self.config.name,
                event_type=AgentEventType.FAILED,
                description=f"Agent {self.config.name} failed: {str(e)}",
                data={"error": str(e)},
                progress=1.0
            ), db=db)
            return TaskResult(
                data={"error": str(e)},
                status=TaskStatus.FAILED,
                process_log=process_log + [f"Error encountered: {str(e)}"]
            )
