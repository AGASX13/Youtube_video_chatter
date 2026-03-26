@echo off
REM Quick Start Script for Windows
REM This script sets up and runs YouTube Video Chatter

cls
echo.
echo ======================================
echo YouTube Video Chatter - Quick Start
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Copying environment configuration...
if not exist .env (
    copy .env.example .env
    echo Created .env from .env.example
)

echo [5/5] Creating necessary directories...
if not exist logs mkdir logs
if not exist data mkdir data
if not exist data\vectorstore_store mkdir data\vectorstore_store

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Make sure Ollama is running: ollama serve
echo 2. Download models:
echo    ollama pull llama3
echo    ollama pull nomic-embed-text
echo 3. Start the application:
echo    streamlit run ui/streamlit_app.py
echo.
echo.
pause
