"""
AI Digital Workforce Backend - FastAPI Application

Main application entry point with OpenAPI documentation, CORS, and WebSocket support.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import socketio

from app.config import settings
from app.database import create_tables
from app.api.routes import tasks, messages, health
from app.websocket.manager import sio


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown tasks."""
    # Startup
    logger.info("Starting AI Digital Workforce Backend...")
    await create_tables()
    logger.info("Database tables created/verified")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Digital Workforce Backend...")


# Create FastAPI application with comprehensive OpenAPI documentation
app = FastAPI(
    title="AI Digital Workforce API",
    description="""
    ## AI Digital Workforce Backend API
    
    A comprehensive API for managing multi-agent AI collaboration workflows.
    
    ### Features
    - **Multi-Agent System**: Researcher, Writer, and Analyst agents
    - **Real-time Communication**: WebSocket support for live agent interactions
    - **Task Management**: Create, track, and export AI-generated deliverables
    - **Web Search Integration**: Tavily API for research capabilities
    - **Export Functionality**: Generate PDF and Markdown outputs
    
    ### Agent Workflow
    1. **Researcher** gathers information from web sources
    2. **Writer** creates content based on research findings  
    3. **Analyst** reviews and refines the output
    4. **Human** can intervene at any stage for guidance
    
    ### Getting Started
    1. Create a new task via `/api/tasks/`
    2. Connect to WebSocket at `/socket.io/` for real-time updates
    3. Watch agents collaborate and provide input as needed
    4. Export final deliverables when complete
    
    ### WebSocket Events
    - `task_started`: Task begins processing
    - `agent_message`: Agent sends a message
    - `task_completed`: Task finished with deliverable
    - `error`: Error occurred during processing
    """,
    version="0.1.0",
    terms_of_service="https://github.com/automate/ai-digital-workforce/blob/main/LICENSE",
    contact={
        "name": "AutoMate Team",
        "url": "https://github.com/automate/ai-digital-workforce",
        "email": "contact@automate.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/automate/ai-digital-workforce/blob/main/LICENSE",
    },
    openapi_tags=[
        {
            "name": "tasks",
            "description": "Task management operations - create, retrieve, and manage AI workflows",
        },
        {
            "name": "messages", 
            "description": "Message operations - retrieve agent conversations and chat history",
        },
        {
            "name": "health",
            "description": "System health and status monitoring",
        },
        {
            "name": "websocket",
            "description": "Real-time WebSocket communication for live agent interactions",
        },
    ],
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(messages.router, prefix="/api/messages", tags=["messages"])

# Mount Socket.IO application
socket_app = socketio.ASGIApp(sio, app)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "service": "ai-digital-workforce-backend"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:socket_app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )