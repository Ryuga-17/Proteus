"""
Fulfillment Tools - The Helper Functions for Getting Orders Delivered! 🛠️

These tools are what the fulfillment agent uses to actually get things done:
1. book_shipment - Creates shipments with logistics partners for home delivery
2. reserve_in_store - Reserves items at stores for customer pickup
3. notify_staff - Sends notifications to warehouse/store staff queues

Each tool simulates calling real APIs (logistics partners, store systems, etc.)
In a real production system, these would connect to actual external services.
"""
import json
from crewai.tools import tool
from pydantic import BaseModel, Field

# ============================================================================
# TOOL 1: BOOK SHIPMENT - For shipping orders to customer addresses
# ============================================================================

class ShipmentInput(BaseModel):
    """Schema for booking a shipment - defines what info we need"""
    order_id: str = Field(description="The unique order ID - like 'ORD-12345'")
    address: str = Field(description="Full customer shipping address - where to deliver")
    items: list = Field(description="List of items to ship - each item has SKU and quantity")


def book_shipment_func(order_id: str, address: str, items: list) -> str:
    """
    Book a shipment with our logistics partner 📦
    
    This function simulates calling a real shipping API (like FedEx, UPS, etc.)
    to create a shipment. In production, this would make actual API calls.
    For now, it generates a tracking number and estimated delivery date.
    
    Args:
        order_id: The unique identifier for this order
        address: Where to ship the package (full customer address)
        items: List of items being shipped (each with SKU and quantity)
    
    Returns:
        A JSON string with shipment details including:
        - Status (SUCCESS)
        - Type (ship-to-home)
        - Tracking number (for tracking the package)
        - Estimated delivery date
    
    Example:
        >>> result = book_shipment_func(
        ...     "ORD-12345",
        ...     "123 Main St, City, State 12345",
        ...     [{"sku": "SHIRT-001", "qty": 2}]
        ... )
        >>> print(result)  # Shows tracking number and delivery date
    """
    print(f"\n📦 TOOL CALLED: book_shipment")
    print(f"   Order ID: {order_id}")
    print(f"   Delivery Address: {address}")
    print(f"   Items: {len(items)} item(s)")
    
    # Generate a tracking number (in real system, this comes from the logistics partner)
    # We create a simple tracking number based on the order ID
    tracking_number = f"ABC{str(abs(hash(order_id)))[-6:]}"
    
    # Return shipment confirmation
    return json.dumps({
        "status": "SUCCESS",
        "type": "ship-to-home",
        "tracking_number": tracking_number,
        "estimated_delivery": "2025-10-22"  # Example date
    })


# Register the tool with CrewAI so the agent can use it
book_shipment = tool(book_shipment_func)

# ============================================================================
# TOOL 2: RESERVE IN-STORE - For holding items at stores for pickup
# ============================================================================

class ReservationInput(BaseModel):
    """Schema for reserving items at a store - what info we need"""
    order_id: str = Field(description="The unique order ID - like 'ORD-12346'")
    store_id: str = Field(description="Which store location - like 'S-102-MUMBAI'")
    items: list = Field(description="List of items to reserve - each with SKU and quantity")


def reserve_in_store_func(order_id: str, store_id: str, items: list) -> str:
    """
    Reserve items at a store for customer pickup 🏪
    
    This function simulates calling a real store reservation system to hold
    items at a specific store location. In production, this would connect to
    the actual store's inventory management system.
    
    It generates a pickup code that the customer will use to claim their order,
    and sets an expiry date for how long the items will be held.
    
    Args:
        order_id: The unique identifier for this order
        store_id: Which store location to reserve at (e.g., 'S-102-MUMBAI')
        items: List of items to reserve (each with SKU and quantity)
    
    Returns:
        A JSON string with reservation details including:
        - Status (SUCCESS)
        - Type (reserve-in-store)
        - Store ID (where to pick up)
        - Pickup code (customer uses this to claim order)
        - Hold expiry (when reservation expires)
    
    Example:
        >>> result = reserve_in_store_func(
        ...     "ORD-12346",
        ...     "S-102-MUMBAI",
        ...     [{"sku": "DRESS-001", "qty": 1}]
        ... )
        >>> print(result)  # Shows pickup code and store details
    """
    print(f"\n🏪 TOOL CALLED: reserve_in_store")
    print(f"   Order ID: {order_id}")
    print(f"   Store: {store_id}")
    print(f"   Items: {len(items)} item(s) being reserved")
    
    # Generate a pickup code (in real system, this comes from the store system)
    # Format: Last 2 chars of store ID + hash of order ID
    pickup_code = f"{store_id[-2:]}-{str(abs(hash(order_id)))[-4:]}"
    
    # Return reservation confirmation
    return json.dumps({
        "status": "SUCCESS",
        "type": "reserve-in-store",
        "store_id": store_id,
        "pickup_code": pickup_code,
        "hold_expires": "2025-10-19T18:00:00"  # Example expiry (3 days from now)
    })


# Register the tool with CrewAI
reserve_in_store = tool(reserve_in_store_func)

# ============================================================================
# TOOL 3: NOTIFY STAFF - For alerting warehouse/store staff about orders
# ============================================================================

class NotificationInput(BaseModel):
    """Schema for sending staff notifications - defines what we need"""
    queue: str = Field(
        description=(
            "Which staff queue to notify - examples:\n"
            "  - 'warehouse_1' for warehouse staff\n"
            "  - 'store_102_pickup' for store pickup staff\n"
            "  - 'store_205_pickup' for a different store"
        )
    )
    message: str = Field(
        description=(
            "The notification message for staff - should include:\n"
            "  - Order details\n"
            "  - What needs to be done\n"
            "  - Any special instructions"
        )
    )


def notify_staff_func(queue: str, message: str) -> str:
    """
    Send a notification to staff so they know about a new order 📢
    
    This function simulates sending notifications to staff queues (like
    warehouse staff or store staff). In production, this would integrate
    with your notification system (email, Slack, internal messaging, etc.).
    
    When an order is booked or reserved, staff need to know so they can:
    - Prepare shipments (warehouse staff)
    - Set aside items for pickup (store staff)
    - Process the order correctly
    
    Args:
        queue: Which staff queue to notify
               Examples: 'warehouse_1', 'store_102_pickup', 'store_205_pickup'
        message: What to tell the staff
                 Should include order details and what they need to do
    
    Returns:
        A JSON confirmation that the notification was sent
    
    Example:
        >>> result = notify_staff_func(
        ...     "warehouse_1",
        ...     "New shipment for ORD-12345: 2 items to ship to customer C-456"
        ... )
        >>> print(result)  # Confirms notification was sent
    """
    print(f"\n📢 TOOL CALLED: notify_staff")
    print(f"   Queue: {queue}")
    print(f"   Message: {message}")
    
    # In a real system, this would send actual notifications
    # For now, we just confirm it was "sent"
    return json.dumps({
        "status": "NOTIFIED",
        "queue": queue,
        "note": "Staff have been alerted about the order"
    })


# Register the tool with CrewAI
notify_staff = tool(notify_staff_func)