"""
Pydantic schemas for message-related API operations.
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

from app.models.message import AgentRole


class MessageBase(BaseModel):
    """Base message schema with common fields."""
    content: str = Field(..., min_length=1, description="Message content")
    agent_role: AgentRole = Field(..., description="Role of the agent sending the message")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    task_id: str = Field(..., description="ID of the task this message belongs to")
    
    class Config:
        schema_extra = {
            "example": {
                "task_id": "123e4567-e89b-12d3-a456-426614174000",
                "content": "I'll start by researching the top electric vehicle startups using web search...",
                "agent_role": "researcher"
            }
        }


class MessageResponse(MessageBase):
    """Schema for message response with all fields."""
    id: str
    task_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "456e7890-e89b-12d3-a456-426614174001",
                "task_id": "123e4567-e89b-12d3-a456-426614174000",
                "content": "I found 10 promising electric vehicle startups. Here's what I discovered...",
                "agent_role": "researcher",
                "created_at": "2025-01-15T10:35:00Z"
            }
        }


class MessageListResponse(BaseModel):
    """Schema for task message list response."""
    messages: List[MessageResponse]
    total: int
    task_id: str
    
    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    {
                        "id": "456e7890-e89b-12d3-a456-426614174001",
                        "task_id": "123e4567-e89b-12d3-a456-426614174000",
                        "content": "I'll research electric vehicle startups...",
                        "agent_role": "researcher",
                        "created_at": "2025-01-15T10:35:00Z"
                    },
                    {
                        "id": "789e1234-e89b-12d3-a456-426614174002", 
                        "task_id": "123e4567-e89b-12d3-a456-426614174000",
                        "content": "Based on the research, I'll now write a comprehensive report...",
                        "agent_role": "writer",
                        "created_at": "2025-01-15T10:40:00Z"
                    }
                ],
                "total": 8,
                "task_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }