"""
Fulfillment Tasks - Getting Orders Where They Need to Go! 📦

These are the tasks our fulfillment agent handles. Each task represents a
different way customers want to receive their orders:
- Ship-to-Home: Delivered right to their door
- Reserve In-Store: Held at a store for pickup

The fulfillment agent processes these tasks by booking shipments/reservations
and notifying the right staff to prepare the orders.
"""
from crewai import Task
from agents import fulfillment_agent

# ============================================================================
# TASK 1: SHIP-TO-HOME - Delivering orders to customer addresses
# ============================================================================

# Order details for the ship-to-home scenario
ship_to_home_order_data = """
{
  "task": "fulfill_order",
  "order_id": "ORD-12345",
  "type": "ship-to-home",
  "customer": "C-456",
  "address": "123 Green St, Bengaluru, KA 560001",
  "items": [
    {"sku": "RED-SHIRT-SML", "qty": 1},
    {"sku": "BLUE-JEANS-32", "qty": 1}
  ]
}
"""

task_ship_to_home = Task(
    description=(
        "Process this fulfillment request for a customer who wants their order "
        "shipped directly to their home!\n\n"
        f"{ship_to_home_order_data}\n\n"
        "Here's what you need to do:\n"
        "  1. First, identify that this is a 'ship-to-home' order\n"
        "  2. Use the book_shipment tool to create the shipment with our logistics partner\n"
        "     (This will generate a tracking number and delivery estimate)\n"
        "  3. Use the notify_staff tool to alert the warehouse staff\n"
        "     (Send a message to 'warehouse_1' queue so they know to prepare the order)\n"
        "  4. Return a final JSON status report with all the details"
    ),
    expected_output=(
        "A final JSON status report that includes:\n"
        "  ✅ Shipment confirmation (status: SUCCESS)\n"
        "  📦 Tracking number (so customer can track their package)\n"
        "  📅 Estimated delivery date\n"
        "  ✅ Confirmation that warehouse staff were notified\n"
        "\n"
        "Make sure everything is clear and complete!"
    ),
    agent=fulfillment_agent
)


# ============================================================================
# TASK 2: RESERVE IN-STORE - Holding items at stores for pickup
# ============================================================================

# Order details for the in-store reservation scenario
reserve_in_store_order_data = """
{
  "task": "fulfill_order",
  "order_id": "ORD-12346",
  "type": "reserve-in-store",
  "customer": "C-789",
  "store_id": "S-102-MUMBAI",
  "items": [
    {"sku": "BLK-DRESS-MED", "qty": 1}
  ]
}
"""

task_reserve_in_store = Task(
    description=(
        "Process this fulfillment request for a customer who wants to pick up "
        "their order at a store location!\n\n"
        f"{reserve_in_store_order_data}\n\n"
        "Here's what you need to do:\n"
        "  1. First, identify that this is a 'reserve-in-store' order\n"
        "  2. Use the reserve_in_store tool to reserve the items at the specified store\n"
        "     (This will generate a pickup code and hold expiry date)\n"
        "  3. Use the notify_staff tool to alert the store staff\n"
        "     (Send a message to the store's pickup queue so they know to prepare the order)\n"
        "  4. Return a final JSON status report with all the details"
    ),
    expected_output=(
        "A final JSON status report that includes:\n"
        "  ✅ Reservation confirmation (status: SUCCESS)\n"
        "  🏪 Store ID where items are reserved\n"
        "  🔢 Pickup code (customer uses this to pick up their order)\n"
        "  ⏰ Hold expiry date (when the reservation expires)\n"
        "  ✅ Confirmation that store staff were notified\n"
        "\n"
        "Everything the customer needs to know to pick up their order!"
    ),
    agent=fulfillment_agent
)