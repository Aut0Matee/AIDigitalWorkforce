"""
Message model for agent communication and chat history.
"""

from sqlalchemy import Column, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class AgentRole(enum.Enum):
    """Agent role enumeration."""
    RESEARCHER = "researcher"
    WRITER = "writer"
    ANALYST = "analyst"
    HUMAN = "human"
    SYSTEM = "system"


class Message(BaseModel):
    """
    Message model representing communication between agents and humans.
    
    Messages are part of a task conversation and track the multi-agent
    collaboration workflow.
    """
    
    __tablename__ = "messages"
    
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False, index=True)
    agent_role = Column(Enum(AgentRole), nullable=False, index=True)
    content = Column(Text, nullable=False)
    
    # Relationship to task
    task = relationship("Task", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id='{self.id}', task_id='{self.task_id}', agent='{self.agent_role.value}')>"