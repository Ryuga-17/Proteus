# tasks.py
from crewai import Task
from agents import post_purchase_agent

# Task 1: Order Tracking ("Where is my order?")
task_track_order = Task(
    description=(
        "A customer is asking: 'Where is my order?' "
        "Their order ID is 'ORD12345'. "
        "1. Find the order status using the Order Management Tool. "
        "2. If shipped, use the tracking number and carrier to get the *live* tracking details from the Carrier API Tool. "
        "3. Synthesize all this information into a single, helpful, and empathetic response for the customer. "
        "4. Conclude by asking if there is anything else you can help with."
    ),
    expected_output=(
        "A friendly, empathetic response to the customer with their order's "
        "shipping status, carrier, and real-time tracking location and updates. "
        "Example: 'I'm happy to help with that! Your order ORD12345 is...'"
    ),
    agent=post_purchase_agent
)

# Task 2: Damaged Item Return/Exchange
task_damaged_item = Task(
    description=(
        "A customer is upset: 'My item from order ORD56789 arrived damaged!' "
        "The item SKU is 'TSHIRT-BLU-M'. They want a replacement. "
        "1. Start with an empathetic apology. "
        "2. Use the Order Management Tool to confirm the order and check its return eligibility. "
        "3. Use the Inventory Tool to check stock for SKU 'TSHIRT-BLU-M'. "
        "4. **IF IN STOCK**: Use the Returns Management Tool to process an 'exchange'. "
        "   Tell the customer you've processed the exchange, a new order is created, "
        "   and provide the return label URL for the damaged item. "
        "5. **IF OUT OF STOCK**: Apologize again. Offer a full refund. "
        "   If they accept, use the Returns Management Tool to process a 'refund'. "
        "   Tell the customer you've processed the refund, provide the return label URL, "
        "   and explain when they'll get their money back. "
        "6. Synthesize all steps into one clear, reassuring response."
    ),
    expected_output=(
        "A comprehensive, empathetic response detailing the full resolution. "
        "This must include an apology and *either* confirmation of the "
        "replacement order and a return label URL *or* confirmation of a full "
        "refund and a return label URL."
    ),
    agent=post_purchase_agent
)

# Task 3: Solicit Feedback
task_get_feedback = Task(
    description=(
        "The customer (CustomerID 'CUST777', associated with order 'ORD12345') "
        "has just had their issue resolved and said 'thank you'. "
        "1. Respond politely. "
        "2. Use the Customer Feedback Tool to generate a survey link for 'CUST777'. "
        "3. Ask the customer if they would mind taking a moment to "
        "   rate their experience and provide the link."
    ),
    expected_output=(
        "A polite and friendly message that thanks the customer and "
        "provides the generated feedback survey link."
    ),
    agent=post_purchase_agent
)