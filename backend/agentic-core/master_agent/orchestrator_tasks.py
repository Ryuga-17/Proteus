"""
Orchestrator Tasks - Pre-built Tasks Ready to Use! 🎬

These are example tasks that show off what our orchestrator can do. You can
run these directly to see how different scenarios work, or use them as
inspiration for creating your own custom tasks.

Think of these as demo scripts that show:
- How inventory management works
- How orders flow through the system
- How payments are processed
- How customer support helps
- etc.

Feel free to customize these or create your own using the create_custom_task() function!
"""
from crewai import Task
from orchestrator_agent import Orchestrator

# ============================================================================
# EXAMPLE TASKS - These demonstrate various capabilities
# ============================================================================

# Task 1: Inventory Management - Keeping track of what's in stock
task_inventory_management = Task(
    description=(
        "A business request has come in: 'Run our nightly inventory optimization check. "
        "I need you to check the sales velocity (how fast items are selling) for sku_123 "
        "and sku_456. Then check the current stock levels for both SKUs at all our locations. "
        "\n\n"
        "If sku_123 has low stock (less than 10 units) at store_main_street, transfer "
        "some from godown_central where we have plenty. "
        "\n\n"
        "Also, if sku_123 is in high demand (sales velocity greater than 10), we should "
        "order 100 more units from our supplier to restock.'"
    ),
    expected_output=(
        "A comprehensive inventory report that includes:\n"
        "  📊 Sales velocity analysis - how fast each SKU is selling\n"
        "  📦 Current stock levels - what we have and where\n"
        "  🔄 Transfer confirmations - if any items were moved between locations\n"
        "  📝 Purchase order confirmations - if we ordered more from suppliers\n"
        "\n"
        "Everything should be clear and actionable so the business knows exactly "
        "what happened and what's in stock!"
    ),
    agent=Orchestrator
)

# Task 2: Full Order Fulfillment - Getting orders to customers
task_order_fulfillment = Task(
    description=(
        "Great news! A customer just placed an order and we need to get it to them. "
        "Here are the details:\n"
        "  📋 Order ID: ORD-78901\n"
        "  👤 Customer: C-456\n"
        "  🛍️  Items:\n"
        "     - 2x RED-SHIRT-SML (Red shirt, size small)\n"
        "     - 1x BLUE-JEANS-32 (Blue jeans, size 32)\n"
        "  🚚 Fulfillment type: ship-to-home (we're shipping it to them)\n"
        "  📍 Delivery address: 123 Green St, Bengaluru, KA 560001\n"
        "\n"
        "Please handle this order from start to finish:\n"
        "  1. First, check if we have all the items in stock\n"
        "  2. Then process the fulfillment (book the shipment)\n"
        "  3. Finally, confirm everything is set up and ready to go"
    ),
    expected_output=(
        "A complete order confirmation that tells the customer:\n"
        "  ✅ Inventory status - do we have everything they ordered?\n"
        "  ✅ Fulfillment booking - shipment is confirmed and booked\n"
        "  ✅ Tracking information - tracking number and delivery estimate\n"
        "  ✅ Staff notifications - warehouse staff have been notified\n"
        "\n"
        "Everything should be clear so the customer knows their order is being handled!"
    ),
    agent=Orchestrator
)

# Task 3: Payment Processing - Handling customer payments
task_payment_processing = Task(
    description=(
        "A customer 'cust-789' is ready to checkout! Their order total comes to $150.00, "
        "and they want to pay using their saved credit card 'card-4567'. "
        "\n\n"
        "Please process this payment transaction and let them know if it was successful. "
        "If there are any issues (like declined card or insufficient funds), "
        "make sure to explain what happened clearly."
    ),
    expected_output=(
        "Payment processing results showing:\n"
        "  ✅ Payment status (success or failed)\n"
        "  🆔 Transaction ID (if successful)\n"
        "  💬 Clear error messages (if something went wrong)\n"
        "  📋 Any other relevant details the customer needs to know"
    ),
    agent=Orchestrator
)

# Task 4: Customer Support - Helping customers after purchase
task_customer_support = Task(
    description=(
        "A customer just reached out asking: 'Where is my order? My order ID is ORD12345.' "
        "\n\n"
        "They're probably anxious to know when their package will arrive! Please help them "
        "track their order and give them helpful, real-time shipping updates. Be friendly "
        "and empathetic - we want to make sure they feel taken care of."
    ),
    expected_output=(
        "A warm, helpful response that includes:\n"
        "  📦 Current order status - where things stand right now\n"
        "  🚚 Shipping carrier - which company is delivering\n"
        "  🔢 Tracking number - so they can track it themselves too\n"
        "  📍 Real-time location - where the package currently is\n"
        "  📅 Estimated delivery - when they can expect it\n"
        "  💬 Next steps - anything else they need to know\n"
        "\n"
        "Make it friendly and reassuring - good customer service matters!"
    ),
    agent=Orchestrator
)

