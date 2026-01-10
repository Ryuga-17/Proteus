#!/bin/bash

# Start Kiosk System (Backend + Frontend)

echo "🚀 Starting Kiosk System..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Start backend
echo -e "${BLUE}📡 Starting Kiosk Backend API...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

if [ ! -f ".deps_installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch .deps_installed
fi

echo -e "${GREEN}✅ Backend starting on http://localhost:8001${NC}"
python main.py &
BACKEND_PID=$!

cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo -e "${BLUE}🎨 Starting Kiosk Frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo -e "${GREEN}✅ Frontend starting on http://localhost:5174${NC}"
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo -e "${GREEN}✅ Kiosk System is running!${NC}"
echo ""
echo "📍 Services:"
echo "   • Backend API: http://localhost:8001"
echo "   • API Docs: http://localhost:8001/docs"
echo "   • Frontend: http://localhost:5174"
echo ""
echo "🛑 To stop, press Ctrl+C or run:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait

