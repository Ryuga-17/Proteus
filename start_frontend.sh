#!/bin/bash

# Start only the frontend server

echo "🎨 Starting Proteus Frontend..."
echo ""

cd "Proteus_EY/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies (this may take a minute)..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
fi

echo ""
echo "✅ Frontend starting on http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start dev server
npm run dev




