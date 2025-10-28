# FILENAME: tasks.py

from crewai import Task
from agents import sales_agent # We assign the task to the sales_agent

sales_task = Task(
    description=(
        "Finalize the checkout for customer 'c123'. "
        "The customer's cart contains the following SKUs: ['prod-a', 'prod-b', 'prod-c']. "
        "The customer has also provided a coupon code: 'SAVE20'. "
        
        "\nYour process is: "
        "1. Delegate the price calculation to the 'Specialized Financial Assistant'. "
        "You must provide it with the customer_id, cart_items, and coupon_code. "
        "2. Wait for its JSON response. "
        "3. Use the data from the JSON (original_price, final_price, total_savings, "
        "and discounts_applied) to create a friendly, customer-facing summary."
    ),
    expected_output=(
        "A final, customer-facing summary message. "
        "Example: 'Great! Here's your order summary, Alex: "
        "- Classic T-Shirt: $25.00..."
        "Total: $190.00. We applied [Discount Name] ($10.00) "
        "and [Coupon Name] ($20.00). Your final price is $160.00. "
        "You saved $30.00 today!'"
    ),
    agent=sales_agent
)