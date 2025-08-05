# AI Digital Workforce API Documentation

This document provides detailed information about the AI Digital Workforce REST API and WebSocket endpoints.

## Base URL

- **Development**: http://localhost:8000
- **Production**: https://your-domain.com

## Authentication

Currently, the API does not require authentication for the MVP version. Future versions will include API key authentication.

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## REST API Endpoints

### Health Check

#### GET /api/health

Check if the API service is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "service": "ai-digital-workforce-backend"
}
```

### Tasks

#### POST /api/tasks/

Create a new AI workflow task.

**Request Body:**
```json
{
  "title": "Market Research Report",
  "description": "Research the top 5 electric vehicle startups in 2025 and create a comprehensive market analysis report."
}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Market Research Report",
  "description": "Research the top 5 electric vehicle startups...",
  "status": "created",
  "deliverable": null,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": null
}
```

#### GET /api/tasks/

Retrieve a paginated list of all tasks.

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `size` (int, optional): Items per page (default: 10, max: 100)
- `status` (str, optional): Filter by task status (`created`, `in_progress`, `completed`, `failed`)

**Response:**
```json
{
  "tasks": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Market Research Report",
      "description": "Research the top 5 electric vehicle startups...",
      "status": "completed",
      "deliverable": "# Electric Vehicle Startups Report...",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T11:45:30Z"
    }
  ],
  "total": 25,
  "page": 1,
  "size": 10
}
```

#### GET /api/tasks/{task_id}

Retrieve details of a specific task.

**Path Parameters:**
- `task_id` (str): Unique task identifier

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Market Research Report",
  "description": "Research the top 5 electric vehicle startups...",
  "status": "completed",
  "deliverable": "# Electric Vehicle Startups Report\n\n## Executive Summary...",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T11:45:30Z"
}
```

#### PUT /api/tasks/{task_id}

Update specific fields of an existing task.

**Path Parameters:**
- `task_id` (str): Unique task identifier

**Request Body:**
```json
{
  "title": "Updated Title",
  "status": "completed",
  "deliverable": "Final report content..."
}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated Title",
  "description": "Original description...",
  "status": "completed",
  "deliverable": "Final report content...",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T12:00:00Z"
}
```

#### DELETE /api/tasks/{task_id}

Delete a task and all associated messages.

**Path Parameters:**
- `task_id` (str): Unique task identifier

**Response:** 204 No Content

### Messages

#### GET /api/messages/task/{task_id}

Retrieve the complete conversation history for a specific task.

**Path Parameters:**
- `task_id` (str): Unique task identifier

**Response:**
```json
{
  "messages": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174001",
      "task_id": "123e4567-e89b-12d3-a456-426614174000",
      "content": "I'll start by researching electric vehicle startups using web search...",
      "agent_role": "researcher",
      "created_at": "2025-01-15T10:35:00Z"
    },
    {
      "id": "789e1234-e89b-12d3-a456-426614174002",
      "task_id": "123e4567-e89b-12d3-a456-426614174000",
      "content": "Based on the research, I'll now write a comprehensive report...",
      "agent_role": "writer",
      "created_at": "2025-01-15T10:40:00Z"
    }
  ],
  "total": 8,
  "task_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### POST /api/messages/

Add a new message to a task conversation.

**Request Body:**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "content": "Please focus more on European companies in your analysis.",
  "agent_role": "human"
}
```

**Response:**
```json
{
  "id": "abc1234-e89b-12d3-a456-426614174003",
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "content": "Please focus more on European companies in your analysis.",
  "agent_role": "human",
  "created_at": "2025-01-15T10:45:00Z"
}
```

#### GET /api/messages/{message_id}

Retrieve details of a specific message.

**Path Parameters:**
- `message_id` (str): Unique message identifier

**Response:**
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174001",
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "content": "I found 10 promising electric vehicle startups...",
  "agent_role": "researcher",
  "created_at": "2025-01-15T10:35:00Z"
}
```

## WebSocket API

The WebSocket API provides real-time communication for live agent interactions.

### Connection

**URL:** `ws://localhost:8000/socket.io/`

**Authentication:** Optional task_id in auth payload

