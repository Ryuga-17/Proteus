# tools.py
import json
from crewai.tools import tool
from pydantic import BaseModel, Field

# --- Tool 1: Book Shipment ---

class ShipmentInput(BaseModel):
    """Input schema for booking a shipment."""
    order_id: str = Field(description="The unique ID of the order.")
    address: str = Field(description="The full customer shipping address.")
    items: list = Field(description="List of SKUs and quantities to ship.")

def book_shipment_func(order_id: str, address: str, items: list) -> str:
    """
    Books a shipment with the logistics partner.
    Returns a JSON string with the tracking number and delivery estimate.
    """
    print(f"\n--- TOOL CALLED: book_shipment---")
    print(f"   Order: {order_id}, Address: {address}")
    tracking_number = f"ABC{str(abs(hash(order_id)))[-6:]}"
    return json.dumps({
        "status": "SUCCESS",
        "type": "ship-to-home",
        "tracking_number": tracking_number,
        "estimated_delivery": "2025-10-22"
    })

book_shipment = tool(book_shipment_func)

# --- Tool 2: Reserve In-Store ---

class ReservationInput(BaseModel):
    """Input schema for reserving items in-store."""
    order_id: str = Field(description="The unique ID of the order.")
    store_id: str = Field(description="The ID of the store for pickup.")
    items: list = Field(description="List of SKUs and quantities to reserve.")

def reserve_in_store_func(order_id: str, store_id: str, items: list) -> str:
    """
    Reserves items for in-store pickup.
    Returns a JSON string with the pickup code and hold expiry.
    """
    print(f"\n---TOOL CALLED: reserve_in_store---")
    print(f"   Order: {order_id}, Store: {store_id}")
    pickup_code = f"{store_id[-2:]}-{str(abs(hash(order_id)))[-4:]}"
    return json.dumps({
        "status": "SUCCESS",
        "type": "reserve-in-store",
        "store_id": store_id,
        "pickup_code": pickup_code,
        "hold_expires": "2025-10-19T18:00:00"
    })

reserve_in_store = tool(reserve_in_store_func)

# --- Tool 3: Notify Staff ---

class NotificationInput(BaseModel):
    """Input schema for sending internal staff notifications."""
    queue: str = Field(description="The destination queue (e.g., 'warehouse_1' or 'store_102_pickup').")
    message: str = Field(description="The notification message for the staff.")

def notify_staff_func(queue: str, message: str) -> str:
    """
    Sends a notification to an internal staff queue (e.g., warehouse or store).
    """
    print(f"\n---TOOL CALLED: notify_staff---")
    print(f"   Queue: {queue}")
    print(f"   Message: {message}")
    return json.dumps({"status": "NOTIFIED", "queue": queue})

notify_staff = tool(notify_staff_func)