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
sys.path.insert(0, os.path.join(base_dir, 'Recommendation agent'))
sys.path.insert(0, os.path.join(base_dir, 'recommendation agent 2'))
# Note: Orchestrator directory is already in path since we're running from it

from crewai.tools import tool


def _structured_success(result: Any) -> str:
    return json.dumps({"success": True, "result": result, "error": None})


def _structured_error(error_type: str, message: str, retryable: bool, user_message: str, details: Optional[Dict[str, Any]] = None) -> str:
    return json.dumps(
        {
            "success": False,
            "result": None,
            "error": {
                "type": error_type,
                "message": message,
                "retryable": retryable,
                "user_message": user_message,
                "details": details or {},
            },
        }
    )


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
    print("\n" + "="*70)
    print("📦 ROUTING TO INVENTORY AGENT")
    print("="*70)
    print(f"📝 Request: {customer_request}")
    print(f"🔍 Analyzing inventory request...")
    print("="*70 + "\n")
    
    try:
        from crewai import Crew, Process
        from inventory_agents import (
            inventory_orchestrator_agent,
            logistics_agent,
            procurement_agent
        )
        from crewai import Task
        
        print(f"🔧 [INVENTORY] Setting up inventory crew...")
        print(f"   - Agents: Orchestrator, Logistics, Procurement")
        print(f"   - Request: '{customer_request}'")
        
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
            agent=inventory_orchestrator_agent
        )
        
        print(f"🚀 [INVENTORY] Starting inventory processing...")
        inventory_crew = Crew(
            agents=[
                inventory_orchestrator_agent,
                logistics_agent,
                procurement_agent
            ],
            tasks=[inventory_task],
            process=Process.sequential,
            verbose=False
        )
        
        print(f"⚙️  [INVENTORY] Processing inventory request...")
        result = inventory_crew.kickoff()
        
        print(f"\n✅ [INVENTORY] Inventory processing complete!")
        print("="*70 + "\n")
        
        return _structured_success(str(result))
        
    except ImportError as e:
        # Couldn't find the inventory agent modules
        return _structured_error(
            "dependency_missing",
            str(e),
            retryable=False,
            user_message="Inventory service is temporarily unavailable. Please try again later.",
        )
    except Exception as e:
        return _structured_error(
            "inventory_error",
            str(e),
            retryable=True,
            user_message="We hit a snag while checking inventory. I'm retrying, or I can connect you to support.",
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
    print("\n" + "="*70)
    print("🚚 ROUTING TO FULFILLMENT AGENT")
    print("="*70)
    print(f"📝 Request: {customer_request}")
    print(f"🔍 Analyzing fulfillment request...")
    print("="*70 + "\n")
    
    try:
        from crewai import Crew, Process
        from agents import fulfillment_agent
        from crewai import Task
        
        print(f"🔧 [FULFILLMENT] Setting up fulfillment task...")
        print(f"   - Request: '{customer_request}'")
        print(f"   - Agent: Fulfillment Agent")
        
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
        
        print(f"🚀 [FULFILLMENT] Starting fulfillment processing...")
        fulfillment_crew = Crew(
            agents=[fulfillment_agent],
            tasks=[fulfillment_task],
            process=Process.sequential,
            verbose=False
        )
        
        print(f"⚙️  [FULFILLMENT] Processing fulfillment request...")
        result = fulfillment_crew.kickoff()
        
        print(f"\n✅ [FULFILLMENT] Fulfillment processing complete!")
        print("="*70 + "\n")
        
        return _structured_success(str(result))
        
    except ImportError as e:
        return _structured_error(
            "dependency_missing",
            str(e),
            retryable=False,
            user_message="Fulfillment service is unavailable. We can confirm your order once it is back.",
        )
    except Exception as e:
        return _structured_error(
            "fulfillment_error",
            str(e),
            retryable=True,
            user_message="There was an issue scheduling fulfillment. I can retry or follow up later.",
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
    print("\n" + "="*70)
    print("💳 ROUTING TO PAYMENT AGENT")
    print("="*70)
    print(f"📝 Request: {customer_request}")
    print(f"🔍 Analyzing payment request...")
    print("="*70 + "\n")
    
    try:
        from crewai import Crew, Process
        from crewai import Task
        from agents import sales_agent, payment_agent, loyalty_agent
        
        print(f"🔧 [PAYMENT] Setting up payment crew...")
        print(f"   - Agents: Sales (coordinator), Payment, Loyalty")
        print(f"   - Request: '{customer_request}'")
        print(f"   - Process: Hierarchical (Sales manages Payment & Loyalty)")
        
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
            agent=sales_agent
        )
        
        print(f"🚀 [PAYMENT] Starting payment processing...")
        payment_crew = Crew(
            agents=[sales_agent, payment_agent, loyalty_agent],
            tasks=[payment_task],
            process=Process.hierarchical,
            verbose=False
        )
        
        print(f"⚙️  [PAYMENT] Processing payment transaction...")
        result = payment_crew.kickoff()
        
        print(f"\n✅ [PAYMENT] Payment processing complete!")
        print("="*70 + "\n")
        
        return _structured_success(str(result))
        
    except ImportError as e:
        return _structured_error(
            "dependency_missing",
            str(e),
            retryable=False,
            user_message="Payment service is not available. Please try another method later.",
        )
    except Exception as e:
        return _structured_error(
            "payment_error",
            str(e),
            retryable=True,
            user_message="We couldn't complete the payment. I can retry or use a different method.",
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
        return _structured_success(str(result))
        
    except ImportError as e:
        return _structured_error(
            "dependency_missing",
            str(e),
            retryable=False,
            user_message="Loyalty pricing is unavailable right now. We'll proceed with standard pricing.",
        )
    except Exception as e:
        return _structured_error(
            "loyalty_error",
            str(e),
            retryable=True,
            user_message="We couldn't apply loyalty benefits. I can retry or continue without them.",
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
    print("\n" + "="*70)
    print("🎧 ROUTING TO SUPPORT AGENT")
    print("="*70)
    print(f"📝 Request: {customer_request}")
    print(f"🔍 Analyzing support request...")
    print("="*70 + "\n")
    
    try:
        from crewai import Crew, Process
        from agents import post_purchase_agent
        from crewai import Task
        
        request_lower = customer_request.lower()
        support_type = "general"
        if "track" in request_lower or "where" in request_lower:
            support_type = "order_tracking"
        elif "return" in request_lower:
            support_type = "return"
        elif "exchange" in request_lower:
            support_type = "exchange"
        elif "feedback" in request_lower or "survey" in request_lower:
            support_type = "feedback"
        
        print(f"🔧 [SUPPORT] Setting up support task...")
        print(f"   - Request: '{customer_request}'")
        print(f"   - Support type: {support_type}")
        print(f"   - Agent: Post Purchase Support Agent")
        
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
        
        print(f"🚀 [SUPPORT] Starting support processing...")
        support_crew = Crew(
            agents=[post_purchase_agent],
            tasks=[support_task],
            process=Process.sequential,
            verbose=False
        )
        
        print(f"⚙️  [SUPPORT] Processing support request...")
        result = support_crew.kickoff()
        
        print(f"\n✅ [SUPPORT] Support processing complete!")
        print("="*70 + "\n")
        
        return _structured_success(str(result))
        
    except ImportError as e:
        return _structured_error(
            "dependency_missing",
            str(e),
            retryable=False,
            user_message="Support service is temporarily unavailable. We can follow up later.",
        )
    except Exception as e:
        return _structured_error(
            "support_error",
            str(e),
            retryable=True,
            user_message="Support couldn't complete your request right now. I can retry or escalate.",
        )


@tool("Route to Recommendation Agent")
def route_to_recommendation(customer_request: str, user_id: str = "default_user") -> str:
    """
    Send product recommendation requests to the Recommendation Agent 🎯
    
    This handles voice-based and natural language product queries. The Recommendation
    Agent processes voice input, understands user intent, and returns personalized
    product recommendations based on user context and query.
    
    Args:
        customer_request: The product query in natural language
                        Examples:
                        - "looking for a shirt for date"
                        - "I need formal pants for office"
                        - "show me workout shoes"
                        - "find a casual dress"
        user_id: Optional user identifier for personalization (default: "default_user")
    
    Returns:
        A list of personalized product recommendations with scores and reasoning
    
    Example:
        >>> result = route_to_recommendation(
        ...     "looking for a shirt for date",
        ...     user_id="USER-123"
        ... )
        >>> print(result)  # Shows ranked recommendations
    """
    print("\n" + "="*70)
    print("🎯 ROUTING TO RECOMMENDATION AGENT")
    print("="*70)
    print(f"📝 Query: {customer_request}")
    print(f"👤 User ID: {user_id}")
    print(f"🔍 Analyzing query for product recommendations...")
    print("="*70 + "\n")
    
    try:
        from crewai import Crew, Process
        from agents import recommendation_agent
        from crewai import Task
        
        print(f"🔧 [RECOMMENDATION] Setting up recommendation task...")
        print(f"   - Query: '{customer_request}'")
        print(f"   - User: {user_id}")
        print(f"   - Agent: Recommendation Agent")
        
        recommendation_task = Task(
            description=(
                f"This request is being processed through the Orchestrator Agent. "
                f"User ID: {user_id}. "
                f"Query: {customer_request}"
            ),
            expected_output=(
                "A list of personalized product recommendations with item IDs, "
                "relevance scores, and explanations of why each product was recommended. "
                "This response will be sent back to the Orchestrator for final formatting."
            ),
            agent=recommendation_agent
        )
        
        print(f"🚀 [RECOMMENDATION] Starting recommendation crew...")
        recommendation_crew = Crew(
            agents=[recommendation_agent],
            tasks=[recommendation_task],
            process=Process.sequential,
            verbose=False
        )
        
        print(f"⚙️  [RECOMMENDATION] Processing recommendation request...")
        result = recommendation_crew.kickoff()
        
        print(f"\n✅ [RECOMMENDATION] Recommendation complete!")
        print(f"   - Results received: {len(str(result))} characters")
        print("="*70 + "\n")
        
        return _structured_success(str(result))
        
    except ImportError as e:
        print(f"\n❌ [RECOMMENDATION] Import error: {str(e)}")
        print("="*70 + "\n")
        return _structured_error(
            "dependency_missing",
            str(e),
            retryable=False,
            user_message="Recommendations are unavailable at the moment. We can browse manually.",
        )
    except Exception as e:
        print(f"\n❌ [RECOMMENDATION] Processing error: {str(e)}")
        print("="*70 + "\n")
        return _structured_error(
            "recommendation_error",
            str(e),
            retryable=True,
            user_message="We couldn't fetch recommendations right now. I can retry.",
        )


@tool("Route to Recommendation Agent 2")
def route_to_recommendation_v2(customer_request: str, user_id: str = "default_user") -> str:
    """
    Send product recommendation requests to the Advanced Recommendation Agent 2 🎯
    
    This uses real Ollama embeddings and Qdrant vector database for highly accurate,
    personalized product recommendations. It leverages real product data and customer
    profiles for superior personalization.
    
    Args:
        customer_request: The product query in natural language
                        Examples:
                        - "looking for a shirt for date"
                        - "I need formal pants for office"
                        - "show me workout shoes"
                        - "find a casual dress"
        user_id: Optional user identifier for personalization (default: "default_user")
    
    Returns:
        A list of personalized product recommendations with scores and reasoning
    
    Example:
        >>> result = route_to_recommendation_v2(
        ...     "looking for a shirt for date",
        ...     user_id="CUST001"
        ... )
        >>> print(result)  # Shows ranked recommendations
    """
    try:
        from crewai import Crew, Process
        from agents import recommendation_agent_2
        from crewai import Task
        
        # Create the recommendation task
        recommendation_task = Task(
            description=(
                f"This request is being processed through the Orchestrator Agent. "
                f"User ID: {user_id}. "
                f"Query: {customer_request}"
            ),
            expected_output=(
                "A list of personalized product recommendations with product IDs, titles, "
                "prices, relevance scores, and explanations of why each product was recommended. "
                "This response will be sent back to the Orchestrator for final formatting."
            ),
            agent=recommendation_agent_2
        )
        
        # Set up the recommendation crew
        recommendation_crew = Crew(
            agents=[recommendation_agent_2],
            tasks=[recommendation_task],
            process=Process.sequential,
            verbose=False  # Keep it quiet from orchestrator level
        )
        
        # Process the recommendation request! 🎯
        result = recommendation_crew.kickoff()
        return _structured_success(str(result))
        
    except ImportError as e:
        return _structured_error(
            "dependency_missing",
            str(e),
            retryable=False,
            user_message="Advanced recommendations are unavailable. I can use basic suggestions.",
        )
    except Exception as e:
        return _structured_error(
            "recommendation_error",
            str(e),
            retryable=True,
            user_message="We couldn't fetch recommendations right now. I can retry.",
        )


@tool("Analyze Request Intent")
def analyze_intent(customer_request: str) -> str:
    print(f"\n🔍 [ORCHESTRATOR] Analyzing intent for: '{customer_request}'")
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
    
    # Look for recommendation-related keywords
    # Things like: looking for, find, show me, recommend, suggest, search for products
    recommendation_keywords = ['looking for', 'find', 'show me', 'recommend', 'suggest', 'search for', 'need a', 'want a']
    if any(keyword in request_lower for keyword in recommendation_keywords):
        # Prefer Agent 2 (production-ready) if available, otherwise use Agent 1
        return json.dumps({
            "primary_agent": "recommendation_v2",
            "confidence": "high",
            "reason": "Request contains product search/recommendation-related keywords",
            "note": "Using Recommendation Agent 2 (production-ready with real data)"
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
    route_to_recommendation = route_to_recommendation
    route_to_recommendation_v2 = route_to_recommendation_v2
    analyze_intent = analyze_intent

