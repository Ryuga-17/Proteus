"""
Orchestrator Tools - Your Trusty Routing Helpers 🛠️

These tools are like the switchboard operators of our system! They know exactly
which specialist agent to connect you with based on what you need.

Think of it like calling a help desk:
- Need to check stock? → Inventory Agent
- Want to ship something? → Fulfillment Agent  
- Processing a payment? → Payment Agent
- etc.

Each routing function creates a temporary "crew" with the right agents,
runs your request through them, and brings back the results.
"""
import sys
import os
import json
from typing import Dict, Any, Optional

# First, we need to make sure Python can find all our agent modules
# We add each agent's directory to the Python path so we can import them
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, 'Inventory agent'))
sys.path.insert(0, os.path.join(base_dir, 'Fullfillment_agent'))
sys.path.insert(0, os.path.join(base_dir, 'payment_agent'))
sys.path.insert(0, os.path.join(base_dir, 'loyalty and offers agent'))
sys.path.insert(0, os.path.join(base_dir, 'post purchase support agent'))

from crewai.tools import tool


@tool("Route to Inventory Agent")
def route_to_inventory(customer_request: str) -> str:
    """
    Send inventory-related requests to the Inventory Agent 📦
    
    This is your go-to function for anything related to stock levels, transfers
    between locations, or ordering from suppliers. The Inventory Agent knows
    how to check what's in stock, move items between stores/godowns, and
    place orders when supplies are running low.
    
    Args:
        customer_request: What you need help with, described in plain English
                        Examples:
                        - "Check stock levels for SKU-123 at all locations"
                        - "Transfer 50 units of widget-X from godown_central to store_main_street"
                        - "Order 100 more units of popular-item-Y from supplier"
    
    Returns:
        A helpful response from the Inventory Agent with the information you requested
        
    Example:
        >>> result = route_to_inventory("Check stock for red shirts size small")
        >>> print(result)  # Shows stock levels across all locations
    """
    try:
        # Import what we need to create an inventory crew
        from crewai import Crew, Process
        from inventory_agents import (
            inventory_orchestrator_agent,  # The planner/analyst
            logistics_agent,               # Handles transfers
            procurement_agent              # Handles orders
        )
        from crewai import Task
        
        # Create a task that describes what we want the inventory team to do
        # Note: This request is coming through the Orchestrator Agent
        inventory_task = Task(
            description=(
                f"This request is being processed through the Orchestrator Agent. "
                f"{customer_request}"
            ),
            expected_output=(
                "A clear response with inventory status, transfer confirmations, "
                "or procurement orders - whatever is needed for this request. "
                "This response will be sent back to the Orchestrator for final formatting."
            ),
            agent=inventory_orchestrator_agent  # Start with the orchestrator who plans things
        )
        
        # Assemble the inventory crew - these agents work together
        inventory_crew = Crew(
            agents=[
                inventory_orchestrator_agent,  # Plans what needs to happen
                logistics_agent,               # Executes transfers
                procurement_agent              # Places orders
            ],
            tasks=[inventory_task],
            process=Process.sequential,  # One task at a time
            verbose=False  # Keep it quiet since we're calling from orchestrator
        )
        
        # Let the inventory team do their work!
        result = inventory_crew.kickoff()
        return str(result)
        
    except ImportError as e:
        # Couldn't find the inventory agent modules
        return (
            f"⚠️  Oops! I couldn't find the Inventory Agent modules. "
            f"This usually means the 'Inventory agent' folder is missing or not set up correctly. "
            f"Error details: {str(e)}"
        )
    except Exception as e:
        # Something unexpected went wrong
        return (
            f"❌ Hmm, we ran into an issue while routing to the Inventory Agent. "
            f"The agent might be busy or there could be a configuration problem. "
            f"Here's what happened: {str(e)}"
        )


