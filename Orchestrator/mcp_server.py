"""
MCP Server for Retail Agent System

This MCP (Model Context Protocol) server exposes all orchestrator routing tools
as standardized MCP tools, making it easier to integrate with LLM-based clients
and simplifying request handling across the system.
"""
import os
import sys
import json
from typing import Optional, Dict, Any

# Add current directory to path for imports
orchestrator_dir = os.path.dirname(os.path.abspath(__file__))
if orchestrator_dir not in sys.path:
    sys.path.insert(0, orchestrator_dir)

# Load environment variables
try:
    from dotenv import load_dotenv
    project_root = os.path.dirname(orchestrator_dir)
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("MCP SDK not installed. Please install with: pip install 'mcp[cli]'")
    sys.exit(1)

# Import orchestrator tools
from orchestrator_tools import (
    analyze_intent,
    route_to_inventory,
    route_to_fulfillment,
    route_to_payment,
    route_to_loyalty,
    route_to_support,
    route_to_recommendation,
    route_to_recommendation_v2
)

# Initialize the MCP server
mcp = FastMCP("Retail Agent Orchestrator", json_response=True)


# ============================================================================
# Intent Analysis Tool
# ============================================================================

@mcp.tool()
def analyze_request_intent(customer_request: str) -> Dict[str, Any]:
    """
    Analyze customer request intent to determine which agent should handle it.
    
    This tool analyzes the incoming request and returns routing recommendations
    with confidence levels, helping the orchestrator make intelligent routing decisions.
    
    Args:
        customer_request: The customer's request in plain English
    
    Returns:
        JSON object with primary_agent, confidence, and routing suggestions
    """
    result_str = analyze_intent(customer_request)
    try:
        return json.loads(result_str)
    except json.JSONDecodeError:
        return {
            "primary_agent": "unknown",
            "confidence": "low",
            "raw_result": result_str
        }


# ============================================================================
# Agent Routing Tools
# ============================================================================

@mcp.tool()
def route_to_inventory_agent(customer_request: str) -> str:
    """
    Route inventory-related requests to the Inventory Agent.
    
    Handles stock checks, transfers between locations, and procurement orders.
    
    Args:
        customer_request: Inventory-related request description
    
    Returns:
        Response from the Inventory Agent with stock information or confirmations
    """
    return route_to_inventory(customer_request)


@mcp.tool()
def route_to_fulfillment_agent(customer_request: str) -> str:
    """
    Route fulfillment requests to the Fulfillment Agent.
    
    Handles shipping orders, in-store reservations, and delivery coordination.
    
    Args:
        customer_request: Fulfillment-related request description
    
    Returns:
        Response from the Fulfillment Agent with shipping/reservation details
    """
    return route_to_fulfillment(customer_request)


@mcp.tool()
def route_to_payment_agent(customer_request: str) -> str:
    """
    Route payment processing requests to the Payment Agent.
    
    Handles credit cards, UPI, kiosk-to-mobile payments, and transactions.
    
    Args:
        customer_request: Payment processing request description
    
    Returns:
        Response from the Payment Agent with transaction status and details
    """
    return route_to_payment(customer_request)


@mcp.tool()
def route_to_loyalty_agent(customer_request: str) -> str:
    """
    Route loyalty and pricing requests to the Loyalty Agent.
    
    Handles pricing calculations, discounts, coupons, and loyalty points.
    
    Args:
        customer_request: Loyalty/pricing-related request description
    
    Returns:
        Response from the Loyalty Agent with pricing breakdown and discounts
    """
    return route_to_loyalty(customer_request)


@mcp.tool()
def route_to_support_agent(customer_request: str) -> str:
    """
    Route post-purchase support requests to the Support Agent.
    
    Handles order tracking, returns, exchanges, and customer feedback.
    
    Args:
        customer_request: Support-related request description
    
    Returns:
        Response from the Support Agent with helpful information or confirmations
    """
    return route_to_support(customer_request)


@mcp.tool()
def route_to_recommendation_agent(customer_request: str, user_id: str = "default_user") -> str:
    """
    Route product recommendation requests to the Recommendation Agent.
    
    Handles voice-based and natural language product queries with personalized recommendations.
    
    Args:
        customer_request: Product query in natural language
        user_id: Optional user identifier for personalization
    
    Returns:
        Response from the Recommendation Agent with product recommendations
    """
    return route_to_recommendation(customer_request, user_id)


@mcp.tool()
def route_to_recommendation_agent_v2(customer_request: str, user_id: str = "default_user") -> str:
    """
    Route product recommendation requests to the Advanced Recommendation Agent 2.
    
    Uses real Ollama embeddings and Qdrant vector database for highly accurate,
    personalized product recommendations with real product data.
    
    Args:
        customer_request: Product query in natural language
        user_id: Optional user identifier for personalization
    
    Returns:
        Response from the Recommendation Agent 2 with personalized recommendations
    """
    return route_to_recommendation_v2(customer_request, user_id)


# ============================================================================
# Smart Routing Tool (Convenience Tool)
# ============================================================================

