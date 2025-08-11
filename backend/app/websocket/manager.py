"""
WebSocket connection manager using Socket.IO for real-time communication.
"""

import logging
import socketio
from typing import Dict, Set
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.allowed_origins,
    ping_interval=settings.ws_ping_interval,
    ping_timeout=settings.ws_ping_timeout,
    logger=settings.debug,
    engineio_logger=settings.debug
)


class ConnectionManager:
    """Manages WebSocket connections and task subscriptions."""
    
    def __init__(self):
        # Track active connections by session ID
        self.active_connections: Dict[str, str] = {}  # session_id -> task_id
        # Track task subscribers
        self.task_subscribers: Dict[str, Set[str]] = {}  # task_id -> set of session_ids
    
    async def connect(self, sid: str, task_id: str = None):
        """Register a new connection."""
        self.active_connections[sid] = task_id
        
        if task_id:
            if task_id not in self.task_subscribers:
                self.task_subscribers[task_id] = set()
            self.task_subscribers[task_id].add(sid)
            
        logger.info(f"Client {sid} connected" + (f" to task {task_id}" if task_id else ""))
    
    async def disconnect(self, sid: str):
        """Handle client disconnection."""
        task_id = self.active_connections.get(sid)
        
        if task_id and task_id in self.task_subscribers:
            self.task_subscribers[task_id].discard(sid)
            if not self.task_subscribers[task_id]:
                del self.task_subscribers[task_id]
        
        if sid in self.active_connections:
            del self.active_connections[sid]
            
        logger.info(f"Client {sid} disconnected")
    
    async def subscribe_to_task(self, sid: str, task_id: str):
        """Subscribe a client to task updates."""
        # Remove from previous task if any
        old_task_id = self.active_connections.get(sid)
        if old_task_id and old_task_id in self.task_subscribers:
            self.task_subscribers[old_task_id].discard(sid)
        
        # Subscribe to new task
        self.active_connections[sid] = task_id
        if task_id not in self.task_subscribers:
            self.task_subscribers[task_id] = set()
        self.task_subscribers[task_id].add(sid)
        
        logger.info(f"Client {sid} subscribed to task {task_id}")
    
    async def broadcast_to_task(self, task_id: str, event: str, data: dict):
        """Broadcast an event to all subscribers of a task."""
        if task_id in self.task_subscribers:
            subscribers = list(self.task_subscribers[task_id])
            if subscribers:
                logger.info(f"Broadcasting {event} to {len(subscribers)} clients for task {task_id}")
                await sio.emit(event, data, room=None, skip_sid=None, to=subscribers)
    
    async def send_to_client(self, sid: str, event: str, data: dict):
        """Send an event to a specific client."""
        await sio.emit(event, data, room=sid)


# Global connection manager instance
connection_manager = ConnectionManager()


@sio.event
async def connect(sid, environ, auth):
    """Handle client connection."""
    task_id = auth.get("task_id") if auth else None
    await connection_manager.connect(sid, task_id)
    
    await sio.emit("connected", {
        "message": "Successfully connected to AI Digital Workforce",
        "session_id": sid,
        "task_id": task_id
    }, room=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    await connection_manager.disconnect(sid)


@sio.event
async def subscribe_task(sid, data):
    """Handle task subscription."""
    task_id = data.get("task_id")
    if not task_id:
        await sio.emit("error", {"message": "task_id is required"}, room=sid)
        return
    
    await connection_manager.subscribe_to_task(sid, task_id)
    await sio.emit("task_subscribed", {"task_id": task_id}, room=sid)


@sio.event
async def human_intervention(sid, data):
    """Handle human intervention during agent workflow."""
    task_id = data.get("task_id")
    message = data.get("message")
    
    if not task_id or not message:
        await sio.emit("error", {
            "message": "task_id and message are required"
        }, room=sid)
        return
    
    # Store human intervention as a message
    from app.database import SessionLocal
    from app.models.message import Message, AgentRole
    
    db = SessionLocal()
    try:
        human_message = Message(
            task_id=task_id,
            agent_role=AgentRole.HUMAN,
            content=message
        )
        db.add(human_message)
        db.commit()
    finally:
        db.close()
    
    # Broadcast intervention to all task subscribers
    await connection_manager.broadcast_to_task(task_id, "human_intervention", {
        "task_id": task_id,
        "message": message,
        "timestamp": str(datetime.utcnow())
    })


# Helper functions for external use
async def notify_task_started(task_id: str, task_data: dict):
    """Notify clients that a task has started."""
    await connection_manager.broadcast_to_task(task_id, "task_started", {
        "task_id": task_id,
        "task": task_data,
        "timestamp": str(datetime.utcnow())
    })


async def notify_agent_message(task_id: str, message_data: dict):
    """Notify clients of a new agent message."""
    # Support both dict and individual parameters
    if isinstance(message_data, dict):
        # Ensure 'message' field exists for frontend compatibility
        if 'content' in message_data and 'message' not in message_data:
            message_data['message'] = message_data['content']
        
        await connection_manager.broadcast_to_task(task_id, "agent_message", {
            "task_id": task_id,
            **message_data
        })
    else:
        # Legacy support
        await connection_manager.broadcast_to_task(task_id, "agent_message", {
            "task_id": task_id,
            "agent_role": message_data,
            "message": "",
            "timestamp": str(datetime.utcnow())
        })


async def notify_task_completed(task_id: str, deliverable: str):
    """Notify clients that a task has been completed."""
    await connection_manager.broadcast_to_task(task_id, "task_completed", {
        "task_id": task_id,
        "deliverable": deliverable,
        "timestamp": str(datetime.utcnow())
    })


async def notify_error(task_id: str, error_message: str):
    """Notify clients of an error during task processing."""
    await connection_manager.broadcast_to_task(task_id, "error", {
        "task_id": task_id,
        "error": error_message,
        "timestamp": str(datetime.utcnow())
    })