@tool("Route to Fulfillment Agent")
def route_to_fulfillment(customer_request: str) -> str:
    """
    Send fulfillment requests to the Fulfillment Agent 🚚
    
    This handles getting products to customers - whether that means shipping
    something to their home or reserving it for pickup at a store. The
    Fulfillment Agent coordinates with warehouses and store staff to make
    sure everything happens smoothly.
    
    Args:
        customer_request: What fulfillment you need, described clearly
                        Examples:
                        - "Ship order ORD-123 to 123 Main St, City, State 12345"
                        - "Reserve item SKU-456 for customer C-789 at store S-102"
                        - "Process shipment for order with tracking ORD-456"
    
    Returns:
        Confirmation from the Fulfillment Agent with tracking numbers,
        pickup codes, or other relevant details
    
    Example:
        >>> result = route_to_fulfillment(
        ...     "Ship order ORD-123 with 2 red shirts to customer address"
        ... )
        >>> print(result)  # Shows tracking number and delivery estimate
    """
    try:
        from crewai import Crew, Process
        from agents import fulfillment_agent
        from crewai import Task
        
        # Create the fulfillment task
        # Note: This request is coming through the Orchestrator Agent
        fulfillment_task = Task(
            description=(
                f"This request is being processed through the Orchestrator Agent. "
                f"{customer_request}"
            ),
            expected_output=(
                "A confirmation response with either: shipment tracking information "
                "(tracking number, delivery date) OR in-store reservation details "
                "(pickup code, store location, hold expiry). "
                "This response will be sent back to the Orchestrator for final formatting."
            ),
            agent=fulfillment_agent
        )
        
        # Set up the fulfillment crew
        fulfillment_crew = Crew(
            agents=[fulfillment_agent],
            tasks=[fulfillment_task],
            process=Process.sequential,
            verbose=False  # Quiet mode when called from orchestrator
        )
        
        # Run it and get the results
        result = fulfillment_crew.kickoff()
        return str(result)
        
    except ImportError as e:
        return (
            f"⚠️  Couldn't find the Fulfillment Agent. "
            f"Make sure the 'Fullfillment_agent' folder exists and is properly set up. "
            f"Error: {str(e)}"
        )
    except Exception as e:
        return (
            f"❌ Something went wrong while contacting the Fulfillment Agent. "
            f"They might be experiencing issues. Error: {str(e)}"
        )


@tool("Route to Payment Agent")
def route_to_payment(customer_request: str) -> str:
    """
    Send payment requests to the Payment Agent 💳
    
    This handles all things payment-related! Whether it's processing a credit card,
    handling a UPI transaction, or setting up a kiosk-to-mobile payment handoff,
    the Payment Agent (working with Sales and Loyalty agents) knows how to handle it.
    
    Args:
        customer_request: What payment you need to process
                        Examples:
                        - "Process payment of $150 for customer cust-789 using credit card card-4567"
                        - "Generate kiosk-to-mobile handoff for customer at kiosk session kiosk-A9, amount $85.20"
                        - "Process payment with loyalty points for customer c123, 500 points"
    
    Returns:
        Transaction details including status, transaction ID, and any relevant information
    
    Example:
        >>> result = route_to_payment(
        ...     "Process $99.99 payment for customer C-456 using saved credit card"
        ... )
        >>> print(result)  # Shows transaction ID and status
    """
    try:
        from crewai import Crew, Process
        from crewai import Task
        
        # Import from the payment_agent directory
        # The payment crew has: sales_agent, payment_agent, and loyalty_agent
        # (Note: This loyalty_agent is for deducting points during payment)
        from agents import sales_agent, payment_agent, loyalty_agent
        
        # The payment crew uses hierarchical processing - sales agent coordinates,
        # payment agent handles transactions, loyalty agent manages points
        # Note: This request is coming through the Orchestrator Agent
        payment_task = Task(
            description=(
                f"This request is being processed through the Orchestrator Agent. "
                f"{customer_request}"
            ),
            expected_output=(
                "Payment processing results including: status (success/failed), "
                "transaction ID if successful, error messages if failed, and any "
                "handoff URLs if this is a kiosk-to-mobile scenario. "
                "This response will be sent back to the Orchestrator for final formatting."
            ),
            agent=sales_agent  # Sales agent orchestrates the payment flow
        )
        
        # Set up the payment crew with hierarchical structure
        payment_crew = Crew(
            agents=[sales_agent, payment_agent, loyalty_agent],
            tasks=[payment_task],
            process=Process.hierarchical,  # Sales agent manages the others
            verbose=False
        )
        
        # Process the payment!
        result = payment_crew.kickoff()
        return str(result)
        
    except ImportError as e:
        return (
            f"⚠️  Payment Agent modules not found. "
            f"Please check that the 'payment_agent' folder is set up correctly. "
            f"Error: {str(e)}"
        )
    except Exception as e:
        return (
            f"❌ Payment processing encountered an issue. "
            f"This could be a configuration problem or the payment system might be unavailable. "
            f"Error: {str(e)}"
        )


