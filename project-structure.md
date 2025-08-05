# AI Digital Workforce - Project Structure (Vite + React)

## Root Directory Structure
```
ai-digital-workforce/
├── README.md                    # Main project documentation
├── LICENSE                      # MIT license
├── docker-compose.yml          # Local development setup
├── .gitignore                  # Git ignore rules
├── docs/                       # Additional documentation
│   ├── setup.md               # Setup instructions
│   ├── contributing.md        # Contribution guidelines
│   ├── architecture.md        # System architecture
│   └── api.md                 # API documentation
├── frontend/                   # Vite + React SPA
└── backend/                    # FastAPI application
```

## Frontend Structure (Vite + React)
```
frontend/
├── package.json                # Dependencies and scripts
├── vite.config.ts             # Vite configuration
├── tailwind.config.js         # Tailwind CSS config
├── tsconfig.json              # TypeScript configuration
├── .env.local                 # Environment variables
├── .gitignore                 # Frontend specific ignores
├── index.html                 # HTML entry point
├── public/                    # Static assets
│   ├── agents/               # Agent avatar images
│   │   ├── researcher.svg
│   │   ├── writer.svg
│   │   └── analyst.svg
│   └── favicon.ico
├── src/
│   ├── main.tsx               # Application entry point
│   ├── App.tsx                # Root App component
│   ├── index.css              # Global styles
│   ├── components/            # React components
│   │   ├── ui/               # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── index.ts      # Barrel exports
│   │   ├── chat/             # Chat-related components
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── AgentAvatar.tsx
│   │   │   ├── TypingIndicator.tsx
│   │   │   └── index.ts
│   │   ├── task/             # Task management components
│   │   │   ├── TaskCreation.tsx
│   │   │   ├── TaskPanel.tsx
│   │   │   ├── TaskStatus.tsx
│   │   │   ├── TaskHistory.tsx
│   │   │   └── index.ts
│   │   ├── export/           # Export functionality
│   │   │   ├── ExportModal.tsx
│   │   │   ├── DeliverableViewer.tsx
│   │   │   └── index.ts
│   │   └── layout/           # Layout components
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       ├── MainLayout.tsx
│   │       └── index.ts
│   ├── pages/                # Route components
│   │   ├── Home.tsx          # Landing/dashboard page
│   │   ├── Task.tsx          # Individual task page
│   │   ├── History.tsx       # Task history page
│   │   └── NotFound.tsx      # 404 page
│   ├── hooks/                # Custom React hooks
│   │   ├── useSocket.ts      # WebSocket connection
│   │   ├── useTask.ts        # Task management
│   │   ├── useChat.ts        # Chat functionality
│   │   └── useLocalStorage.ts # Local storage hook
│   ├── services/             # API and external services
│   │   ├── api.ts            # API client configuration
│   │   ├── socket.ts         # Socket.IO client setup
│   │   ├── taskService.ts    # Task-related API calls
│   │   └── exportService.ts  # Export utilities
│   ├── utils/                # Utility functions
│   │   ├── constants.ts      # App constants
│   │   ├── helpers.ts        # General utilities
│   │   ├── formatters.ts     # Data formatting
│   │   └── validators.ts     # Input validation
│   ├── types/                # TypeScript type definitions
│   │   ├── task.ts
│   │   ├── message.ts
│   │   ├── agent.ts
│   │   ├── api.ts
│   │   └── index.ts          # Barrel exports
│   ├── context/              # React Context providers
│   │   ├── TaskContext.tsx   # Task state management
│   │   ├── SocketContext.tsx # WebSocket context
│   │   └── AppContext.tsx    # Global app state
│   └── router/               # React Router configuration
│       ├── AppRouter.tsx     # Main router component
│       ├── routes.tsx        # Route definitions
│       └── ProtectedRoute.tsx # Route protection (future)
```

