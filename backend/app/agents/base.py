"""
Base agent class for all AI agents in the digital workforce.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from app.models.message import AgentRole
from app.websocket.manager import notify_agent_message

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the digital workforce.
    
    Each agent has a specific role and capabilities, and can communicate
    with other agents through the orchestrator.
    """
    
    def __init__(self, role: AgentRole, name: str, description: str):
        self.role = role
        self.name = name
        self.description = description
        self.capabilities: List[str] = []
        self.system_prompt: str = ""
        
    @abstractmethod
    async def process(self, task_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task with the given context.
        
        Args:
            task_id: Unique identifier for the task
            context: Current task context including previous agent outputs
            
        Returns:
            Dict containing the agent's output and any additional data
        """
        pass
    
    async def send_message(self, task_id: str, message: str):
        """
        Send a message to the task conversation and notify via WebSocket.
        
        Args:
            task_id: Task identifier
            message: Message content
        """
        logger.info(f"{self.name} sending message for task {task_id}: {message[:100]}...")
        
        # Notify via WebSocket for real-time updates
        await notify_agent_message(task_id, self.role.value, message)
        
        # Return message data for storage
        return {
            "task_id": task_id,
            "agent_role": self.role,
            "content": message,
            "timestamp": datetime.utcnow()
        }
    
    def get_system_prompt(self) -> str:
        """Get the agent's system prompt for LLM interactions."""
        return self.system_prompt or f"""You are {self.name}, a specialized AI agent.

Role: {self.description}

Capabilities:
{chr(10).join(f'- {cap}' for cap in self.capabilities)}

Guidelines:
- Be professional and focused on your role
- Provide clear, actionable insights
- Collaborate effectively with other agents
- Stay within your area of expertise
"""
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(role={self.role.value}, name={self.name})>"