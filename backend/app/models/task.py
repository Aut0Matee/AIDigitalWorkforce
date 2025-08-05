"""
Task model for managing AI workflow tasks.
"""

from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class TaskStatus(enum.Enum):
    """Task status enumeration."""
    CREATED = "created"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    """
    Task model representing an AI workflow task.
    
    A task is created by a user and processed by multiple AI agents
    in collaboration to produce a deliverable output.
    """
    
    __tablename__ = "tasks"
    
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.CREATED, nullable=False, index=True)
    deliverable = Column(Text, nullable=True)  # Final output from agents
    
    # Relationship to messages
    messages = relationship("Message", back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Task(id='{self.id}', title='{self.title}', status='{self.status.value}')>"