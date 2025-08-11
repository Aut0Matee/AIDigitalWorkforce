#!/usr/bin/env python3
"""
Initialize the database by creating all required tables.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import models to register them with Base
from app.models.base import Base
from app.models.task import Task
from app.models.message import Message
from app.database import engine

def init_database():
    """Initialize database tables."""
    print("Creating database tables...")
    print(f"Database URL: {engine.url}")
    
    # Drop all tables first (for clean slate)
    Base.metadata.drop_all(bind=engine)
    print("Dropped existing tables (if any)")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")
    print("\nTables created:")
    for table in Base.metadata.tables:
        print(f"  - {table}")
    
    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print("\nVerified tables in database:")
    for table in existing_tables:
        print(f"  ✓ {table}")

if __name__ == "__main__":
    init_database()