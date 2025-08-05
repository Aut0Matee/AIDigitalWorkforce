"""
Message and conversation API endpoints with OpenAPI documentation.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.message import Message
from app.models.task import Task
from app.schemas.message import MessageResponse, MessageListResponse, MessageCreate

router = APIRouter()


@router.get(
    "/task/{task_id}",
    response_model=MessageListResponse,
    summary="Get Task Conversation",
    description="""
    Retrieve the complete conversation history for a specific task.
    
    Returns all messages in chronological order showing the multi-agent
    collaboration workflow from start to finish. Includes messages from:
    - **Researcher**: Information gathering and web search results
    - **Writer**: Content creation and drafting  
    - **Analyst**: Review, critique, and refinement suggestions
    - **Human**: User interventions and guidance
    - **System**: Workflow status and error messages
    """,
    responses={
        200: {"description": "Conversation retrieved successfully"},
        404: {"description": "Task not found"}
    }
)
async def get_task_messages(task_id: str, db: Session = Depends(get_db)):
    """
    Get all messages for a specific task.
    
    Args:
        task_id: Unique task identifier
        db: Database session
        
    Returns:
        MessageListResponse: Complete conversation history
        
    Raises:
        HTTPException: 404 if task not found
    """
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get all messages for the task
    messages = db.query(Message).filter(
        Message.task_id == task_id
    ).order_by(Message.created_at.asc()).all()
    
    return MessageListResponse(
        messages=messages,
        total=len(messages),
        task_id=task_id
    )


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=201,
    summary="Add Message to Conversation",
    description="""
    Add a new message to a task conversation.
    
    This endpoint is typically used for:
    - **Human interventions**: User providing guidance or feedback
    - **Agent responses**: AI agents communicating their progress
    - **System notifications**: Workflow status updates
    
    Messages are automatically timestamped and will trigger WebSocket
    notifications to connected clients.
    """,
    responses={
        201: {"description": "Message added successfully"},
        404: {"description": "Task not found"},
        400: {"description": "Invalid message data"}
    }
)
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """
    Add a new message to a task conversation.
    
    Args:
        message: Message data with content, agent role, and task ID
        db: Database session
        
    Returns:
        MessageResponse: Created message with metadata
        
    Raises:
        HTTPException: 404 if task not found
    """
    # Verify task exists
    task = db.query(Task).filter(Task.id == message.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Create new message
    db_message = Message(
        task_id=message.task_id,
        agent_role=message.agent_role,
        content=message.content
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # TODO: Trigger WebSocket notification to connected clients
    
    return db_message


@router.get(
    "/{message_id}",
    response_model=MessageResponse,
    summary="Get Message Details",
    description="""
    Retrieve details of a specific message.
    
    Returns the complete message information including content,
    agent role, timestamps, and associated task.
    """,
    responses={
        200: {"description": "Message found and returned"},
        404: {"description": "Message not found"}
    }
)
async def get_message(message_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific message by ID.
    
    Args:
        message_id: Unique message identifier
        db: Database session
        
    Returns:
        MessageResponse: Complete message information
        
    Raises:
        HTTPException: 404 if message not found
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message