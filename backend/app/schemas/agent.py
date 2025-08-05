"""
Pydantic schemas for agent-related operations.
"""

from pydantic import BaseModel
from app.models.message import AgentRole


class AgentInfo(BaseModel):
    """Schema for agent information."""
    role: AgentRole
    name: str
    description: str
    capabilities: list[str]
    
    class Config:
        schema_extra = {
            "example": {
                "role": "researcher",
                "name": "Research Agent",
                "description": "Specializes in web research and data gathering",
                "capabilities": [
                    "Web search and information retrieval",
                    "Data analysis and summarization", 
                    "Source verification and fact-checking"
                ]
            }
        }


class AgentListResponse(BaseModel):
    """Schema for available agents list."""
    agents: list[AgentInfo]
    
    class Config:
        schema_extra = {
            "example": {
                "agents": [
                    {
                        "role": "researcher",
                        "name": "Research Agent",
                        "description": "Specializes in web research and data gathering",
                        "capabilities": ["Web search", "Data analysis", "Source verification"]
                    },
                    {
                        "role": "writer", 
                        "name": "Content Writer",
                        "description": "Creates high-quality written content",
                        "capabilities": ["Content creation", "Copywriting", "Document formatting"]
                    },
                    {
                        "role": "analyst",
                        "name": "Quality Analyst", 
                        "description": "Reviews and improves content quality",
                        "capabilities": ["Content review", "Quality assessment", "Editing"]
                    }
                ]
            }
        }