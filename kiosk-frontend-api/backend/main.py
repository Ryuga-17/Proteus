"""
Kiosk Frontend API - QR Code Session Management & Data Fetching
Handles WhatsApp link sessions, shopping cart, and purchase history
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
import os
import uuid
import time
import json
import qrcode
import io
import base64
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for accessing main backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5174")
KIOSK_PORT = int(os.getenv("KIOSK_PORT", "8001"))
KIOSK_ID = os.getenv("KIOSK_ID", f"KIOSK-{uuid.uuid4().hex[:8].upper()}")  # Unique kiosk identifier
KIOSK_LOCATION_ID = os.getenv("KIOSK_LOCATION_ID", "store_main_street")  # Location from database

# In-memory storage (in production, use Redis or database)
kiosk_sessions: Dict[str, Dict[str, Any]] = {}
shopping_carts: Dict[str, List[Dict[str, Any]]] = {}  # user_id -> cart items
session_expiry_time = 3600  # 1 hour

app = FastAPI(
    title="Kiosk Frontend API",
    description="QR Code Session Management & Data Fetching for Kiosk System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5174", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Pydantic Models
# ============================================================================

class QRCodeSessionResponse(BaseModel):
    session_id: str
    kiosk_id: str
    location_id: Optional[str] = None
    qr_code_data_url: str
    session_url: str
    expires_at: str

class SessionStatusResponse(BaseModel):
    session_id: str
    kiosk_id: str
    location_id: Optional[str] = None
    status: str  # "pending", "linked", "expired"
    user_id: Optional[str] = None
    linked_at: Optional[str] = None
    expires_at: str

class LinkSessionRequest(BaseModel):
    session_id: str
    user_id: str
    device_info: Optional[Dict[str, Any]] = None

class ShoppingCartItem(BaseModel):
    product_id: str
    sku: Optional[str] = None
    quantity: int
    size: Optional[str] = None
    price: Optional[float] = None
    title: Optional[str] = None
    image: Optional[str] = None

class ShoppingCartResponse(BaseModel):
    user_id: str
    items: List[Dict[str, Any]]
    total_items: int
    subtotal: float
    updated_at: str

class PurchaseHistoryResponse(BaseModel):
    user_id: str
    orders: List[Dict[str, Any]]
    total_orders: int
    total_spent: float

class KioskDataResponse(BaseModel):
    session: SessionStatusResponse
    shopping_cart: Optional[ShoppingCartResponse] = None
    purchase_history: Optional[PurchaseHistoryResponse] = None

# ============================================================================
# Helper Functions
# ============================================================================

def generate_qr_code(data: str) -> str:
    """Generate QR code as base64 data URL"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    img_base64 = base64.b64encode(buffer.read()).decode()
    return f"data:image/png;base64,{img_base64}"

def cleanup_expired_sessions():
    """Remove expired sessions"""
    current_time = time.time()
    expired_sessions = [
        session_id for session_id, session_data in kiosk_sessions.items()
        if session_data.get("expires_at", 0) < current_time
    ]
    for session_id in expired_sessions:
        del kiosk_sessions[session_id]

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Kiosk Frontend API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    cleanup_expired_sessions()
    return {
        "status": "healthy",
        "active_sessions": len(kiosk_sessions),
        "backend_api_url": BACKEND_API_URL
    }

