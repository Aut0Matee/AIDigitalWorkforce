#!/usr/bin/env python3
"""
Initialize MySQL database with tables for the AI Digital Workforce.
Run this after MySQL permissions are configured to allow WSL connections.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models.base import Base
import app.models.task
import app.models.message
from sqlalchemy import text

def init_database():
    """Initialize the MySQL database with required tables."""
    
    print("=" * 60)
    print("Initializing MySQL Database for AI Digital Workforce")
    print("=" * 60)
    
    try:
        # Test connection
        print("Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text('SELECT VERSION() as version'))
            version = result.fetchone()[0]
            print(f"✅ Connected to MySQL {version}")
            
            result = conn.execute(text('SELECT DATABASE() as db'))
            db_name = result.fetchone()[0]
            print(f"✅ Using database: {db_name}")
        
        # Create tables
        print("\nCreating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Verify tables
        print("\nVerifying created tables...")
        with engine.connect() as conn:
            result = conn.execute(text('SHOW TABLES'))
            tables = result.fetchall()
            table_names = [table[0] for table in tables]
            
            for table in table_names:
                print(f"  • {table}")
            
            print(f"\n✅ {len(table_names)} tables created successfully!")
        
        # Test basic operations
        print("\nTesting database operations...")
        db = SessionLocal()
        try:
            from app.models.task import Task, TaskStatus
            
            # Try to query tasks table
            count = db.query(Task).count()
            print(f"✅ Tasks table accessible (current count: {count})")
            
        finally:
            db.close()
        
        print("\n" + "=" * 60)
        print("✅ MySQL Database initialization completed successfully!")
        print("✅ The system is now ready to use MySQL instead of SQLite")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        print("\nPossible solutions:")
        print("1. Ensure MySQL server is running on Windows")
        print("2. Grant WSL access in MySQL:")
        print("   CREATE USER 'root'@'172.18.%' IDENTIFIED BY 'root';")
        print("   GRANT ALL PRIVILEGES ON dg_workforce.* TO 'root'@'172.18.%';")
        print("   FLUSH PRIVILEGES;")
        print("3. Verify the database 'dg_workforce' exists")
        sys.exit(1)

if __name__ == "__main__":
    init_database()