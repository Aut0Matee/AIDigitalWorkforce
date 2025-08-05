# Contributing to AI Digital Workforce

Thank you for your interest in contributing to AI Digital Workforce! This document provides guidelines and information for contributors.

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please treat all community members with respect and create a positive environment for everyone.

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-digital-workforce.git
   cd ai-digital-workforce
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```

3. **Start development environment**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

## 📝 How to Contribute

### Reporting Bugs

1. Check if the bug already exists in [Issues](https://github.com/automate/ai-digital-workforce/issues)
2. Create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details

### Suggesting Features

1. Check [Issues](https://github.com/automate/ai-digital-workforce/issues) for existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Code Contributions

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run backend tests
   cd backend && pytest
   
   # Run frontend tests
   cd frontend && npm test
   
   # Run linting
   cd backend && black . && flake8
   cd frontend && npm run lint
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## 🎨 Coding Standards

### Backend (Python)

- **Formatting**: Use [Black](https://black.readthedocs.io/) for code formatting
- **Linting**: Use [Flake8](https://flake8.pycqa.org/) for linting
- **Type Hints**: Use type hints for all functions and classes
- **Docstrings**: Use Google-style docstrings

```python
def create_task(title: str, description: str) -> Task:
    """
    Create a new task for agent processing.
    
    Args:
        title: The task title
        description: Detailed task description
        
    Returns:
        Task: The created task instance
        
    Raises:
        ValueError: If title or description is empty
    """
    pass
```

### Frontend (TypeScript/React)

- **Formatting**: Use [Prettier](https://prettier.io/) for code formatting
- **Linting**: Use [ESLint](https://eslint.org/) for linting
- **Components**: Use functional components with hooks
- **TypeScript**: Use strict type checking

```typescript
interface TaskProps {
  title: string;
  description: string;
  onComplete: (result: string) => void;
}

const TaskComponent: React.FC<TaskProps> = ({ title, description, onComplete }) => {
  // Component implementation
};
```

### General Guidelines

- **Commit Messages**: Use [Conventional Commits](https://www.conventionalcommits.org/)
  - `feat:` for new features
  - `fix:` for bug fixes  
  - `docs:` for documentation changes
  - `refactor:` for code refactoring
  - `test:` for adding tests

- **Branch Naming**:
  - `feature/description` for new features
  - `fix/description` for bug fixes
  - `docs/description` for documentation

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
pytest --cov=app tests/  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Tests

```bash
docker-compose -f docker-compose.test.yml up --build
```

## 📚 Documentation

When adding new features:

1. **Update API documentation** - OpenAPI schemas are auto-generated
2. **Update README.md** - Add new features to the feature list
3. **Add inline comments** - For complex logic
4. **Update type definitions** - Keep TypeScript types current

## 🔧 Development Tips

### Debugging

- **Backend**: Use `DEBUG=true` in `.env` for detailed logs
- **Frontend**: Use `VITE_ENABLE_DEBUG=true` for debug features
- **Database**: SQLite browser for inspecting database

### Hot Reloading

- Backend: `uvicorn main:socket_app --reload`
- Frontend: `npm run dev`
- Docker: Use `docker-compose.dev.yml` for development

### Adding New Agents

1. Create agent class in `backend/app/agents/`
2. Add to `AgentRole` enum in `models/message.py`
3. Update orchestrator in `agents/orchestrator.py`
4. Add frontend avatar in `public/agents/`
5. Update UI components to handle new agent type

## 🎯 Areas for Contribution

### High Priority

- [ ] **Agent System**: More specialized agents (Coder, Designer, etc.)
- [ ] **UI/UX**: Improved dashboard and chat interface
- [ ] **Performance**: Optimize WebSocket connections
- [ ] **Testing**: Increase test coverage

### Medium Priority

- [ ] **Integrations**: Slack, Discord, Notion connectors
- [ ] **Export**: More export formats (DOCX, HTML)
- [ ] **Analytics**: Usage tracking and metrics
- [ ] **Mobile**: Responsive mobile interface

### Low Priority

- [ ] **Voice**: Speech-to-text and text-to-speech
- [ ] **Themes**: Dark mode and custom themes
- [ ] **Localization**: Multi-language support
- [ ] **Plugins**: Plugin system for extensions

## ❓ Questions?

- **General Questions**: Open a [Discussion](https://github.com/automate/ai-digital-workforce/discussions)
- **Bug Reports**: Create an [Issue](https://github.com/automate/ai-digital-workforce/issues)
- **Feature Requests**: Create an [Issue](https://github.com/automate/ai-digital-workforce/issues)
- **Direct Contact**: contact@automate.com

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Hall of Fame for major contributions

Thank you for contributing to AI Digital Workforce! 🚀