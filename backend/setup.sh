#!/bin/bash

# Setup script for local backend development

echo "🚀 Setting up AI Digital Workforce Backend..."

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install fastapi uvicorn[standard] pydantic pydantic-settings
pip install sqlalchemy alembic
pip install python-socketio python-multipart
pip install openai langchain langgraph tavily-python
pip install python-dotenv httpx aiofiles jinja2
pip install passlib python-jose[cryptography]
pip install pytest pytest-asyncio black flake8 mypy

# Create requirements.txt from installed packages
echo "📝 Creating requirements.txt..."
pip freeze > requirements.txt

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    echo "🔐 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
fi

# Create data directory
mkdir -p data

echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the backend server, run:"
echo "  uvicorn main:socket_app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Don't forget to add your API keys to the .env file!"