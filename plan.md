# AI Digital Workforce - MVP System Plan

## Architecture Overview

### System Design Philosophy
- **Distinct Frontend/Backend**: Clear separation for scalability and maintainability
- **MVP Focus**: Core functionality only, avoid over-engineering
- **Open Source Ready**: Clean, documented, contribution-friendly structure
- **Real-time First**: WebSocket-driven communication for live agent collaboration

## Technology Stack

### Frontend
- **Framework**: Vite + React 18
- **Routing**: React Router v6
- **Styling**: Tailwind CSS
- **Real-time**: Socket.IO client
- **State Management**: React hooks + Context API (keep it simple for MVP)
- **UI Components**: Headless UI or React components for consistent design
- **Export**: Client-side PDF generation with jsPDF

### Backend
- **Framework**: FastAPI (Python)
- **Agent Orchestration**: LangGraph for multi-agent workflows
- **LLM Integration**: OpenAI API (GPT-4) with fallback to other providers
- **Real-time**: Socket.IO server
- **Database**: SQLite for MVP (easy deployment, no external deps)
- **Search Tool**: Tavily API for web research
- **File Storage**: Local filesystem for MVP deliverables

### Deployment
- **Development**: Docker Compose for easy local setup
- **Frontend**: Netlify or Vercel (static hosting, free tier)
- **Backend**: Render or Railway (free tier)
- **Database**: Embedded SQLite (migrates with backend)

## Core Components

### 1. Agent System
```
Agent Roles:
├── Researcher (web search, data gathering)
├── Writer (content creation, drafting)
└── Analyst (review, critique, refinement)

Agent Communication:
├── Message passing via WebSocket
├── Structured agent prompts
└── Turn-based collaboration flow
```

### 2. Task Management
```
Task Flow:
1. User creates task → Task ID generated
2. Agent orchestrator assigns roles
3. Agents collaborate in sequence
4. Final deliverable exported
5. Task marked complete
```

### 3. Real-time Interface
```
Frontend Components (React + Vite):
├── TaskCreation (simple form)
├── ChatWindow (agent messages)
├── TaskPanel (status, history)
├── DeliverableExport (download buttons)
├── UserInterjection (interrupt agents)
└── Router (React Router v6 for navigation)
```

## Data Models

### Task
```python
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus  # CREATED, IN_PROGRESS, COMPLETED
    created_at: datetime
    deliverable: Optional[str]  # Final output
```

### Message
```python
class Message:
    id: str
    task_id: str
    agent_role: AgentRole  # RESEARCHER, WRITER, ANALYST, HUMAN
    content: str
    timestamp: datetime
```

## MVP Scope Decisions

### What's Included
- 3 predefined agents (Researcher, Writer, Analyst)
- Single task processing (no queuing)
- Basic web search integration
- Real-time chat interface
- Markdown/PDF export
- Human interjection capability

### What's Excluded (Future)
- Custom agent creation
- Multiple simultaneous tasks
- Advanced integrations (Slack, Notion)
- Voice mode
- User authentication
- Task templates

## Security & Performance

### MVP Security
- Rate limiting on API endpoints
- Input validation and sanitization
- No user data persistence (tasks cleared on restart)
- Environment variables for API keys

### Performance Targets
- Agent response time: <5 seconds
- WebSocket latency: <500ms
- Concurrent users: 10-20 (MVP limit)

## Development Approach

### Phase 1: Core Backend (Week 1)
1. FastAPI setup with basic endpoints
2. Agent system with LangGraph
3. Database models and basic CRUD
4. WebSocket message handling

### Phase 2: Frontend Foundation (Week 2)
1. Vite + React setup with Tailwind
2. React Router configuration
3. Basic UI components
4. WebSocket client integration
5. Task creation and chat display

### Phase 3: Integration (Week 3)
1. Frontend-backend connectivity
2. Real-time agent communication
3. Task status management
4. Error handling and edge cases

### Phase 4: Polish & Deploy (Week 4)
1. Export functionality
2. UI/UX improvements
3. Documentation
4. Deployment setup

## File Structure Preview
```
ai-digital-workforce/
├── frontend/           # Vite + React SPA
├── backend/           # FastAPI application
├── docker-compose.yml # Local development
├── README.md          # Setup instructions
└── docs/             # Additional documentation
```