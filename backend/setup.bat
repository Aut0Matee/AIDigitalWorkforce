@echo off
REM Setup script for Windows local backend development

echo Setting up AI Digital Workforce Backend...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install fastapi uvicorn[standard] pydantic pydantic-settings
pip install sqlalchemy alembic
pip install python-socketio python-multipart
pip install openai langchain langgraph tavily-python
pip install python-dotenv httpx aiofiles jinja2
pip install passlib python-jose[cryptography]
pip install pytest pytest-asyncio black flake8 mypy

echo Creating requirements.txt...
pip freeze > requirements.txt

REM Create .env file from example if it doesn't exist
if not exist .env (
    echo Creating .env file from example...
    copy .env.example .env
    echo Please edit .env and add your API keys!
)

REM Create data directory
if not exist data mkdir data

echo.
echo Setup complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate
echo.
echo To start the backend server, run:
echo   uvicorn main:socket_app --reload --host 0.0.0.0 --port 8000
echo.
echo Don't forget to add your API keys to the .env file!