# Task 5: Complex Checkout - Pricing, Loyalty, Payment, and Fulfillment
task_checkout_with_loyalty = Task(
    description=(
        "A customer 'c123' is finishing up their shopping! They have these items in their cart: "
        "prod-a, prod-b, and prod-c. They're also smart shoppers - they have a coupon code "
        "'SAVE20' and want to use 500 of their loyalty points to save even more money. "
        "\n\n"
        "Please handle this complete checkout process:\n"
        "  1. Calculate the pricing - apply the coupon and loyalty points to see the final price\n"
        "  2. Process the payment - handle the transaction (might need to deduct those loyalty points)\n"
        "  3. If payment succeeds, initiate fulfillment - get their order ready to ship\n"
        "\n"
        "Return a complete checkout summary so they know exactly what happened and what they paid."
    ),
    expected_output=(
        "A complete checkout summary that shows:\n"
        "  💰 Original price - what everything costs before discounts\n"
        "  🎁 Applied discounts - coupon savings and loyalty points used\n"
        "  💵 Final price - what they actually paid (after all discounts)\n"
        "  ✅ Payment confirmation - transaction was successful\n"
        "  📋 Order confirmation number - their reference for tracking\n"
        "\n"
        "Everything should be clear so they know exactly what they got and how much they saved!"
    ),
    agent=Orchestrator
)

# Task 6: Returns & Exchanges - Making things right when problems happen
task_return_exchange = Task(
    description=(
        "Oh no! A customer just reached out saying: 'My item from order ORD56789 arrived damaged!' "
        "The item that was damaged is a TSHIRT-BLU-M (blue t-shirt, size medium). "
        "They'd like to get a replacement if possible. "
        "\n\n"
        "Please handle this situation with care:\n"
        "  1. First, verify the order details - make sure everything matches up\n"
        "  2. Check if we have a replacement in stock - can we exchange it?\n"
        "  3. Process the exchange or refund - whatever works best for them\n"
        "  4. Provide a return label and clear instructions - make it easy for them\n"
        "\n"
        "Be empathetic - nobody likes getting damaged items. Make sure they feel taken care of!"
    ),
    expected_output=(
        "A helpful response that includes:\n"
        "  ✅ Order verification - confirming we found their order\n"
        "  🔄 Exchange/refund confirmation - what we're doing to fix it\n"
        "  📦 Return label URL - easy way for them to send the damaged item back\n"
        "  📝 Next steps - what happens next and when they'll receive their replacement/refund\n"
        "\n"
        "Make it clear, helpful, and reassuring - we want to turn this negative experience "
        "into a positive one!"
    ),
    agent=Orchestrator
)

# ============================================================================
# CREATE YOUR OWN TASKS - Make custom tasks for anything you need!
# ============================================================================

def create_custom_task(customer_request: str, expected_output: str = None) -> Task:
    """
    Create a custom task for the orchestrator - your way! 🎨
    
    This function lets you create a task for any request you can think of.
    Just describe what you need, and optionally specify what kind of response
    you'd like. The orchestrator will figure out the best way to handle it!
    
    Args:
        customer_request: What you need help with - describe it in plain English!
                         Be as detailed as you want - more context helps the
                         orchestrator route it to the right agents.
        
        expected_output: What you'd like to receive (optional)
                        If you don't specify, we'll give you a helpful,
                        comprehensive response that addresses the request.
    
    Returns:
        A Task object ready to be run through the orchestrator
    
    Example:
        >>> my_task = create_custom_task(
        ...     "Check if we have red shirts size small at store downtown, "
        ...     "and if yes, reserve one for customer C-123",
        ...     "A confirmation with reservation details or stock status"
        ... )
        >>> result = run_orchestrator(my_task, "Reserve Shirt")
    """
    # If they didn't specify what output they want, we'll give them something helpful
    if expected_output is None:
        expected_output = (
            "A clear, comprehensive response that fully addresses the request. "
            "Include all relevant details, confirmations, or information needed "
            "to help the customer or business understand what happened."
        )
    
    # Create and return the task - easy!
    return Task(
        description=customer_request,
        expected_output=expected_output,
        agent=Orchestrator  # Our orchestrator will handle it!
    )