@tool("Route to Loyalty and Offers Agent")
def route_to_loyalty(customer_request: str) -> str:
    """
    Send loyalty and pricing requests to the Loyalty Agent 🎁
    
    This agent is your go-to for anything related to pricing, discounts, coupons,
    loyalty points, and special offers. They calculate the best deals for customers
    and make sure all applicable discounts are applied correctly.
    
    Args:
        customer_request: What loyalty/pricing help you need
                        Examples:
                        - "Calculate final price for customer c123 with cart ['prod-a', 'prod-b'] and coupon 'SAVE20'"
                        - "Apply 500 loyalty points to order total of $50 for customer C-456"
                        - "Check available offers for customer with 1500 loyalty points"
    
    Returns:
        Pricing breakdown showing original price, discounts applied, loyalty points used,
        and final price - all clearly explained
    
    Example:
        >>> result = route_to_loyalty(
        ...     "Calculate price for order with items A, B, C using coupon SAVE20"
        ... )
        >>> print(result)  # Shows detailed price breakdown
    """
    try:
        from crewai import Crew, Process
        from crewai import Task
        
        # Import from the 'loyalty and offers agent' folder
        # Note: We need to import from the correct directory
        import sys
        loyalty_agent_dir = os.path.join(base_dir, 'loyalty and offers agent')
        if loyalty_agent_dir not in sys.path:
            sys.path.insert(0, loyalty_agent_dir)
        
        from agents import sales_agent, loyalty_agent
        
        # Create the loyalty/pricing task
        loyalty_task = Task(
            description=(
                f"This request is being processed through the Orchestrator Agent. "
                f"{customer_request}"
            ),
            expected_output=(
                "A comprehensive pricing breakdown showing: original total, individual "
                "item prices, applied discounts/coupons, loyalty points used, "
                "final discounted price, and total savings. "
                "This response will be sent back to the Orchestrator for final formatting."
            ),
            agent=sales_agent  # Sales agent presents the results to customer
        )
        
        # Set up the loyalty crew
        # This crew is being invoked by the Orchestrator Agent
        loyalty_crew = Crew(
            agents=[sales_agent, loyalty_agent],
            tasks=[loyalty_task],
            process=Process.sequential,  # Sales agent works with loyalty agent
            verbose=False  # Keep quiet since orchestrator is managing this
        )
        
        # Calculate those savings!
        result = loyalty_crew.kickoff()
        return str(result)
        
    except ImportError as e:
        return (
            f"⚠️  Loyalty Agent not found. "
            f"Check that the 'loyalty and offers agent' folder exists and is configured. "
            f"Error: {str(e)}"
        )
    except Exception as e:
        return (
            f"❌ Couldn't process loyalty/pricing request. "
            f"The loyalty system might be experiencing issues. "
            f"Error: {str(e)}"
        )


@tool("Route to Post Purchase Support Agent")
def route_to_support(customer_request: str) -> str:
    """
    Send post-purchase support requests to the Support Agent 🎧
    
    After a customer makes a purchase, this agent helps with everything that comes next:
    tracking orders, processing returns/exchanges, handling damaged items, and
    collecting feedback. They're friendly, empathetic, and focused on making sure
    customers are happy!
    
    Args:
        customer_request: What support help is needed
                        Examples:
                        - "Track order ORD12345 and show current location and delivery estimate"
                        - "Process return for damaged item TSHIRT-BLU-M from order ORD56789"
                        - "Customer CUST777 wants to exchange item - check if replacement is available"
                        - "Get feedback survey link for customer CUST777 after order ORD12345"
    
    Returns:
        A friendly, helpful response that addresses the customer's concern with
        all the relevant details they need
    
    Example:
        >>> result = route_to_support(
        ...     "Customer wants to know where their order ORD-12345 is"
        ... )
        >>> print(result)  # Shows tracking info in a friendly way
    """
    try:
        from crewai import Crew, Process
        from agents import post_purchase_agent
        from crewai import Task
        
        # Create the support task
        # Note: This request is coming through the Orchestrator Agent
        support_task = Task(
            description=(
                f"This request is being processed through the Orchestrator Agent. "
                f"{customer_request}"
            ),
            expected_output=(
                "A warm, empathetic response that fully addresses the customer's concern. "
                "If tracking: include current status, carrier, tracking number, location, ETA. "
                "If return/exchange: include confirmation, return label URL, next steps. "
                "If feedback: include survey link and friendly request. "
                "This response will be sent back to the Orchestrator for final formatting."
            ),
            agent=post_purchase_agent
        )
        
        # Set up the support crew
        support_crew = Crew(
            agents=[post_purchase_agent],
            tasks=[support_task],
            process=Process.sequential,
            verbose=False  # Keep it quiet from orchestrator level
        )
        
        # Help that customer! 🎧
        result = support_crew.kickoff()
        return str(result)
        
    except ImportError as e:
        return (
            f"⚠️  Support Agent modules not found. "
            f"Please verify the 'post purchase support agent' folder is set up. "
            f"Error: {str(e)}"
        )
    except Exception as e:
        return (
            f"❌ Support request couldn't be processed. "
            f"The support system might be unavailable or misconfigured. "
            f"Error: {str(e)}"
        )


