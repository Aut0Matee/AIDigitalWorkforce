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

# Check if venv module is available
echo "🔍 Checking for python3-venv..."
if ! python3 -m venv --help &> /dev/null; then
    echo "❌ python3-venv is not installed."
    echo "📦 Please install it with:"
    echo "   sudo apt install python3-venv  # For Ubuntu/Debian"
    echo "   sudo yum install python3-venv  # For RHEL/CentOS"
    echo ""
    echo "After installing, run this script again."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Check if venv was created successfully
if [ ! -f venv/bin/activate ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
python -m pip install fastapi uvicorn[standard] pydantic pydantic-settings
python -m pip install sqlalchemy alembic
python -m pip install python-socketio python-multipart
python -m pip install openai langchain langgraph tavily-python
python -m pip install python-dotenv httpx aiofiles jinja2
python -m pip install passlib python-jose[cryptography]
python -m pip install pytest pytest-asyncio black flake8 mypy

# Create requirements.txt from installed packages
echo "📝 Creating requirements.txt..."
python -m pip freeze > requirements.txt

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