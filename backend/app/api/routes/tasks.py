"""
Task management API endpoints with comprehensive OpenAPI documentation.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskListResponse

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=201,
    summary="Create New Task",
    description="""
    Create a new AI workflow task that will be processed by multiple agents.
    
    The task will be assigned to a multi-agent workflow where:
    1. **Researcher** gathers information from web sources
    2. **Writer** creates content based on research
    3. **Analyst** reviews and refines the output
    
    Real-time updates will be sent via WebSocket as agents collaborate.
    """,
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid task data"},
        422: {"description": "Validation error"}
    }
)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task for AI agent processing.
    
    Args:
        task: Task creation data with title and description
        db: Database session
        
    Returns:
        TaskResponse: Created task with generated ID and metadata
    """
    db_task = Task(
        title=task.title,
        description=task.description,
        status=TaskStatus.CREATED
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Trigger agent workflow processing
    from app.services.task_service import get_task_service
    task_service = get_task_service()
    
    # Process task in background
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(task_service.process_task_async(db_task.id))
    
    return db_task


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="List Tasks",
    description="""
    Retrieve a paginated list of all tasks with filtering options.
    
    Tasks are returned in descending order by creation date (newest first).
    Use pagination parameters to manage large result sets.
    """,
    responses={
        200: {"description": "Tasks retrieved successfully"},
        400: {"description": "Invalid query parameters"}
    }
)
async def list_tasks(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    size: int = Query(10, ge=1, le=100, description="Number of tasks per page"),
    status: TaskStatus = Query(None, description="Filter by task status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of tasks.
    
    Args:
        page: Page number for pagination
        size: Number of tasks per page  
        status: Optional status filter
        db: Database session
        
    Returns:
        TaskListResponse: Paginated list of tasks with metadata
    """
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination and ordering
    tasks = query.order_by(Task.created_at.desc()).offset((page - 1) * size).limit(size).all()
    
    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        size=size
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get Task Details",
    description="""
    Retrieve detailed information about a specific task.
    
    Returns the complete task data including any generated deliverable
    and current processing status.
    """,
    responses={
        200: {"description": "Task found and returned"},
        404: {"description": "Task not found"}
    }
)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by ID.
    
    Args:
        task_id: Unique task identifier
        db: Database session
        
    Returns:
        TaskResponse: Complete task information
        
    Raises:
        HTTPException: 404 if task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update Task",
    description="""
    Update specific fields of an existing task.
    
    Allows updating title, description, status, or deliverable content.
    Only provided fields will be updated.
    """,
    responses={
        200: {"description": "Task updated successfully"},
        404: {"description": "Task not found"},
        400: {"description": "Invalid update data"}
    }
)
async def update_task(
    task_id: str, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    
    Args:
        task_id: Unique task identifier
        task_update: Fields to update
        db: Database session
        
    Returns:
        TaskResponse: Updated task information
        
    Raises:
        HTTPException: 404 if task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only provided fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    
    return task


@router.delete(
    "/{task_id}",
    status_code=204,
    summary="Delete Task",
    description="""
    Delete a task and all associated messages.
    
    This operation is irreversible and will remove all conversation
    history and deliverables associated with the task.
    """,
    responses={
        204: {"description": "Task deleted successfully"},
        404: {"description": "Task not found"}
    }
)
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Delete a task and all associated data.
    
    Args:
        task_id: Unique task identifier
        db: Database session
        
    Raises:
        HTTPException: 404 if task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return None