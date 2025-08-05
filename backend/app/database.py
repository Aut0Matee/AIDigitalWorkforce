"""
Database configuration and session management for SQLAlchemy.

Provides database connection, session management, and table creation utilities.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings

logger = logging.getLogger(__name__)

# Create database engine
if settings.database_url.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        settings.database_url,
        connect_args={
            "check_same_thread": False,  # Allow SQLite to be used with multiple threads
        },
        poolclass=StaticPool,  # Use static pool for SQLite
        echo=settings.debug,  # Log SQL queries in debug mode
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_tables():
    """Create all database tables."""
    try:
        # Import models to register them with Base
        from app.models import task, message  # noqa: F401
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise