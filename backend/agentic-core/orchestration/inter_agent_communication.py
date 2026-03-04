"""
Inter-Agent Communication System - Agents Talking Through Orchestrator 🤝

This module enables agents to communicate with each other through the Orchestrator.
Agents can request help from other agents, share information, and coordinate
multi-agent workflows - all while maintaining the Orchestrator as the central
communication hub.

Communication Protocol:
- Agents send messages/requests to Orchestrator
- Orchestrator routes to the appropriate agent
- Response flows back through Orchestrator
- Original agent receives the response

All communication flows through Orchestrator - agents never talk directly to each other!
"""
import sys
import os

# Add Orchestrator to path (we're already in Orchestrator directory)
# No need to add it to path since we're importing from same directory

from crewai.tools import tool

# Import routing functions - these will be called dynamically to avoid circular imports
def _import_routing_tools():
    """Dynamically import routing tools to avoid circular dependencies"""
    from orchestrator_tools import (
        route_to_inventory,
        route_to_fulfillment,
        route_to_payment,
        route_to_loyalty,
        route_to_support
    )
    return {
        'inventory': route_to_inventory,
        'fulfillment': route_to_fulfillment,
        'payment': route_to_payment,
        'loyalty': route_to_loyalty,
        'support': route_to_support
    }


# ============================================================================
# COMMUNICATION TOOLS - Agents use these to request help from other agents
# ============================================================================

@tool("Request Help from Inventory Agent")
def request_inventory_help(request_description: str, context: str = "") -> str:
    """
    Request help from the Inventory Agent 📦
    
    Use this when your agent needs inventory-related information:
    - Checking stock levels
    - Verifying availability
    - Getting inventory data
    - Requesting transfers or orders
    
    This request flows through the Orchestrator to maintain centralized communication.
    
    Args:
        request_description: What you need from the Inventory Agent
                           Example: "Check stock for SKU-123 at all locations"
        context: Optional context about why you need this (helps the agent understand)
                Example: "Need to verify availability before processing order"
    
    Returns:
        Response from the Inventory Agent (via Orchestrator)
    
    Example:
        >>> result = request_inventory_help(
        ...     "Check stock for SKU-123",
        ...     "Verifying availability before fulfillment"
        ... )
    """
    routing_tools = _import_routing_tools()
    full_request = request_description
    if context:
        full_request = f"{request_description} Context: {context}"
    
    return routing_tools['inventory'](full_request)


@tool("Request Help from Fulfillment Agent")
def request_fulfillment_help(request_description: str, context: str = "") -> str:
    """
    Request help from the Fulfillment Agent 🚚
    
    Use this when your agent needs fulfillment-related help:
    - Shipping orders
    - Reserving items at stores
    - Getting tracking information
    - Checking fulfillment status
    
    This request flows through the Orchestrator to maintain centralized communication.
    
    Args:
        request_description: What you need from the Fulfillment Agent
                           Example: "Ship order ORD-123 to customer address"
        context: Optional context about why you need this
                Example: "Order is confirmed and paid, ready to ship"
    
    Returns:
        Response from the Fulfillment Agent (via Orchestrator)
    """
    routing_tools = _import_routing_tools()
    full_request = request_description
    if context:
        full_request = f"{request_description} Context: {context}"
    
    return routing_tools['fulfillment'](full_request)


@tool("Request Help from Payment Agent")
def request_payment_help(request_description: str, context: str = "") -> str:
    """
    Request help from the Payment Agent 💳
    
    Use this when your agent needs payment-related help:
    - Processing payments
    - Verifying transactions
    - Handling refunds
    - Payment status checks
    
    This request flows through the Orchestrator to maintain centralized communication.
    
    Args:
        request_description: What you need from the Payment Agent
                           Example: "Process $150 payment for customer C-456"
        context: Optional context about why you need this
                Example: "Order total is $150, customer ready to pay"
    
    Returns:
        Response from the Payment Agent (via Orchestrator)
    """
    routing_tools = _import_routing_tools()
    full_request = request_description
    if context:
        full_request = f"{request_description} Context: {context}"
    
    return routing_tools['payment'](full_request)


@tool("Request Help from Loyalty Agent")
def request_loyalty_help(request_description: str, context: str = "") -> str:
    """
    Request help from the Loyalty Agent 🎁
    
    Use this when your agent needs loyalty/pricing-related help:
    - Calculating prices with discounts
    - Applying coupons
    - Checking loyalty point balances
    - Pricing breakdowns
    
    This request flows through the Orchestrator to maintain centralized communication.
    
    Args:
        request_description: What you need from the Loyalty Agent
                           Example: "Calculate price with coupon SAVE20"
        context: Optional context about why you need this
                Example: "Customer wants to checkout, need final price"
    
    Returns:
        Response from the Loyalty Agent (via Orchestrator)
    """
    routing_tools = _import_routing_tools()
    full_request = request_description
    if context:
        full_request = f"{request_description} Context: {context}"
    
    return routing_tools['loyalty'](full_request)


@tool("Request Help from Support Agent")
def request_support_help(request_description: str, context: str = "") -> str:
    """
    Request help from the Support Agent 🎧
    
    Use this when your agent needs support-related help:
    - Order tracking information
    - Return/exchange processing
    - Customer feedback collection
    - Support-related data
    
    This request flows through the Orchestrator to maintain centralized communication.
    
    Args:
        request_description: What you need from the Support Agent
                           Example: "Track order ORD-12345 for customer"
        context: Optional context about why you need this
                Example: "Customer is asking about delivery status"
    
    Returns:
        Response from the Support Agent (via Orchestrator)
    """
    routing_tools = _import_routing_tools()
    full_request = request_description
    if context:
        full_request = f"{request_description} Context: {context}"
    
    return routing_tools['support'](full_request)


@tool("Request Help from Any Agent")
def request_agent_help(target_agent: str, request_description: str, context: str = "") -> str:
    """
    Request help from any agent (generic interface) 🔄
    
    This is a smart routing function that automatically routes to the right agent
    based on the target_agent name. Use this when you're not sure which specific
    tool to use, or when you want a unified interface.
    
    All requests flow through the Orchestrator to maintain centralized communication.
    
    Args:
        target_agent: Which agent you need ("inventory", "fulfillment", "payment", "loyalty", "support")
                    Example: "inventory"
        request_description: What you need from that agent
                           Example: "Check stock for SKU-123"
        context: Optional context about why you need this
    
    Returns:
        Response from the requested agent (via Orchestrator)
    
    Example:
        >>> result = request_agent_help(
        ...     "inventory",
        ...     "Check stock for SKU-123",
        ...     "Verifying before order processing"
        ... )
    """
    routing_tools = _import_routing_tools()
    target_agent_lower = target_agent.lower().strip()
    
    if target_agent_lower not in routing_tools:
        return (
            f"⚠️  Unknown agent: '{target_agent}'. "
            f"Available agents: {', '.join(routing_tools.keys())}"
        )
    
    full_request = request_description
    if context:
        full_request = f"{request_description} Context: {context}"
    
    routing_function = routing_tools[target_agent_lower]
    return routing_function(full_request)


# Export all communication tools
class InterAgentCommunication:
    """
    Inter-Agent Communication Tools - For agents to request help from each other
    
    These tools allow agents to communicate with other agents through the Orchestrator.
    Agents use these tools when they need information or services from other specialists.
    """
    request_inventory_help = request_inventory_help
    request_fulfillment_help = request_fulfillment_help
    request_payment_help = request_payment_help
    request_loyalty_help = request_loyalty_help
    request_support_help = request_support_help
    request_agent_help = request_agent_help

