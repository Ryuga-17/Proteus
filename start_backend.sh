#!/bin/bash

# Start only the backend server

echo "🚀 Starting Proteus Backend API..."
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install dependencies if needed
if [ ! -f ".deps_installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch .deps_installed
fi

echo ""
echo "✅ Backend starting on http://localhost:8000"
echo "📖 API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start server
python main.py