@app.post("/api/kiosk/session/qr", response_model=QRCodeSessionResponse)
async def generate_qr_session():
    """
    Generate a new QR code session for this kiosk
    Each kiosk has a unique KIOSK_ID (set via environment variable)
    User scans this QR code with their WhatsApp/device to link their account
    """
    cleanup_expired_sessions()
    
    # Generate unique session ID (includes kiosk_id for tracking)
    session_id = f"{KIOSK_ID}-{uuid.uuid4().hex[:12].upper()}"
    expires_at_time = time.time() + session_expiry_time
    
    # Create session with kiosk information
    kiosk_sessions[session_id] = {
        "session_id": session_id,
        "kiosk_id": KIOSK_ID,
        "location_id": KIOSK_LOCATION_ID,
        "status": "pending",
        "user_id": None,
        "created_at": time.time(),
        "expires_at": expires_at_time,
        "linked_at": None
    }
    
    # Generate session URL (includes kiosk_id for tracking)
    # In production, this would be a deep link or WhatsApp link
    session_url = f"{FRONTEND_URL}/kiosk/link?session={session_id}&kiosk={KIOSK_ID}"
    
    # Generate QR code
    qr_data_url = generate_qr_code(session_url)
    
    expires_at = datetime.fromtimestamp(expires_at_time).isoformat()
    
    print(f"\n{'='*70}")
    print(f"📱 QR SESSION GENERATED")
    print(f"{'='*70}")
    print(f"Kiosk ID: {KIOSK_ID}")
    print(f"Location ID: {KIOSK_LOCATION_ID}")
    print(f"Session ID: {session_id}")
    print(f"Expires At: {expires_at}")
    print(f"{'='*70}\n")
    
    return QRCodeSessionResponse(
        session_id=session_id,
        kiosk_id=KIOSK_ID,
        location_id=KIOSK_LOCATION_ID,
        qr_code_data_url=qr_data_url,
        session_url=session_url,
        expires_at=expires_at
    )

@app.get("/api/kiosk/session/{session_id}/status", response_model=SessionStatusResponse)
async def get_session_status(session_id: str):
    """Get status of a kiosk session"""
    cleanup_expired_sessions()
    
    if session_id not in kiosk_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = kiosk_sessions[session_id]
    
    # Check if expired
    if session["expires_at"] < time.time():
        session["status"] = "expired"
    
    expires_at = datetime.fromtimestamp(session["expires_at"]).isoformat()
    linked_at = datetime.fromtimestamp(session["linked_at"]).isoformat() if session.get("linked_at") else None
    
    return SessionStatusResponse(
        session_id=session_id,
        kiosk_id=session.get("kiosk_id", KIOSK_ID),
        location_id=session.get("location_id"),
        status=session["status"],
        user_id=session.get("user_id"),
        linked_at=linked_at,
        expires_at=expires_at
    )

@app.post("/api/kiosk/session/link", response_model=SessionStatusResponse)
async def link_session(request: LinkSessionRequest):
    """
    Link a user's device to a kiosk session
    Called when user scans QR code from their WhatsApp/device
    """
    cleanup_expired_sessions()
    
    if request.session_id not in kiosk_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = kiosk_sessions[request.session_id]
    
    # Check if expired
    if session["expires_at"] < time.time():
        session["status"] = "expired"
        raise HTTPException(status_code=410, detail="Session expired")
    
    # Link session to user
    session["user_id"] = request.user_id
    session["status"] = "linked"
    session["linked_at"] = time.time()
    session["device_info"] = request.device_info
    
    expires_at = datetime.fromtimestamp(session["expires_at"]).isoformat()
    linked_at = datetime.fromtimestamp(session["linked_at"]).isoformat()
    
    print(f"\n{'='*70}")
    print(f"🔗 SESSION LINKED")
    print(f"{'='*70}")
    print(f"Kiosk ID: {session.get('kiosk_id', KIOSK_ID)}")
    print(f"Location ID: {session.get('location_id')}")
    print(f"Session ID: {request.session_id}")
    print(f"User ID: {request.user_id}")
    print(f"Linked At: {linked_at}")
    print(f"{'='*70}\n")
    
    return SessionStatusResponse(
        session_id=request.session_id,
        kiosk_id=session.get("kiosk_id", KIOSK_ID),
        location_id=session.get("location_id"),
        status="linked",
        user_id=request.user_id,
        linked_at=linked_at,
        expires_at=expires_at
    )

