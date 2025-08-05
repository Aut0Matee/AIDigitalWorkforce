# AI Digital Workforce Backend

## Setup Instructions

### WSL/Ubuntu Users

If you're using WSL (Windows Subsystem for Linux) or Ubuntu, you need to install `python3-venv` first:

```bash
# Update package list
sudo apt update

# Install python3-venv
sudo apt install python3-venv

# Now run the setup script
./setup.sh
```

### Manual Setup (All Platforms)

If the setup script doesn't work, you can set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
python -m pip install fastapi uvicorn[standard] pydantic pydantic-settings
python -m pip install sqlalchemy alembic
python -m pip install python-socketio python-multipart
python -m pip install openai langchain langgraph tavily-python
python -m pip install python-dotenv httpx aiofiles jinja2
python -m pip install passlib python-jose[cryptography]
python -m pip install pytest pytest-asyncio black flake8 mypy

# Generate requirements.txt
python -m pip freeze > requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your API keys
```

### Running the Backend

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the server
uvicorn main:socket_app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc