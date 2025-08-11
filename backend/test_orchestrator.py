#!/usr/bin/env python3
"""
Test script to verify agent orchestration is working.
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.task import Task, TaskStatus
from app.models.base import Base
from app.agents.orchestrator_fixed import get_orchestrator
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_orchestrator():
    """Test the orchestrator with a simple task."""
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create a test task
        test_task = Task(
            title="Test Task for Agent Orchestration",
            description="Write a short summary about artificial intelligence",
            status=TaskStatus.CREATED
        )
        
        db.add(test_task)
        db.commit()
        db.refresh(test_task)
        
        logger.info(f"Created test task with ID: {test_task.id}")
        
        # Get orchestrator
        orchestrator = get_orchestrator()
        logger.info("Orchestrator initialized")
        
        # Process the task
        logger.info(f"Starting task processing for task {test_task.id}")
        result = await orchestrator.process_task(test_task, db)
        
        logger.info(f"Task processing completed!")
        logger.info(f"Result length: {len(result)} characters")
        logger.info(f"Result preview: {result[:200]}...")
        
        # Check final task status
        db.refresh(test_task)
        logger.info(f"Final task status: {test_task.status}")
        
        return result
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Agent Orchestration")
    print("=" * 60)
    
    # Check if API key is set
    from app.config import settings
    if settings.openai_api_key == "sk-test-key-replace-with-real-key":
        print("\n⚠️  WARNING: OpenAI API key is not set!")
        print("Please set your OpenAI API key in the .env file or environment variables.")
        print("Export OPENAI_API_KEY=your-actual-key")
        sys.exit(1)
    
    print(f"\n✓ OpenAI API key configured")
    print("Starting orchestrator test...\n")
    
    # Run the test
    result = asyncio.run(test_orchestrator())
    
    if result:
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Test failed!")
        print("=" * 60)