@app.get("/api/kiosk/cart/{user_id}", response_model=ShoppingCartResponse)
async def get_shopping_cart(user_id: str):
    """Get user's shopping cart"""
    cart_items = shopping_carts.get(user_id, [])
    
    # Calculate totals
    total_items = sum(item.get("quantity", 0) for item in cart_items)
    subtotal = sum(item.get("price", 0) * item.get("quantity", 0) for item in cart_items)
    
    return ShoppingCartResponse(
        user_id=user_id,
        items=cart_items,
        total_items=total_items,
        subtotal=round(subtotal, 2),
        updated_at=datetime.now().isoformat()
    )

@app.post("/api/kiosk/cart/{user_id}/add")
async def add_to_cart(user_id: str, item: ShoppingCartItem):
    """Add item to shopping cart"""
    if user_id not in shopping_carts:
        shopping_carts[user_id] = []
    
    # Check if item already exists (same product_id and sku)
    existing_item = None
    for cart_item in shopping_carts[user_id]:
        if cart_item.get("product_id") == item.product_id and cart_item.get("sku") == item.sku:
            existing_item = cart_item
            break
    
    if existing_item:
        # Update quantity
        existing_item["quantity"] += item.quantity
    else:
        # Add new item
        shopping_carts[user_id].append(item.dict())
    
    return {"success": True, "message": "Item added to cart"}

@app.get("/api/kiosk/history/{user_id}", response_model=PurchaseHistoryResponse)
async def get_purchase_history(user_id: str):
    """
    Get user's purchase history from main backend
    Fetches orders from the main backend API
    """
    try:
        import httpx
        
        # In production, fetch from database via main backend
        # For now, use mock data structure
        # TODO: Integrate with main backend /api/orders endpoint
        
        # Mock purchase history structure
        orders = [
            {
                "order_id": "ORD-001",
                "order_date": "2024-01-15T10:30:00",
                "status": "delivered",
                "total_amount": 129.99,
                "items": [
                    {"product_id": "PROD-123", "title": "Classic White Sweatshirt", "quantity": 1, "price": 24.99},
                    {"product_id": "PROD-124", "title": "Premium Jeans", "quantity": 2, "price": 52.50}
                ]
            },
            {
                "order_id": "ORD-002",
                "order_date": "2024-01-10T14:20:00",
                "status": "shipped",
                "total_amount": 89.99,
                "items": [
                    {"product_id": "PROD-125", "title": "Running Shoes", "quantity": 1, "price": 89.99}
                ]
            }
        ]
        
        total_spent = sum(order["total_amount"] for order in orders)
        
        return PurchaseHistoryResponse(
            user_id=user_id,
            orders=orders,
            total_orders=len(orders),
            total_spent=total_spent
        )
        
    except Exception as e:
        print(f"Error fetching purchase history: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching purchase history: {str(e)}")

@app.get("/api/kiosk/data/{session_id}", response_model=KioskDataResponse)
async def get_kiosk_data(session_id: str):
    """
    Get all kiosk data for a session (session status, cart, purchase history)
    This is the main endpoint the kiosk UI calls to fetch all necessary data
    """
    cleanup_expired_sessions()
    
    # Get session status
    if session_id not in kiosk_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = kiosk_sessions[session_id]
    
    if session["status"] != "linked":
        # Return session status only if not linked
        expires_at = datetime.fromtimestamp(session["expires_at"]).isoformat()
        return KioskDataResponse(
            session=SessionStatusResponse(
                session_id=session_id,
                status=session["status"],
                user_id=session.get("user_id"),
                linked_at=None,
                expires_at=expires_at
            )
        )
    
    user_id = session["user_id"]
    
    # Get shopping cart
    cart = await get_shopping_cart(user_id)
    
    # Get purchase history
    history = await get_purchase_history(user_id)
    
    # Get session status
    session_status = await get_session_status(session_id)
    
    return KioskDataResponse(
        session=session_status,
        shopping_cart=cart,
        purchase_history=history
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=KIOSK_PORT)

