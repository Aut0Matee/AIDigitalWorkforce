"""
Configuration management for the AI Digital Workforce backend.

Uses Pydantic Settings for environment variable management with validation.
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="info", description="Logging level")
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    
    # Database
    database_type: str = Field(
        default="sqlite",
        description="Database type (sqlite or mysql)"
    )
    database_url: str = Field(
        default="sqlite:///./data/database.db",
        description="Database connection URL"
    )
    
    # API Keys
    openai_api_key: str = Field(
        default="sk-test-key-replace-with-real-key",
        description="OpenAI API key for LLM integration"
    )
    tavily_api_key: str = Field(
        default="tvly-test-key-replace-with-real-key",
        description="Tavily API key for web search"
    )
    
    # Security
    secret_key: str = Field(
        default="test-secret-key-change-in-production",
        description="Secret key for JWT tokens and sessions"
    )
    
    # CORS
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed CORS origins"
    )
    
    # Agent Configuration
    max_agent_retries: int = Field(
        default=3,
        description="Maximum retry attempts for agent operations"
    )
    agent_timeout_seconds: int = Field(
        default=30,
        description="Timeout for individual agent operations"
    )
    max_concurrent_tasks: int = Field(
        default=5,
        description="Maximum number of concurrent tasks"
    )
    
    # WebSocket Configuration
    ws_ping_interval: int = Field(
        default=25,
        description="WebSocket ping interval in seconds"
    )
    ws_ping_timeout: int = Field(
        default=60,
        description="WebSocket ping timeout in seconds"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()