```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:8000', {
  auth: {
    task_id: 'optional-task-id'
  }
});
```

### Events

#### Client → Server Events

##### `subscribe_task`
Subscribe to updates for a specific task.

```javascript
socket.emit('subscribe_task', {
  task_id: '123e4567-e89b-12d3-a456-426614174000'
});
```

##### `human_intervention`
Send human intervention during agent workflow.

```javascript
socket.emit('human_intervention', {
  task_id: '123e4567-e89b-12d3-a456-426614174000',
  message: 'Please focus on European markets only.'
});
```

#### Server → Client Events

##### `connected`
Confirmation of successful connection.

```javascript
socket.on('connected', (data) => {
  console.log('Connected:', data);
  // { message: "Successfully connected...", session_id: "...", task_id: "..." }
});
```

##### `task_subscribed`
Confirmation of task subscription.

```javascript
socket.on('task_subscribed', (data) => {
  console.log('Subscribed to task:', data.task_id);
});
```

##### `task_started`
Notification that a task has begun processing.

```javascript
socket.on('task_started', (data) => {
  console.log('Task started:', data);
  // { task_id: "...", task: {...}, timestamp: "..." }
});
```

##### `agent_message`
Real-time agent message during collaboration.

```javascript
socket.on('agent_message', (data) => {
  console.log('Agent message:', data);
  // { task_id: "...", agent_role: "researcher", message: "...", timestamp: "..." }
});
```

##### `task_completed`
Notification that a task has been completed.

```javascript
socket.on('task_completed', (data) => {
  console.log('Task completed:', data);
  // { task_id: "...", deliverable: "...", timestamp: "..." }
});
```

##### `human_intervention`
Broadcast of human intervention to all task subscribers.

```javascript
socket.on('human_intervention', (data) => {
  console.log('Human intervention:', data);
  // { task_id: "...", message: "...", timestamp: "..." }
});
```

##### `error`
Error notification during task processing.

```javascript
socket.on('error', (data) => {
  console.error('Error:', data);
  // { task_id: "...", error: "...", timestamp: "..." }
});
```

## Data Models

### Task Status

```typescript
type TaskStatus = 'created' | 'in_progress' | 'completed' | 'failed';
```

### Agent Roles

```typescript
type AgentRole = 'researcher' | 'writer' | 'analyst' | 'human' | 'system';
```

### Task

```typescript
interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  deliverable: string | null;
  created_at: string;
  updated_at: string | null;
}
```

### Message

```typescript
interface Message {
  id: string;
  task_id: string;
  content: string;
  agent_role: AgentRole;
  created_at: string;
}
```

## Error Handling

### HTTP Status Codes

- `200` - OK
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

### Error Response Format

```json
{
  "detail": "Task not found"
}
```

### Validation Error Format

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

Currently no rate limiting is implemented in the MVP. Future versions will include:
- 100 requests per minute per IP
- 10 concurrent WebSocket connections per IP
- Task creation limited to 5 per minute

## Examples

### Python Example

```python
import requests
import socketio

# Create a task
response = requests.post('http://localhost:8000/api/tasks/', json={
    'title': 'Market Research',
    'description': 'Research EV startups in 2025'
})
task = response.json()

# Connect to WebSocket
sio = socketio.Client()

@sio.on('agent_message')
def on_agent_message(data):
    print(f"{data['agent_role']}: {data['message']}")

sio.connect('http://localhost:8000')
sio.emit('subscribe_task', {'task_id': task['id']})
```

### JavaScript Example

```javascript
// Create a task
const response = await fetch('http://localhost:8000/api/tasks/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Market Research',
    description: 'Research EV startups in 2025'
  })
});
const task = await response.json();

// Connect to WebSocket
import io from 'socket.io-client';
const socket = io('http://localhost:8000');

socket.on('agent_message', (data) => {
  console.log(`${data.agent_role}: ${data.message}`);
});

socket.emit('subscribe_task', { task_id: task.id });
```

## Changelog

### v0.1.0 (Current)
- Initial API implementation
- Task CRUD operations
- Message management
- WebSocket real-time communication
- OpenAPI documentation