@mcp.tool()
def handle_customer_request(customer_request: str, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Intelligently handle any customer request by analyzing intent and routing appropriately.
    
    This is a convenience tool that combines intent analysis with routing, making it
    easy to handle any request through a single interface.
    
    Args:
        customer_request: The customer's request in plain English
        user_id: Optional user identifier for personalization
    
    Returns:
        Dictionary with routing decision and agent response
    """
    # First, analyze the intent
    intent_result = analyze_request_intent(customer_request)
    primary_agent = intent_result.get("primary_agent", "unknown")
    
    # Route based on intent
    agent_response = None
    routing_success = False
    
    try:
        if primary_agent == "inventory":
            agent_response = route_to_inventory_agent(customer_request)
            routing_success = True
        elif primary_agent == "fulfillment":
            agent_response = route_to_fulfillment_agent(customer_request)
            routing_success = True
        elif primary_agent == "payment":
            agent_response = route_to_payment_agent(customer_request)
            routing_success = True
        elif primary_agent == "loyalty":
            agent_response = route_to_loyalty_agent(customer_request)
            routing_success = True
        elif primary_agent == "support":
            agent_response = route_to_support_agent(customer_request)
            routing_success = True
        elif primary_agent == "recommendation_v2":
            agent_response = route_to_recommendation_agent_v2(customer_request, user_id)
            routing_success = True
        elif primary_agent == "recommendation":
            agent_response = route_to_recommendation_agent(customer_request, user_id)
            routing_success = True
        else:
            agent_response = "Unable to determine appropriate agent for this request. Please try rephrasing your request."
            routing_success = False
    except Exception as e:
        agent_response = f"Error routing request: {str(e)}"
        routing_success = False
    
    return {
        "intent_analysis": intent_result,
        "primary_agent": primary_agent,
        "routing_success": routing_success,
        "agent_response": agent_response,
        "user_id": user_id
    }


# ============================================================================
# Resources (Data Sources)
# ============================================================================

@mcp.resource("agent://capabilities")
def get_agent_capabilities() -> str:
    """
    Get a list of all available agent capabilities in the system.
    """
    capabilities = {
        "inventory_agent": {
            "description": "Handles stock checks, transfers, and procurement",
            "capabilities": ["stock_levels", "transfers", "supplier_orders"]
        },
        "fulfillment_agent": {
            "description": "Handles shipping and in-store reservations",
            "capabilities": ["shipments", "reservations", "delivery_tracking"]
        },
        "payment_agent": {
            "description": "Handles payment processing and transactions",
            "capabilities": ["credit_card", "upi", "kiosk_mobile", "transactions"]
        },
        "loyalty_agent": {
            "description": "Handles pricing, discounts, and loyalty points",
            "capabilities": ["pricing", "discounts", "coupons", "loyalty_points"]
        },
        "support_agent": {
            "description": "Handles post-purchase support and customer service",
            "capabilities": ["order_tracking", "returns", "exchanges", "feedback"]
        },
        "recommendation_agent": {
            "description": "Provides product recommendations based on voice queries",
            "capabilities": ["voice_search", "product_recommendations", "personalization"]
        },
        "recommendation_agent_v2": {
            "description": "Advanced recommendations with real data and embeddings",
            "capabilities": ["semantic_search", "vector_recommendations", "real_data"]
        }
    }
    return json.dumps(capabilities, indent=2)


# ============================================================================
# Prompts (Templates)
# ============================================================================

@mcp.prompt()
def create_inventory_request(sku: str, location: Optional[str] = None, action: str = "check") -> str:
    """
    Create a formatted inventory request prompt.
    
    Args:
        sku: The SKU to check/manage
        location: Optional location to check
        action: Action type (check, transfer, order)
    """
    if action == "check":
        if location:
            return f"Check stock levels for {sku} at {location}"
        return f"Check stock levels for {sku} at all locations"
    elif action == "transfer":
        return f"Transfer {sku} between locations"
    elif action == "order":
        return f"Order more units of {sku} from supplier"
    return f"Handle inventory request for {sku}"


@mcp.prompt()
def create_support_request(order_id: Optional[str] = None, request_type: str = "track") -> str:
    """
    Create a formatted support request prompt.
    
    Args:
        order_id: Optional order ID to track
        request_type: Type of support request (track, return, exchange, feedback)
    """
    if request_type == "track" and order_id:
        return f"Track order {order_id} and show current location and delivery estimate"
    elif request_type == "return":
        return f"Process return for order {order_id}" if order_id else "Process return request"
    elif request_type == "exchange":
        return f"Process exchange for order {order_id}" if order_id else "Process exchange request"
    elif request_type == "feedback":
        return f"Get feedback survey link for order {order_id}" if order_id else "Get feedback survey"
    return "Provide customer support assistance"


# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    # Run the server with stdio transport (for CLI usage)
    # Can also use "streamable-http" for HTTP transport
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    print(f"Starting MCP server with {transport} transport...", file=sys.stderr)
    mcp.run(transport=transport)

