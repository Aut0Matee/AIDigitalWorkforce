"""
Task processing service for managing AI agent workflows.
"""

import logging
import asyncio
from typing import Optional
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus
from app.agents.orchestrator import get_orchestrator
from app.database import SessionLocal

logger = logging.getLogger(__name__)


class TaskProcessingService:
    """Service for processing tasks through the multi-agent workflow."""
    
    def __init__(self):
        self.orchestrator = get_orchestrator()
        self._processing_tasks = set()  # Track active tasks
    
    async def process_task_async(self, task_id: str):
        """
        Process a task asynchronously.
        
        Args:
            task_id: ID of the task to process
        """
        if task_id in self._processing_tasks:
            logger.warning(f"Task {task_id} is already being processed")
            return
            
        self._processing_tasks.add(task_id)
        
        try:
            # Get task from database
            db = SessionLocal()
            try:
                task = db.query(Task).filter(Task.id == task_id).first()
                
                if not task:
                    logger.error(f"Task {task_id} not found")
                    return
                    
                if task.status != TaskStatus.CREATED:
                    logger.warning(f"Task {task_id} already processed (status: {task.status})")
                    return
                
                # Process through orchestrator
                logger.info(f"Starting processing for task {task_id}: {task.title}")
                
                deliverable = await self.orchestrator.process_task(task, db)
                
                logger.info(f"Task {task_id} processing completed")
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {str(e)}")
            
        finally:
            self._processing_tasks.discard(task_id)
    
    def process_task_background(self, task_id: str):
        """
        Queue a task for background processing.
        
        Args:
            task_id: ID of the task to process
        """
        # Create a new event loop for the background task
        # In production, use a proper task queue like Celery
        asyncio.create_task(self.process_task_async(task_id))
        
        logger.info(f"Task {task_id} queued for processing")
    
    def is_processing(self, task_id: str) -> bool:
        """Check if a task is currently being processed."""
        return task_id in self._processing_tasks
    
    def get_active_tasks(self) -> list:
        """Get list of currently processing task IDs."""
        return list(self._processing_tasks)


# Global service instance
_task_service = None


def get_task_service() -> TaskProcessingService:
    """Get or create the global task processing service."""
    global _task_service
    if _task_service is None:
        _task_service = TaskProcessingService()
    return _task_service