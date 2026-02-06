# FILENAME: tools.py

from langchain_community.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any

# Import the mock data from our DB file
from mock_db import PRODUCT_CATALOG, CUSTOMER_PROFILES, PROMOTIONS_DB

class PricingToolSchema(BaseModel):
    """Input schema for PricingAndOffersTool."""
    customer_id: str = Field(..., description="The unique ID of the customer.")
    cart_items: List[str] = Field(..., description="List of product SKUs in the cart.")
    coupon_code: str = Field(None, description="An optional coupon code provided by the customer.")

class PricingAndOffersTool(BaseTool):
    """
    A specialized tool to query the pricing, customer, and promotion databases.
    It calculates the original price, validates all applicable offers,
    and returns a final, fully calculated price breakdown.
    """
    name: str = "Pricing and Offers Calculation Tool"
    description: str = (
        "Use this tool to get the final price for a customer's cart. "
        "It takes a customer_id, a list of cart_items (SKUs), and an optional coupon_code. "
        "It automatically checks loyalty status and applies all valid promotions."
    )
    args_schema: Type[BaseModel] = PricingToolSchema

    def _run(self, customer_id: str, cart_items: List[str], coupon_code: str = None) -> Dict[str, Any]:
        """The logic for the tool."""
        
        # 1. Get customer and cart details
        customer = CUSTOMER_PROFILES.get(customer_id)
        if not customer:
            return {"error": "Customer not found."}
        
        cart_details = [PRODUCT_CATALOG.get(sku) for sku in cart_items if sku in PRODUCT_CATALOG]
        if not cart_details:
            return {"error": "No valid items in cart."}

        # 2. Calculate Original Price
        original_price = sum(item['price'] for item in cart_details)
        final_price = original_price
        discounts_applied = []

        # 3. Apply Loyalty Discount [cite: 290]
        loyalty_rule = PROMOTIONS_DB["LOYALTY_RULES"].get(customer["loyalty_tier"])
        if loyalty_rule and loyalty_rule["type"] == "percent_off":
            discount_amount = final_price * loyalty_rule["value"]
            final_price -= discount_amount
            discounts_applied.append({
                "name": loyalty_rule["name"],
                "amount": round(discount_amount, 2)
            })

        # 4. Apply Coupon Code [cite: 290]
        coupon = PROMOTIONS_DB["COUPONS"].get(coupon_code)
        if coupon:
            if final_price >= coupon["min_spend"]:
                if coupon["type"] == "dollar_off":
                    discount_amount = coupon["value"]
                    final_price -= discount_amount
                    discounts_applied.append({
                        "name": f"Coupon ({coupon_code})",
                        "amount": round(discount_amount, 2)
                    })
                elif coupon["type"] == "percent_off":
                    discount_amount = final_price * coupon["value"]
                    final_price -= discount_amount
                    discounts_applied.append({
                        "name": f"Coupon ({coupon_code})",
                        "amount": round(discount_amount, 2)
                    })
            else:
                discounts_applied.append({
                    "name": f"Coupon ({coupon_code})",
                    "error": f"Minimum spend of ${coupon['min_spend']} not met."
                })
        
        # 5. Compile Final Report
        total_savings = round(original_price - final_price, 2)
        
        return {
            "customer_id": customer_id,
            "original_price": round(original_price, 2),
            "final_price": round(final_price, 2),
            "total_savings": total_savings,
            "discounts_applied": discounts_applied,
            "items_processed": [item['name'] for item in cart_details]
        }

# Instantiate a single instance of the tool for the agents to use
pricing_tool = PricingAndOffersTool()