@tool("Analyze Request Intent")
def analyze_intent(customer_request: str) -> str:
    """
    Figure out which agent should handle this request - the smart way! 🧠
    
    This function reads through a customer request and figures out which specialist
    agent is best equipped to help. It looks for keywords and context clues to
    make an intelligent routing decision.
    
    Think of it as a smart receptionist who listens to what you need and
    directs you to the right department!
    
    Args:
        customer_request: The customer's request in their own words
                         Examples:
                         - "Do you have red shirts in stock?"
                         - "I want to pay for my order with my credit card"
                         - "Where is my order ORD-123?"
    
    Returns:
        A JSON object with routing recommendations:
        {
            "primary_agent": "inventory|fulfillment|payment|loyalty|support|unknown",
            "confidence": "high|low",
            "suggestion": "Additional guidance if needed"
        }
    
    Example:
        >>> result = analyze_intent("Check if SKU-123 is in stock")
        >>> print(result)  # {"primary_agent": "inventory", "confidence": "high"}
    """
    # Convert to lowercase so we can match keywords regardless of capitalization
    request_lower = customer_request.lower()
    
    # Look for inventory-related keywords
    # Things like: stock levels, checking SKUs, moving items between locations, ordering from suppliers
    inventory_keywords = ['stock', 'inventory', 'sku', 'transfer', 'procurement', 'supplier', 'replenish']
    if any(keyword in request_lower for keyword in inventory_keywords):
        return json.dumps({
            "primary_agent": "inventory",
            "confidence": "high",
            "reason": "Request contains inventory-related keywords"
        })
    
    # Look for fulfillment-related keywords
    # Things like: shipping orders, reserving items, warehouse operations, deliveries
    fulfillment_keywords = ['ship', 'fulfill', 'reserve', 'pickup', 'delivery', 'warehouse']
    if any(keyword in request_lower for keyword in fulfillment_keywords):
        return json.dumps({
            "primary_agent": "fulfillment",
            "confidence": "high",
            "reason": "Request contains fulfillment/shipping-related keywords"
        })
    
    # Look for payment-related keywords
    # Things like: processing payments, credit cards, transactions, kiosks
    payment_keywords = ['pay', 'payment', 'transaction', 'card', 'upi', 'kiosk', 'mobile']
    if any(keyword in request_lower for keyword in payment_keywords):
        return json.dumps({
            "primary_agent": "payment",
            "confidence": "high",
            "reason": "Request contains payment/transaction-related keywords"
        })
    
    # Look for loyalty and pricing keywords
    # Things like: loyalty points, coupons, discounts, promotions, pricing
    loyalty_keywords = ['loyalty', 'points', 'coupon', 'promotion', 'offer', 'discount', 'pricing']
    if any(keyword in request_lower for keyword in loyalty_keywords):
        return json.dumps({
            "primary_agent": "loyalty",
            "confidence": "high",
            "reason": "Request contains loyalty/pricing-related keywords"
        })
    
    # Look for support-related keywords
    # Things like: tracking orders, returns, refunds, exchanges, customer service
    support_keywords = ['track', 'order', 'return', 'refund', 'exchange', 'damaged', 'feedback', 'support']
    if any(keyword in request_lower for keyword in support_keywords):
        return json.dumps({
            "primary_agent": "support",
            "confidence": "high",
            "reason": "Request contains post-purchase support-related keywords"
        })
    
    # If we can't figure it out, let the orchestrator know it needs manual review
    return json.dumps({
        "primary_agent": "unknown",
        "confidence": "low",
        "suggestion": "Request doesn't match clear patterns. Review manually to determine best agent.",
        "note": "The orchestrator should examine this request more carefully"
    })


# ============================================================================
# Convenience Class for Easy Access
# ============================================================================

class OrchestratorTools:
    """
    A handy container class that holds all our routing tools 🎒
    
    You can use this if you want to access the tools as attributes,
    but you can also import the functions directly. Both work fine!
    
    Example:
        >>> tools = OrchestratorTools()
        >>> result = tools.route_to_inventory("Check stock for SKU-123")
    """
    route_to_inventory = route_to_inventory
    route_to_fulfillment = route_to_fulfillment
    route_to_payment = route_to_payment
    route_to_loyalty = route_to_loyalty
    route_to_support = route_to_support
    analyze_intent = analyze_intent

