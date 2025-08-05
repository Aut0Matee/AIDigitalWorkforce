"""
Pydantic schemas for task-related API operations.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.task import TaskStatus


class TaskBase(BaseModel):
    """Base task schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: str = Field(..., min_length=1, description="Detailed task description")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Market Research on EV Startups",
                "description": "Research the top electric vehicle startups in 2025 and create a comprehensive report with market analysis, funding information, and competitive landscape."
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating task fields."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[TaskStatus] = None
    deliverable: Optional[str] = None


class TaskResponse(TaskBase):
    """Schema for task response with all fields."""
    id: str
    status: TaskStatus
    deliverable: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Market Research on EV Startups", 
                "description": "Research the top electric vehicle startups...",
                "status": "completed",
                "deliverable": "# Electric Vehicle Startups Report\n\n## Executive Summary\n...",
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T11:45:30Z"
            }
        }


class TaskListResponse(BaseModel):
    """Schema for paginated task list response."""
    tasks: List[TaskResponse]
    total: int
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)
    
    class Config:
        schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Market Research on EV Startups",
                        "description": "Research the top electric vehicle startups...",
                        "status": "completed",
                        "deliverable": "# Report content...",
                        "created_at": "2025-01-15T10:30:00Z",
                        "updated_at": "2025-01-15T11:45:30Z"
                    }
                ],
                "total": 25,
                "page": 1,
                "size": 10
            }
        }