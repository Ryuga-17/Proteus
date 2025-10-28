# tasks.py
from crewai import Task

# Import the agents
from agents import sales_agent

print("\n--- Defining Tasks ---")

# --- SCENARIO 1: GRACEFUL FAILURE HANDLING ---
task_fail_scenario = Task(
    description=(
        "A customer, 'cust-789', is checking out with an order total of $150.00. "
        "They have chosen to pay with their saved credit card, which has number 'fail-1234'. "
        "You (the SalesAgent) must orchestrate this payment."
        "1. Delegate the payment to the 'PaymentAgent'. "
        "2. The 'PaymentAgent' must use its 'process_standard_payment' tool. "
        "3. Receive the final JSON status from the 'PaymentAgent'. "
        "4. Your final output MUST be only the JSON string returned by the PaymentAgent."
    ),
    expected_output="A final JSON string from the PaymentAgent confirming the 'failed' status and error message.",
    agent=sales_agent, # Task is assigned to the orchestrator
)

# --- SCENARIO 2: KIOSK-TO-MOBILE HANDOFF ---
task_kiosk_scenario = Task(
    description=(
        "A customer, 'cust-303', is at an in-store kiosk (session 'kiosk-A9'). "
        "Their order total is $85.20. They want to pay on their mobile. "
        "You (the SalesAgent) must orchestrate this handoff."
        "1. Delegate this task to the 'PaymentAgent'. "
        "2. The 'PaymentAgent' must use its 'generate_kiosk_to_mobile_handoff' tool. "
        "3. Receive the final JSON status from the 'PaymentAgent'. "
        "4. Your final output MUST be only the JSON string containing the 'payment_url_for_qr_code'."
    ),
    expected_output="A final JSON string from the PaymentAgent containing the 'status' and 'payment_url_for_qr_code'.",
    agent=sales_agent,
)

# --- SCENARIO 3: PAY WITH POINTS (Optional to run) ---
task_points_scenario = Task(
    description=(
        "A customer, 'cust-555', is checking out with an order total of $50.00. "
        "They have 1500 points and have chosen to 'Pay with Points'. This will require 500 points. "
        "You (the SalesAgent) must orchestrate this payment."
        "1. Delegate this task to the 'PaymentAgent'. "
        "2. The 'PaymentAgent' must realize this is a loyalty payment and DELEGATE the task to the 'LoyaltyAgent'. "
        "3. The 'LoyaltyAgent' must use its 'debit_loyalty_points' tool. "
        "4. The final JSON status must be passed all the way back to you. "
        "5. Your final output MUST be only the JSON string from the LoyaltyAgent."
    ),
    expected_output="A final JSON string from the LoyaltyAgent confirming the 'success' and 'points_debited'.",
    agent=sales_agent,
)