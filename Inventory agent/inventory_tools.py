import time
from crewai_tools import BaseTool



class MockDB:
    """Simulates a persistent database for inventory and product data."""
    def __init__(self):
        self.inventory = {
            "store_main_street": {"sku_123": 5, "sku_456": 25},
            "store_westside_mall": {"sku_123": 8, "sku_456": 30},
            "godown_central": {"sku_123": 500, "sku_456": 300},
        }
        self.sales_history = {
            "sku_123": [10, 12, 15, 14, 20],  # "In-demand"
            "sku_456": [5, 6, 5, 7, 6],    
        }
        self.product_margins = {
            "sku_123": 15.00, 
            "sku_456": 25.00,
        }

    def get_stock(self, sku: str) -> dict:
        print(f"TOOL_LOG: Reading stock for {sku} from all locations.")
        results = {}
        for location, stock in self.inventory.items():
            if sku in stock:
                results[location] = stock[sku]
        return results

    def get_sales_velocity(self, sku: str) -> float:
        print(f"TOOL_LOG: Calculating sales velocity for {sku}.")
        history = self.sales_history.get(sku, [])
        return sum(history) / len(history) if history else 0

    def get_margin(self, sku: str) -> float:
        print(f"TOOL_LOG: Fetching margin for {sku}.")
        return self.product_margins.get(sku, 0.0)

    def update_stock(self, location_id: str, sku: str, quantity_change: int) -> bool:
        """Internal function to update stock. Returns True on success."""
        if location_id in self.inventory and sku in self.inventory[location_id]:
            if self.inventory[location_id][sku] + quantity_change < 0:
                print(f"TOOL_LOG (ERROR): Not enough stock of {sku} at {location_id}.")
                return False
            self.inventory[location_id][sku] += quantity_change
            print(f"TOOL_LOG (SUCCESS): Stock for {sku} at {location_id} is now {self.inventory[location_id][sku]}")
            return True
        print(f"TOOL_LOG (ERROR): Invalid location or SKU for stock update.")
        return False

# Initializing a single instance of our mock database
db = MockDB()


class InventoryTools:
    @BaseTool
    def check_stock_tool(sku: str) -> str:
        """
        Checks the stock level for a specific SKU across all locations 
        (godowns and stores).
        """
        stock_data = db.get_stock(sku)
        return f"Stock levels for {sku}: {stock_data}"

    @BaseTool
    def get_sales_velocity_tool(sku: str) -> str:
        """
        Calculates the average daily sales velocity for a specific SKU
        to determine if it's 'in-demand'.
        """
        velocity = db.get_sales_velocity(sku)
        return f"Sales velocity for {sku}: {velocity:.2f} units/day"

    @BaseTool
    def execute_safe_transfer_tool(from_location: str, to_location: str, sku: str, quantity: int) -> str:
        """
        Executes a 'safe' stock transfer between two locations.
        This tool contains the business-critical GUARDRAILS.
        It will fail if the transfer is unsafe or unprofitable.
        """
        print(f"--- Running Safe Transfer Guardrails for {quantity} of {sku} ---")
        
        # GUARDRAIL 1: Financial (Profitability) ---
        # Simulating logistics cost vs. margin
        logistics_cost = 50.0  # Flat $50 fee for any inter-store transfer
        product_margin = db.get_margin(sku) * quantity
        
        if logistics_cost > (product_margin * 0.3):
            rejection_msg = f"REJECTED: Transfer cost (${logistics_cost}) exceeds 30% of margin (${product_margin:.2f}). Flagging for human review."
            print(f"GUARDRAIL_HIT: {rejection_msg}")
            return rejection_msg

        # GUARDRAIL 2: Inventory (Safety Stock) ---
        source_stock = db.inventory.get(from_location, {}).get(sku, 0)
        safety_stock_level = 5  # Minimum 5 units
        
        if (source_stock - quantity) < safety_stock_level:
            rejection_msg = f"REJECTED: Transfer would leave {from_location} with {source_stock - quantity} units, which is below the safety stock level of {safety_stock_level}."
            print(f"GUARDRAIL_HIT: {rejection_msg}")
            return rejection_msg
            
        # GUARDRAIL 3: Fault Tolerance (Execution) ---
        print("GUARDRAILS_PASSED: Executing transfer...")
        # This is a "transaction" - must decrement from source AND increment at destination
        if not db.update_stock(from_location, sku, -quantity):
            return "FAILED: Could not decrement stock from source."
        
        if not db.update_stock(to_location, sku, quantity):
            # Rolling back to the first transaction
            db.update_stock(from_location, sku, quantity)
            return "FAILED: Could not increment stock at destination. Rolling back."

        return f"SUCCESS: Transferred {quantity} units of {sku} from {from_location} to {to_location}."

    @BaseTool
    def order_from_supplier_tool(sku: str, quantity: int) -> str:
        """
        Places a replenishment order for a given SKU with an external supplier.
        """
        print(f"TOOL_LOG: Placing order for {quantity} of {sku} from supplier.")
        # In a real app, this would trigger a procurement API
        time.sleep(1) 
        return f"SUCCESS: Purchase Order PO-10{int(time.time())} placed for {quantity} units of {sku}."