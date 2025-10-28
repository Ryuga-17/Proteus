# tools.py
import json
from crewai.tools import tool
from pydantic import BaseModel, Field

# --- Input Schemas for Tools ---

class PaymentInput(BaseModel):
    """Input schema for processing a standard payment."""
    customer_id: str = Field(description="The customer's unique ID.")
    amount: float = Field(description="The total amount to be charged.")
    payment_method: str = Field(description="The method of payment (e.g., 'credit_card', 'upi').")
    details: dict = Field(description="Payment-specific details, like card number or UPI ID.")

class KioskHandoffInput(BaseModel):
    """Input schema for initiating a kiosk-to-mobile handoff."""
    customer_id: str = Field(description="The customer's unique ID.")
    amount: float = Field(description="The total amount for the transaction.")
    session_id: str = Field(description="The in-store kiosk session ID.")
    
class LoyaltyPaymentInput(BaseModel):
    """Input schema for paying with loyalty points."""
    customer_id: str = Field(description="The customer's unique ID.")
    points_to_debit: int = Field(description="The number of points to use for the purchase.")

# --- Tool Class ---

class PaymentTools:
    
    @tool
    def process_standard_payment(
        customer_id: str, 
        amount: float, 
        payment_method: str, 
        details: dict
    ) -> str:
        """
        Processes a standard payment (e.g., credit card, UPI, gift card).
        Returns a JSON string of the transaction status.
        This tool simulates calling a payment gateway stub.
        """
        print(f"\n[Tool Called: process_standard_payment]")
        print(f"   > Attempting payment for {customer_id} of ${amount} via {payment_method}.")
        
        # Simulate a payment failure
        if details.get("card_number") == "fail-1234":
            print(f"   > SIMULATED FAILURE: Insufficient funds.")
            return json.dumps({
                "status": "failed",
                "transaction_id": None,
                "error_message": "Insufficient funds"
            })
            
        # Simulate success
        transaction_id = f"txn_sandbox_{abs(hash(customer_id + str(amount)))}"
        print(f"   > SIMULATED SUCCESS: Transaction ID: {transaction_id}")
        return json.dumps({
            "status": "success",
            "transaction_id": transaction_id,
            "amount_paid": amount
        })

    @tool
    def generate_kiosk_to_mobile_handoff(
        customer_id: str, 
        amount: float, 
        session_id: str
    ) -> str:
        """
        Generates a secure QR code URL for cross-channel payment handoff.
        This allows a user to start on a kiosk and pay on their mobile.
        """
        print(f"\n[Tool Called: generate_kiosk_to_mobile_handoff]")
        # This simulates generating a unique, single-use token
        token = f"token_kiosk_{abs(hash(session_id + customer_id))}"
        payment_url = f"https://pay.example.com?token={token}"
        print(f"   > Generated secure URL for kiosk session {session_id}: {payment_url}")
        
        # The agent's JSON output includes the URL for the 'Sales Agent' to use
        return json.dumps({
            "status": "handoff_initiated",
            "payment_url_for_qr_code": payment_url,
            "message": "Please scan the QR code on your mobile to complete payment."
        })

    @tool
    def debit_loyalty_points(customer_id: str, points_to_debit: int) -> str:
        """
        Connects to the Loyalty Agent's system to pay using points.
        This tool is called *by* the Payment Agent.
        """
        print(f"\n[Tool Called: debit_loyalty_points]")
        print(f"   > Attempting to debit {points_to_debit} points from {customer_id}.")
        
        # Simulate failure (not enough points)
        if points_to_debit > 1000:
            print(f"   > SIMULATED FAILURE: Insufficient points.")
            return json.dumps({
                "status": "failed",
                "customer_id": customer_id,
                "error_message": "Insufficient loyalty points."
            })
            
        # Simulate success
        print(f"   > SIMULATED SUCCESS: Debited {points_to_debit} points.")
        return json.dumps({
            "status": "success",
            "customer_id": customer_id,
            "points_debited": points_to_debit,
            "remaining_balance": 1000 - points_to_debit
        })