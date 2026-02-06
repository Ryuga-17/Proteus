"""
Payment Agent Tasks - Testing Different Payment Scenarios! 💳

These tasks demonstrate how the payment crew handles different payment scenarios:
1. Payment failures - When cards are declined or have insufficient funds
2. Kiosk-to-mobile handoffs - When customers want to pay on their phone instead
3. Loyalty point payments - When customers use their points to pay

Each scenario shows how the Sales Agent orchestrates the payment process and
works with the Payment and Loyalty agents to get things done.
"""
from crewai import Task

# Import the sales agent who will orchestrate these payment scenarios
from agents import sales_agent

print("\n📋 Defining Payment Tasks...")

# ============================================================================
# SCENARIO 1: GRACEFUL FAILURE HANDLING - When payments don't go through
# ============================================================================

task_fail_scenario = Task(
    description=(
        "A customer 'cust-789' is checking out with an order total of $150.00. "
        "They've chosen to pay using their saved credit card (number 'fail-1234'). "
        "Unfortunately, this card is set up to simulate a payment failure.\n\n"
        
        "Here's what you (the Sales Agent) need to do:\n"
        "  1. Delegate the payment processing to the Payment Agent\n"
        "     (Pass them the customer ID, amount, payment method, and card details)\n"
        "  2. The Payment Agent will use their 'process_standard_payment' tool\n"
        "     (This will simulate the payment attempt and return a failure status)\n"
        "  3. Receive the JSON status from the Payment Agent\n"
        "  4. Return ONLY the JSON string from the Payment Agent\n\n"
        
        "This scenario tests that we handle payment failures gracefully - "
        "the customer should get a clear explanation of what went wrong!"
    ),
    expected_output=(
        "A JSON string from the Payment Agent showing:\n"
        "  ❌ Status: 'failed'\n"
        "  💬 Error message explaining what went wrong (e.g., 'Insufficient funds')\n"
        "  📋 Transaction ID: null (since payment didn't go through)\n\n"
        "This helps us ensure customers always get clear feedback when payments fail."
    ),
    agent=sales_agent  # Sales Agent orchestrates the payment flow
)


# ============================================================================
# SCENARIO 2: KIOSK-TO-MOBILE HANDOFF - Moving payment to customer's phone
# ============================================================================

task_kiosk_scenario = Task(
    description=(
        "A customer 'cust-303' is shopping at an in-store kiosk (session ID: 'kiosk-A9'). "
        "Their order total is $85.20. They've decided they'd rather pay on their mobile "
        "phone instead of at the kiosk.\n\n"
        
        "Here's what you (the Sales Agent) need to orchestrate:\n"
        "  1. Delegate this task to the Payment Agent\n"
        "     (Tell them about the kiosk session and that customer wants mobile payment)\n"
        "  2. The Payment Agent will use their 'generate_kiosk_to_mobile_handoff' tool\n"
        "     (This creates a payment URL/QR code that the customer can scan)\n"
        "  3. Receive the JSON status from the Payment Agent with the handoff details\n"
        "  4. Return ONLY the JSON string containing the 'payment_url_for_qr_code'\n\n"
        
        "This scenario is great for in-store experiences where customers want to "
        "use their phone's payment app (like Apple Pay, Google Pay, etc.)!"
    ),
    expected_output=(
        "A JSON string from the Payment Agent containing:\n"
        "  ✅ Status: 'pending' or 'initiated'\n"
        "  📱 payment_url_for_qr_code: The URL/QR code data the customer scans\n"
        "  🔗 Additional handoff details if needed\n\n"
        "The kiosk can display this as a QR code that the customer scans with their phone!"
    ),
    agent=sales_agent
)


# ============================================================================
# SCENARIO 3: PAY WITH POINTS - Using loyalty points for payment
# ============================================================================

task_points_scenario = Task(
    description=(
        "A customer 'cust-555' is finishing their checkout! Their order total is $50.00. "
        "They have 1500 loyalty points available and have chosen to 'Pay with Points'. "
        "This purchase will require 500 points (let's say 100 points = $10, so 500 points = $50).\n\n"
        
        "Here's the multi-agent workflow you (the Sales Agent) need to orchestrate:\n"
        "  1. Delegate the payment task to the Payment Agent\n"
        "     (Tell them it's a loyalty point payment)\n"
        "  2. The Payment Agent will realize this needs loyalty point deduction\n"
        "     and will delegate to the Loyalty Agent\n"
        "  3. The Loyalty Agent will use their 'debit_loyalty_points' tool\n"
        "     (This deducts 500 points from the customer's account)\n"
        "  4. The status flows back: Loyalty Agent → Payment Agent → Sales Agent\n"
        "  5. Return ONLY the final JSON string from the Loyalty Agent\n\n"
        
        "This scenario shows how multiple agents work together - Payment Agent "
        "recognizes it needs loyalty processing and coordinates with Loyalty Agent!"
    ),
    expected_output=(
        "A JSON string from the Loyalty Agent showing:\n"
        "  ✅ Status: 'success'\n"
        "  ⭐ points_debited: 500\n"
        "  💰 Equivalent value deducted from order\n"
        "  📋 Updated point balance\n\n"
        "This confirms the points were successfully used and the payment is complete!"
    ),
    agent=sales_agent
)