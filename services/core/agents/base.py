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

    async def run(self, input_data: Any, context: Optional[Dict] = None) -> TaskResult:
        """
        Wrapper around process to handle logging, errors, and common middleware.
        Ensures output is a structured TaskResult for Theater/Education.
        """
        self.logger.info(f"Starting execution for agent {self.config.name}")
        
        # Initial Theater Entry
        event_bus.emit(AgentEvent(
            agent_id=self.config.name,
            event_type=AgentEventType.STARTED,
            description=f"Agent {self.config.name} started execution.",
            how=f"Instantiating {self.config.name} with model {self.config.model}.",
            why=self.config.description or f"Executing task assigned to {self.config.name}.",
            progress=0.1
        ))
        
        process_log = [f"{self.config.name} initiated: Analyzing objective."]
        
        try:
            result_data = await self.process(input_data, context)
            
            # If the result is already a TaskResult, return it
            if isinstance(result_data, TaskResult):
                event_bus.emit(AgentEvent(
                    agent_id=self.config.name,
                    event_type=AgentEventType.COMPLETED,
                    description=f"Agent {self.config.name} completed the task.",
                    how=f"Task result returned status: {result_data.status}",
                    why=f"Successful execution of {self.config.name} logic.",
                    progress=1.0
                ))
                return result_data
                
            # Otherwise, package it
            self.logger.info(f"Completed execution for agent {self.config.name}")
            
            event_bus.emit(AgentEvent(
                agent_id=self.config.name,
                event_type=AgentEventType.COMPLETED,
                description=f"Agent {self.config.name} completed the task.",
                how=f"Final packaging of TaskResult.",
                why=f"Logical completion of agent-specific processing.",
                progress=1.0
            ))
            
            return TaskResult(
                data=result_data,
                status=TaskStatus.COMPLETED,
                process_log=process_log + [f"{self.config.name} completed the task."],
                educational_takeaway=f"Lesson from {self.config.name}: Focus on quality and consistency in {self.config.name} processes."
            )
            
        except Exception as e:
            self.logger.error(f"Error in agent {self.config.name}: {str(e)}", exc_info=True)
            event_bus.emit(AgentEvent(
                agent_id=self.config.name,
                event_type=AgentEventType.FAILED,
                description=f"Agent {self.config.name} failed: {str(e)}",
                data={"error": str(e)},
                progress=1.0
            ))
            return TaskResult(
                data={"error": str(e)},
                status=TaskStatus.FAILED,
                process_log=process_log + [f"Error encountered: {str(e)}"]
            )
