# tasks.py
from crewai import Task
from agents import fulfillment_agent

# --- Task 1: Ship-to-Home Scenario ---
ship_to_home_input = """
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
    description=f"Process the following fulfillment request. First, use the correct tool to book the fulfillment. Second, notify the appropriate staff. {ship_to_home_input}",
    expected_output="A final JSON string confirming the shipment, including the tracking number, and confirming that the warehouse staff was notified.",
    agent=fulfillment_agent
)

# --- Task 2: Reserve In-Store Scenario ---
reserve_in_store_input = """
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
    description=f"Process the following fulfillment request. First, use the correct tool to book the fulfillment. Second, notify the appropriate staff. {reserve_in_store_input}",
    expected_output="A final JSON string confirming the in-store reservation, including the pickup code, and confirming that the store staff was notified.",
    agent=fulfillment_agent
)