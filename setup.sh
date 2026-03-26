#!/bin/bash
# Quick Start Script for Linux/macOS
# This script sets up and runs YouTube Video Chatter

clear

echo "======================================"
echo "YouTube Video Chatter - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    echo "Ubuntu: sudo apt-get install python3 python3-venv"
    echo "macOS: brew install python3"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Copying environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

echo "[5/5] Creating necessary directories..."
mkdir -p logs
mkdir -p data/vectorstore_store

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Download models:"
echo "   ollama pull llama3"
echo "   ollama pull nomic-embed-text"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Start the application:"
echo "   streamlit run ui/streamlit_app.py"
echo ""
