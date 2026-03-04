"""
Example: Using MCP Client for Request Handling

This example demonstrates how to use the MCP client to simplify request handling.
"""

# Example 1: Simple synchronous client (recommended for most use cases)
from mcp_client import SimpleOrchestratorClient

def example_simple_client():
    """Example using the simple synchronous client."""
    print("="*70)
    print("Example 1: Simple Synchronous Client")
    print("="*70)
    
    # Create client
    client = SimpleOrchestratorClient()
    
    # Handle a request - it automatically analyzes intent and routes
    result = client.handle_request(
        "Check stock levels for SKU-123 at all store locations",
        user_id="USER-123"
    )
    
    print(f"\nIntent Analysis: {result['intent_analysis']}")
    print(f"Primary Agent: {result['primary_agent']}")
    print(f"Routing Success: {result['routing_success']}")
    print(f"\nAgent Response:\n{result['agent_response']}")
    
    return result


def example_direct_routing():
    """Example of routing directly to a specific agent."""
    print("\n" + "="*70)
    print("Example 2: Direct Agent Routing")
    print("="*70)
    
    client = SimpleOrchestratorClient()
    
    # Route directly to inventory agent
    response = client.route_to_inventory(
        "Check stock for SKU-456 at store_main_street and transfer 10 units if needed"
    )
    
    print(f"\nInventory Agent Response:\n{response}")
    
    return response


def example_intent_analysis():
    """Example of analyzing intent separately."""
    print("\n" + "="*70)
    print("Example 3: Intent Analysis Only")
    print("="*70)
    
    client = SimpleOrchestratorClient()
    
    requests = [
        "Check stock for red shirts",
        "Process payment for my order",
        "Where is my order ORD-123?",
        "Calculate price with my loyalty points",
        "Show me some workout shoes"
    ]
    
    for request in requests:
        intent_str = client.analyze_intent(request)
        print(f"\nRequest: '{request}'")
        print(f"Intent: {intent_str}")


def example_multiple_agents():
    """Example of handling requests that might need multiple agents."""
    print("\n" + "="*70)
    print("Example 4: Complex Multi-Agent Request")
    print("="*70)
    
    client = SimpleOrchestratorClient()
    
    # This request might trigger inventory check first, then pricing
    complex_request = (
        "I want to check if red shirts size small are in stock at store_main_street, "
        "and if available, calculate the final price with my loyalty points and coupon SAVE20"
    )
    
    result = client.handle_request(complex_request, user_id="CUSTOMER-456")
    
    print(f"\nRequest: '{complex_request}'")
    print(f"Primary Agent: {result['primary_agent']}")
    print(f"Response:\n{result['agent_response']}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("MCP Client Usage Examples")
    print("="*70 + "\n")
    
    try:
        # Run examples
        example_simple_client()
        example_direct_routing()
        example_intent_analysis()
        example_multiple_agents()
        
        print("\n" + "="*70)
        print("All examples completed successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

