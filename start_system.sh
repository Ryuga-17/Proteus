#!/bin/bash

# Start the complete Proteus Agentic System
# This script starts both backend and frontend

echo "🚀 Starting Proteus Agentic System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0
    else
        return 1
    fi
}

# Check backend port
if check_port 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use. Backend may already be running.${NC}"
else
    echo -e "${GREEN}✅ Port 8000 is available for backend${NC}"
fi

# Check frontend port
if check_port 5173; then
    echo -e "${YELLOW}⚠️  Port 5173 is already in use. Frontend may already be running.${NC}"
else
    echo -e "${GREEN}✅ Port 5173 is available for frontend${NC}"
fi

echo ""
echo "📦 Starting Backend Server..."
echo ""

# Start backend in background
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install backend dependencies if needed
if [ ! -f ".deps_installed" ]; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
    touch .deps_installed
fi

# Start backend server
echo -e "${BLUE}Backend starting on http://localhost:8000${NC}"
echo -e "${BLUE}API docs: http://localhost:8000/docs${NC}"
python main.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Go back to root
cd ..

echo ""
echo "🎨 Starting Frontend Server..."
echo ""

# Start frontend
cd "Proteus_EY/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (this may take a minute)..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
fi

# Start frontend
echo -e "${BLUE}Frontend starting on http://localhost:5173${NC}"
npm run dev &
FRONTEND_PID=$!

# Go back to root
cd ../..

echo ""
echo -e "${GREEN}✅ System is starting!${NC}"
echo ""
echo "📍 Services:"
echo "   • Backend API: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • Frontend: http://localhost:5173"
echo ""
echo "🛑 To stop the system, press Ctrl+C or run:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "⏳ Waiting for services to start..."
sleep 5

# Check if services are running
if check_port 8000 && check_port 5173; then
    echo -e "${GREEN}✅ Both services are running!${NC}"
    echo ""
    echo "🌐 Open http://localhost:5173 in your browser"
else
    echo -e "${YELLOW}⚠️  Some services may still be starting...${NC}"
fi

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait




