# tools.py
import datetime
from crewai.tools import BaseTool

# In a real-world scenario, these tools would make API calls (e.g., using 'requests')
# to your backend systems, OMS, inventory, carrier APIs, etc.

class OrderManagementTool(BaseTool):
    name: str = "Order Management System API Tool"
    description: str = "Fetches order details, status, and tracking numbers. Input must be an order_ID string (e.g., 'ORD12345')."

    def _run(self, order_ID: str) -> dict:
        # Mock database of orders
        mock_orders = {
            "ORD12345": {
                "status": "Shipped",
                "tracking_number": "1Z987XYZ",
                "carrier": "UPS",
                "estimated_delivery": (datetime.date.today() + datetime.timedelta(days=2)).isoformat(),
                "items": [{"sku": "SHOE-RED-10", "name": "Red Running Shoes", "quantity": 1}],
                "customer_id": "CUST777"
            },
            "ORD56789": {
                "status": "Delivered",
                "delivered_on": (datetime.date.today() - datetime.timedelta(days=3)).isoformat(),
                "items": [{"sku": "TSHIRT-BLU-M", "name": "Blue Cotton T-Shirt", "quantity": 1}],
                "customer_id": "CUST888",
                "return_eligible_until": (datetime.date.today() + datetime.timedelta(days=27)).isoformat()
            }
        }
        return mock_orders.get(order_ID, {"error": "Order not found"})

class CarrierAPITool(BaseTool):
    name: str = "Carrier Tracking API Tool"
    description: str = "Gets real-time tracking details from a carrier. Input must be a tracking_number string (e.g., '1Z987XYZ')."

    def _run(self, tracking_number: str) -> dict:
        # Mock API response
        if tracking_number == "1Z987XYZ":
            return {
                "tracking_number": "1Z987XYZ",
                "status": "In Transit",
                "last_location": "City Distribution Center",
                "last_update": "2025-10-23T14:30:00Z"
            }
        return {"error": "Tracking number invalid"}

class InventoryTool(BaseTool):
    name: str = "Inventory Check API Tool"
    description: str = "Checks real-time stock for a given SKU. Input must be a SKU string (e.g., 'TSHIRT-BLU-M')."

    def _run(self, sku: str) -> dict:
        # Mock inventory levels
        mock_inventory = {
            "TSHIRT-BLU-M": {"stock_level": 150, "status": "In Stock"},
            "SHOE-RED-10": {"stock_level": 0, "status": "Out of Stock"}
        }
        return mock_inventory.get(sku, {"stock_level": 0, "status": "SKU Not Found"})

class ReturnsManagementTool(BaseTool):
    name: str = "Returns Management API Tool"
    description: str = "Processes returns or exchanges. Input should be a dictionary with 'order_ID', 'sku', 'reason', and 'type' (e.t., 'refund' or 'exchange')."

    def _run(self, order_ID: str, sku: str, reason: str, type: str) -> dict:
        # Mock RMA generation
        if type == "exchange":
            # In a real app, this would also trigger a new $0 order
            new_exchange_order_id = "EXCHG-" + order_ID.split('-')[-1]
            return {
                "status": "Exchange Processed",
                "return_label_url": f"https://api.retailer.com/returns/labels/RMA-{order_ID}.pdf",
                "new_exchange_order_id": new_exchange_order_id,
                "message": f"A new order ({new_exchange_order_id}) for {sku} has been created."
            }
        elif type == "refund":
            return {
                "status": "Refund Initiated",
                "return_label_url": f"https://api.retailer.com/returns/labels/RMA-{order_ID}.pdf",
                "refund_amount": 25.99, # Mock amount
                "message": "Refund will be processed in 3-5 business days after item is received."
            }
        return {"error": "Invalid return request"}

class PaymentTool(BaseTool):
    name: str = "Payment API Tool"
    description: str = "Processes refunds to a customer's original payment method. Input must be a dictionary with 'order_ID' and 'amount'."

    def _run(self, order_ID: str, amount: float) -> dict:
        # Mock refund processing
        return {
            "status": "Refund Processed",
            "transaction_id": f"REF-{order_ID}-{datetime.datetime.now().timestamp()}",
            "amount": amount,
            "message": "Refund will appear on customer's statement in 3-5 business days."
        }

class CustomerFeedbackTool(BaseTool):
    name: str = "Customer Feedback API Tool"
    description: str = "Sends a feedback survey link to a customer. Input must be a customer_id string (e.g., 'CUST777')."

    def _run(self, customer_id: str) -> dict:
        # Mock survey link generation
        survey_link = f"https://api.retailer.com/feedback/survey?cid={customer_id}"
        return {
            "status": "Survey Link Sent",
            "survey_link": survey_link
        }