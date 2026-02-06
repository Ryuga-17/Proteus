"""
MCP Client for Retail Agent System

This client provides a simple interface to interact with the MCP server,
making it easy to use the orchestrator tools through the standardized MCP protocol.
"""
import os
import sys
import json
from typing import Optional, Dict, Any

# Add current directory to path
orchestrator_dir = os.path.dirname(os.path.abspath(__file__))
if orchestrator_dir not in sys.path:
    sys.path.insert(0, orchestrator_dir)

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("MCP SDK not installed. Please install with: pip install 'mcp[cli]'")
    ClientSession = None
    stdio_client = None


class OrchestratorMCPClient:
    """
    Client for interacting with the Retail Agent Orchestrator MCP server.
    
    This client provides a simplified interface to all orchestrator capabilities
    through the Model Context Protocol.
    """
    
    def __init__(self, server_path: Optional[str] = None, transport: str = "stdio"):
        """
        Initialize the MCP client.
        
        Args:
            server_path: Path to the MCP server script (defaults to mcp_server.py in same directory)
            transport: Transport type ("stdio" or "streamable-http")
        """
        if ClientSession is None:
            raise ImportError("MCP SDK is not installed. Install with: pip install 'mcp[cli]'")
        
        self.transport = transport
        if server_path is None:
            server_path = os.path.join(orchestrator_dir, "mcp_server.py")
        self.server_path = server_path
        
        # Server parameters for stdio transport
        if transport == "stdio":
            self.server_params = StdioServerParameters(
                command="python",
                args=[server_path],
                env=None
            )
        else:
            raise ValueError(f"Transport {transport} not yet supported. Use 'stdio'.")
        
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
    
    async def connect(self):
        """Connect to the MCP server."""
        if self.session is None:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    await session.initialize()
    
    async def disconnect(self):
        """Disconnect from the MCP server."""
        if self.session:
            # Session will close automatically when context exits
            self.session = None
    
    async def analyze_intent(self, customer_request: str) -> Dict[str, Any]:
        """
        Analyze customer request intent.
        
        Args:
            customer_request: The customer's request in plain English
        
        Returns:
            Dictionary with intent analysis results
        """
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "analyze_request_intent",
            arguments={"customer_request": customer_request}
        )
        return json.loads(result.content[0].text) if result.content else {}
    
    async def route_to_inventory(self, customer_request: str) -> str:
        """Route request to Inventory Agent."""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "route_to_inventory_agent",
            arguments={"customer_request": customer_request}
        )
        return result.content[0].text if result.content else ""
    
    async def route_to_fulfillment(self, customer_request: str) -> str:
        """Route request to Fulfillment Agent."""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "route_to_fulfillment_agent",
            arguments={"customer_request": customer_request}
        )
        return result.content[0].text if result.content else ""
    
    async def route_to_payment(self, customer_request: str) -> str:
        """Route request to Payment Agent."""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "route_to_payment_agent",
            arguments={"customer_request": customer_request}
        )
        return result.content[0].text if result.content else ""
    
    async def route_to_loyalty(self, customer_request: str) -> str:
        """Route request to Loyalty Agent."""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "route_to_loyalty_agent",
            arguments={"customer_request": customer_request}
        )
        return result.content[0].text if result.content else ""
    
    async def route_to_support(self, customer_request: str) -> str:
        """Route request to Support Agent."""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "route_to_support_agent",
            arguments={"customer_request": customer_request}
        )
        return result.content[0].text if result.content else ""
    
    async def route_to_recommendation(self, customer_request: str, user_id: str = "default_user") -> str:
        """Route request to Recommendation Agent."""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "route_to_recommendation_agent",
            arguments={"customer_request": customer_request, "user_id": user_id}
        )
        return result.content[0].text if result.content else ""
    
    async def route_to_recommendation_v2(self, customer_request: str, user_id: str = "default_user") -> str:
        """Route request to Recommendation Agent 2 (advanced)."""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "route_to_recommendation_agent_v2",
            arguments={"customer_request": customer_request, "user_id": user_id}
        )
        return result.content[0].text if result.content else ""
    
    async def handle_request(self, customer_request: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        Intelligently handle any customer request (convenience method).
        
        This method analyzes intent and routes automatically.
        
        Args:
            customer_request: The customer's request in plain English
            user_id: Optional user identifier for personalization
        
        Returns:
            Dictionary with intent analysis, routing decision, and agent response
        """
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "handle_customer_request",
            arguments={"customer_request": customer_request, "user_id": user_id}
        )
        return json.loads(result.content[0].text) if result.content else {}
    
    async def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get list of all available agent capabilities."""
        if not self.session:
            await self.connect()
        
        resource = await self.session.read_resource("agent://capabilities")
        return json.loads(resource.contents[0].text) if resource.contents else {}


# ============================================================================
# Simplified Synchronous Interface
# ============================================================================

class SimpleOrchestratorClient:
    """
    Simplified synchronous interface that wraps the async MCP client.
    
    This provides a simpler API for basic use cases where async isn't needed.
    Note: This uses direct tool imports for synchronous operation.
    """
    
    def __init__(self):
        """Initialize the simple client (uses direct imports, no MCP server needed)."""
        # Import tools directly for synchronous access
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
        
        self.analyze_intent = analyze_intent
        self.route_to_inventory = route_to_inventory
        self.route_to_fulfillment = route_to_fulfillment
        self.route_to_payment = route_to_payment
        self.route_to_loyalty = route_to_loyalty
        self.route_to_support = route_to_support
        self.route_to_recommendation = route_to_recommendation
        self.route_to_recommendation_v2 = route_to_recommendation_v2
    
    def handle_request(self, customer_request: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        Handle customer request by analyzing intent and routing appropriately.
        
        Args:
            customer_request: The customer's request in plain English
            user_id: Optional user identifier for personalization
        
        Returns:
            Dictionary with routing decision and agent response
        """
        # Analyze intent
        intent_result_str = self.analyze_intent(customer_request)
        try:
            intent_result = json.loads(intent_result_str)
        except json.JSONDecodeError:
            intent_result = {"primary_agent": "unknown", "confidence": "low"}
        
        primary_agent = intent_result.get("primary_agent", "unknown")
        
        # Route based on intent
        agent_response = None
        routing_success = False
        
        try:
            if primary_agent == "inventory":
                agent_response = self.route_to_inventory(customer_request)
                routing_success = True
            elif primary_agent == "fulfillment":
                agent_response = self.route_to_fulfillment(customer_request)
                routing_success = True
            elif primary_agent == "payment":
                agent_response = self.route_to_payment(customer_request)
                routing_success = True
            elif primary_agent == "loyalty":
                agent_response = self.route_to_loyalty(customer_request)
                routing_success = True
            elif primary_agent == "support":
                agent_response = self.route_to_support(customer_request)
                routing_success = True
            elif primary_agent == "recommendation_v2":
                agent_response = self.route_to_recommendation_v2(customer_request, user_id)
                routing_success = True
            elif primary_agent == "recommendation":
                agent_response = self.route_to_recommendation(customer_request, user_id)
                routing_success = True
            else:
                agent_response = "Unable to determine appropriate agent for this request."
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


# Convenience function for simple use cases
def create_client(use_mcp: bool = False) -> Any:
    """
    Create an orchestrator client.
    
    Args:
        use_mcp: If True, returns MCP client (async). If False, returns simple sync client.
    
    Returns:
        OrchestratorMCPClient (if use_mcp=True) or SimpleOrchestratorClient (if use_mcp=False)
    """
    if use_mcp:
        return OrchestratorMCPClient()
    else:
        return SimpleOrchestratorClient()