## Backend Structure (FastAPI)
```
backend/
├── pyproject.toml             # Python dependencies (Poetry)
├── requirements.txt           # Pip dependencies (alternative)
├── .env                       # Environment variables
├── .gitignore                 # Backend specific ignores
├── Dockerfile                 # Container configuration
├── main.py                    # FastAPI application entry point
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection and setup
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── task.py            # Task model
│   │   ├── message.py         # Message model
│   │   └── base.py            # Base model class
│   ├── schemas/               # Pydantic schemas (API contracts)
│   │   ├── __init__.py
│   │   ├── task.py            # Task schemas
│   │   ├── message.py         # Message schemas
│   │   └── agent.py           # Agent schemas
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── routes/            # Route definitions
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py       # Task management endpoints
│   │   │   ├── messages.py    # Message endpoints
│   │   │   └── health.py      # Health check endpoint
│   │   └── deps.py            # Dependency injection
│   ├── agents/                # AI Agent system
│   │   ├── __init__.py
│   │   ├── base.py            # Base agent class
│   │   ├── researcher.py      # Researcher agent
│   │   ├── writer.py          # Writer agent
│   │   ├── analyst.py         # Analyst agent
│   │   ├── orchestrator.py    # Agent orchestration
│   │   └── prompts/           # Agent prompt templates
│   │       ├── researcher.txt
│   │       ├── writer.txt
│   │       └── analyst.txt
│   ├── services/              # Business logic services
│   │   ├── __init__.py
│   │   ├── task_service.py    # Task management logic
│   │   ├── agent_service.py   # Agent coordination
│   │   ├── search_service.py  # Web search integration
│   │   └── export_service.py  # Export functionality
│   ├── websocket/             # WebSocket handling
│   │   ├── __init__.py
│   │   ├── manager.py         # WebSocket connection manager
│   │   ├── handlers.py        # Message handlers
│   │   └── events.py          # Event definitions
│   ├── tools/                 # External tool integrations
│   │   ├── __init__.py
│   │   ├── web_search.py      # Tavily API integration
│   │   └── llm_client.py      # OpenAI API client
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── logging.py         # Logging configuration
│       ├── security.py        # Security utilities
│       └── helpers.py         # General helpers
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_agents/          # Agent tests
│   ├── test_api/             # API endpoint tests
│   └── test_services/        # Service layer tests
├── alembic/                   # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── data/                      # Local data storage
│   ├── database.db           # SQLite database
│   └── exports/              # Generated deliverables
└── scripts/                   # Utility scripts
    ├── setup.py              # Setup script
    └── seed_db.py            # Database seeding
```

## Key Configuration Files

### Frontend Configuration

#### vite.config.ts
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'http://localhost:8000',
        ws: true,
      },
    },
  },
})
```

#### package.json (Frontend)
```json
{
  "name": "ai-digital-workforce-frontend",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext ts,tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "socket.io-client": "^4.7.0",
    "@headlessui/react": "^1.7.0",
    "jspdf": "^2.5.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.4.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0"
  }
}
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./data/database.db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
    volumes:
      - ./backend:/app
      - ./backend/data:/app/data
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

## Key Architectural Decisions

### Frontend (Vite + React)
- **Vite**: Fast development server with HMR and optimized builds
- **React Router v6**: Client-side routing for SPA navigation
- **Tailwind CSS**: Utility-first styling for rapid UI development
- **TypeScript**: Type safety throughout the application
- **Socket.IO Client**: Real-time communication with backend

### Backend (FastAPI)
- **FastAPI**: High-performance async Python framework
- **SQLAlchemy**: ORM for database operations
- **LangGraph**: Multi-agent workflow orchestration
- **SQLite**: Embedded database for MVP simplicity
- **Socket.IO**: WebSocket server for real-time communication

### Development Benefits
- **Hot Module Replacement**: Instant updates during development
- **Static Build Output**: Easy deployment to CDNs/static hosts
- **Clear Separation**: Frontend and backend can be developed independently
- **Type Safety**: Full TypeScript coverage for better DX

This structure provides a clean, scalable foundation for the AI Digital Workforce MVP with modern tooling and best practices.