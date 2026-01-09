# Backend API - Proteus Agentic System

## Overview

FastAPI backend that connects the Proteus_EY frontend with the agentic system.

## Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python main.py
# Or with uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access API
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health

## API Endpoints

### Health Check
```
GET /
GET /api/health
```

### Voice Recommendations
```
POST /api/recommendations/voice
Body: {
  "query": "looking for a shirt for date",
  "user_id": "CUST001"
}
```

### General Recommendations
```
POST /api/recommendations
Body: {
  "query": "show me running shoes",
  "user_id": "CUST001"
}
```

### Agent Query (Orchestrator)
```
POST /api/agent/query
Body: {
  "request": "Check stock for SKU-123",
  "user_id": "default_user"
}
```

### Products
```
GET /api/products?category=women&search=running&limit=50
GET /api/products/{product_id}
GET /api/categories
```

## Backend Configuration

### Environment Variables

Create a `.env` file in the `backend` directory with the following:

```bash
# Frontend URL - Set the URL where your frontend is running
# For a single URL:
FRONTEND_URL=http://localhost:5173

# For multiple URLs (comma-separated):
# FRONTEND_URL=http://localhost:5173,http://localhost:3000,https://yourdomain.com

# Optional: Demo mode (default: True)
# DEMO_MODE=True
```

The backend will automatically load these environment variables and configure CORS to allow requests from the specified frontend URL(s).

If `FRONTEND_URL` is not set, the backend defaults to:
- http://localhost:5173 (Vite default)
- http://localhost:3000 (Alternative)
- http://127.0.0.1:5173

## Frontend Configuration

Add to `.env` in frontend:
```
VITE_API_URL=http://localhost:8000
```

## Integration Flow

```
Frontend (VoiceSearch.tsx)
    ↓
POST /api/recommendations/voice
    ↓
Backend (main.py)
    ↓
Recommendation Agent 2
    ↓
Ollama + Qdrant
    ↓
Results → Frontend
```

## CORS

CORS is configured automatically based on the `FRONTEND_URL` environment variable in the backend `.env` file. The backend will allow requests from the specified frontend URL(s).

If no `.env` file is present or `FRONTEND_URL` is not set, it defaults to common development URLs (localhost:5173, localhost:3000, 127.0.0.1:5173).




