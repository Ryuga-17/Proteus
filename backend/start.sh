#!/bin/bash
# Quick start script for backend server

echo "🚀 Starting Proteus Agentic System Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start server
echo ""
echo "✅ Starting server on http://localhost:8000"
echo "📖 API docs available at http://localhost:8000/docs"
echo ""
python main.py




