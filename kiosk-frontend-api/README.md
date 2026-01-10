# Kiosk Frontend API System

QR Code-based session management system for kiosk integration with WhatsApp link sessions. Allows users to scan a QR code with their device to link their account and view shopping cart and purchase history on the kiosk.

## Features

- 📱 **QR Code Generation**: Generate unique QR codes for kiosk sessions
- 🔗 **Session Linking**: Link user's device (WhatsApp/mobile) to kiosk session
- 🛒 **Shopping Cart Display**: View user's shopping cart on kiosk
- 📜 **Purchase History**: Display user's past purchase history
- ⏱️ **Session Management**: Automatic session expiration and cleanup
- 🔄 **Real-time Updates**: Polling-based updates for session status

## Architecture

```
Kiosk System
├── backend/          # FastAPI backend (Port 8001)
│   ├── main.py      # API endpoints
│   └── requirements.txt
└── frontend/        # React frontend (Port 5174)
    ├── src/
    │   ├── components/  # UI components
    │   ├── services/    # API service
    │   └── App.jsx
    └── package.json
```

## Setup

### Backend Setup

1. **Install dependencies:**
```bash
cd kiosk-frontend-api/backend
pip install -r requirements.txt
```

2. **Configure environment variables:**
Create a `.env` file in `backend/`:
```env
BACKEND_API_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5174
KIOSK_PORT=8001
```

3. **Start the backend:**
```bash
python main.py
# Or with uvicorn:
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd kiosk-frontend-api/frontend
npm install
```

2. **Configure environment variables:**
Create a `.env` file in `frontend/`:
```env
VITE_API_URL=http://localhost:8001
```

3. **Start the frontend:**
```bash
npm run dev
```

The kiosk UI will be available at `http://localhost:5174`

## API Endpoints

### Session Management

- `POST /api/kiosk/session/qr` - Generate QR code session
- `GET /api/kiosk/session/{session_id}/status` - Get session status
- `POST /api/kiosk/session/link` - Link user device to session
- `GET /api/kiosk/data/{session_id}` - Get all kiosk data (session + cart + history)

### Shopping Cart

- `GET /api/kiosk/cart/{user_id}` - Get user's shopping cart
- `POST /api/kiosk/cart/{user_id}/add` - Add item to cart

### Purchase History

- `GET /api/kiosk/history/{user_id}` - Get user's purchase history

### Health Check

- `GET /api/health` - Health check endpoint

## Workflow

1. **Kiosk displays QR code:**
   - Kiosk generates a new session and displays QR code
   - QR code contains a session URL

2. **User scans QR code:**
   - User opens the session URL on their WhatsApp/device
   - User's device calls `/api/kiosk/session/link` with user_id

3. **Session linked:**
   - Backend links the session to the user
   - Kiosk polls `/api/kiosk/data/{session_id}` every 2 seconds

4. **Display data:**
   - Once linked, kiosk displays:
     - Shopping cart
     - Purchase history
     - Session information

## Session Lifecycle

- **Pending**: QR code generated, waiting for user to scan
- **Linked**: User has scanned QR code and linked their account
- **Expired**: Session expired (default: 1 hour)

## Data Models

### Session
```json
{
  "session_id": "KIOSK-ABC123",
  "status": "linked",
  "user_id": "USER123",
  "linked_at": "2024-01-15T10:30:00",
  "expires_at": "2024-01-15T11:30:00"
}
```

### Shopping Cart
```json
{
  "user_id": "USER123",
  "items": [
    {
      "product_id": "PROD-123",
      "sku": "SKU-123",
      "quantity": 2,
      "price": 24.99,
      "title": "Product Name"
    }
  ],
  "total_items": 2,
  "subtotal": 49.98
}
```

### Purchase History
```json
{
  "user_id": "USER123",
  "orders": [
    {
      "order_id": "ORD-001",
      "order_date": "2024-01-15T10:30:00",
      "status": "delivered",
      "total_amount": 129.99,
      "items": [...]
    }
  ],
  "total_orders": 5,
  "total_spent": 450.00
}
```

## Integration with Main Backend

The kiosk system is designed to work alongside the main backend API (`backend/main.py`). To integrate with real data:

1. **Shopping Cart**: Currently uses in-memory storage. Integrate with Redis or database for persistence.

2. **Purchase History**: Currently returns mock data. Integrate with main backend's `/api/orders` endpoint or database.

3. **User Authentication**: Add authentication/authorization for secure session linking.

## Development Notes

- Sessions are stored in-memory (use Redis in production)
- Shopping carts are stored in-memory (integrate with database)
- Purchase history currently returns mock data (integrate with database)
- QR codes expire after 1 hour (configurable via `session_expiry_time`)
- Frontend polls every 2 seconds for session updates

## Future Enhancements

- [ ] Redis/database integration for session and cart storage
- [ ] Real-time WebSocket updates instead of polling
- [ ] User authentication and authorization
- [ ] Integration with main backend API for real data
- [ ] WhatsApp Business API integration for deep linking
- [ ] Session analytics and tracking
- [ ] Multi-kiosk support with location tracking

## License

Part of the Proteus Agentic System

