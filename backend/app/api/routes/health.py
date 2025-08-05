"""
Health check endpoints for system monitoring.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    service: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="System Health Check",
    description="Check if the API service is running and healthy",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "version": "0.1.0", 
                        "service": "ai-digital-workforce-backend"
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Perform a basic health check of the service.
    
    Returns basic service information and confirms the API is operational.
    Used for monitoring and load balancer health checks.
    """
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        service="ai-digital-workforce-backend"
    )