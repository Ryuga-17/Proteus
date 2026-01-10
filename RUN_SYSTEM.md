# 🚀 Running the Complete System

## Quick Start

### Option 1: Run Everything (Recommended)

```bash
./start_system.sh
```

This will start both backend and frontend automatically.

### Option 2: Run Separately

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

### Option 3: Manual Start

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd Proteus_EY/frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

## Access Points

Once running:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

## System Components

### Backend (Port 8000)
- FastAPI server
- Connects to all agents
- Handles API requests

### Frontend (Port 5173)
- React + TypeScript
- Voice search
- Shopping cart
- Product browsing

### Agents (Via Backend)
- Orchestrator
- Recommendation Agent 2
- Inventory Agent
- Payment Agent
- Fulfillment Agent
- Loyalty Agent
- Support Agent

## Testing the System

### 1. Test Backend Health
```bash
curl http://localhost:8000/api/health
```

### 2. Test Voice Search
1. Open http://localhost:5173
2. Click voice search button
3. Say: "looking for a shirt for date"
4. See recommendations

### 3. Test Purchase Flow
1. Add items to cart
2. Click "Proceed to pay"
3. Check backend logs for stock reduction
4. Verify order ID shown

### 4. Test API Directly
```bash
# Voice recommendations
curl -X POST http://localhost:8000/api/recommendations/voice \
  -H "Content-Type: application/json" \
  -d '{"query": "looking for a shirt", "user_id": "CUST001"}'

# Check stock
curl http://localhost:8000/api/inventory/stock/sku_123

# Process purchase
curl -X POST http://localhost:8000/api/purchase \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product_id": "123", "sku": "sku_123", "quantity": 1}],
    "user_id": "TEST_USER"
  }'
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill it
kill -9 $(lsof -ti:8000)

# Same for port 5173
kill -9 $(lsof -ti:5173)
```

### Backend Won't Start
- Check Python version: `python3 --version` (need 3.8+)
- Install dependencies: `pip install -r backend/requirements.txt`
- Check for errors in terminal

### Frontend Won't Start
- Check Node.js: `node --version` (need 18+)
- Install dependencies: `cd Proteus_EY/frontend && npm install`
- Check `.env` file exists with `VITE_API_URL=http://localhost:8000`

### CORS Errors
- Verify backend is running on port 8000
- Check `VITE_API_URL` in frontend `.env`
- Check browser console for errors

### No Recommendations
- Check backend logs
- Verify Recommendation Agent 2 is set up
- Check Ollama/Qdrant if using real services

## System Architecture

```
┌─────────────────┐
│   Frontend      │
│  (React/TS)     │
│  Port: 5173     │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   Backend API   │
│   (FastAPI)     │
│   Port: 8000    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│Orch.  │ │ Agents  │
└───┬───┘ └─────────┘
    │
┌───▼──────────────────┐
│  Recommendation      │
│  Inventory           │
│  Payment             │
│  Fulfillment         │
│  Loyalty             │
│  Support             │
└──────────────────────┘
```

## Next Steps

1. **Test Voice Search** - Try different queries
2. **Test Purchase** - Complete a purchase and verify stock reduction
3. **Check API Docs** - Visit http://localhost:8000/docs
4. **Explore Features** - Browse products, use cart, etc.

## Stopping the System

- **If using start_system.sh:** Press Ctrl+C
- **If running separately:** Press Ctrl+C in each terminal
- **Kill processes:**
  ```bash
  kill -9 $(lsof -ti:8000)
  kill -9 $(lsof -ti:5173)
  ```

Enjoy your agentic system! 🎉




