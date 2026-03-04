# MCP Integration Guide

## Overview

The Model Context Protocol (MCP) integration provides a standardized interface for accessing orchestrator tools, simplifying request handling and enabling better integration with LLM-based clients.

## Benefits of MCP Integration

1. **Standardized Interface**: All orchestrator tools are exposed through a consistent MCP interface
2. **Simplified Request Handling**: Single method (`handle_customer_request`) for routing any request
3. **Better LLM Integration**: MCP tools can be easily discovered and used by LLM clients
4. **Resource Management**: Agent capabilities are exposed as discoverable resources
5. **Prompt Templates**: Pre-built prompts for common request patterns

## Installation

Install the MCP SDK:

```bash
pip install 'mcp[cli]'
```

Or update requirements:

```bash
pip install -r Orchestrator/requirements.txt
```

## Architecture

```
┌─────────────────┐
│   MCP Client    │
│  (Optional)     │
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│   MCP Server    │
│ (mcp_server.py) │
└────────┬────────┘
         │
         │ Direct Calls
         │
┌────────▼────────┐
│ Orchestrator    │
│     Tools       │
└────────┬────────┘
         │
         │ Routes to
         │
┌────────▼────────┐
│  Agent Crews    │
│ (Inventory, etc)│
└─────────────────┘
```

## Usage Options

### Option 1: Direct Tool Access (Synchronous - Recommended)

The simplest way to use MCP functionality without running a server:

```python
from Orchestrator.mcp_client import SimpleOrchestratorClient

# Create client
client = SimpleOrchestratorClient()

# Handle any request (automatically analyzes intent and routes)
result = client.handle_request(
    "Check stock for SKU-123 at all locations",
    user_id="USER-123"
)

print(f"Agent used: {result['primary_agent']}")
print(f"Response: {result['agent_response']}")
```

### Option 2: MCP Server (Async - For LLM Integration)

For integration with LLM clients that support MCP:

```bash
# Run the MCP server
python Orchestrator/mcp_server.py
```

Or set environment variable for HTTP transport:

```bash
export MCP_TRANSPORT=streamable-http
python Orchestrator/mcp_server.py
```

Then use the async client:

```python
import asyncio
from Orchestrator.mcp_client import OrchestratorMCPClient

async def main():
    async with OrchestratorMCPClient() as client:
        # Analyze intent
        intent = await client.analyze_intent("Check stock for SKU-123")
        print(f"Intent: {intent}")
        
        # Route to specific agent
        response = await client.route_to_inventory("Check stock for SKU-123")
        print(f"Response: {response}")
        
        # Or use the smart handler
        result = await client.handle_request(
            "Check stock for SKU-123",
            user_id="USER-123"
        )
        print(f"Result: {result}")

asyncio.run(main())
```

### Option 3: Backend Integration

Enable MCP in the backend by setting an environment variable:

```bash
export USE_MCP=true
```

Then the backend will automatically use the MCP client for agent queries:

```python
# In backend/main.py, the agent_query endpoint will use MCP if enabled
POST /api/agent/query
{
    "request": "Check stock for SKU-123",
    "user_id": "USER-123"
}
```

## Available MCP Tools

### 1. `analyze_request_intent`

Analyzes customer request to determine which agent should handle it.

```python
result = await client.analyze_intent("Check stock for red shirts")
# Returns: {"primary_agent": "inventory", "confidence": "high", ...}
```

### 2. Agent Routing Tools

- `route_to_inventory_agent` - Routes to Inventory Agent
- `route_to_fulfillment_agent` - Routes to Fulfillment Agent
- `route_to_payment_agent` - Routes to Payment Agent
- `route_to_loyalty_agent` - Routes to Loyalty Agent
- `route_to_support_agent` - Routes to Support Agent
- `route_to_recommendation_agent` - Routes to Recommendation Agent
- `route_to_recommendation_agent_v2` - Routes to Recommendation Agent 2

### 3. `handle_customer_request` (Smart Handler)

Intelligently analyzes intent and routes automatically:

```python
result = await client.handle_request(
    "Check stock for SKU-123",
    user_id="USER-123"
)
# Returns: {
#   "intent_analysis": {...},
#   "primary_agent": "inventory",
#   "routing_success": True,
#   "agent_response": "..."
# }
```

## Available Resources

### `agent://capabilities`

Get a list of all available agent capabilities:

```python
capabilities = await client.get_agent_capabilities()
# Returns: {
#   "inventory_agent": {"description": "...", "capabilities": [...]},
#   ...
# }
```

## Available Prompts

### `create_inventory_request`

Create a formatted inventory request:

```python
prompt = create_inventory_request(
    sku="SKU-123",
    location="store_main_street",
    action="check"
)
```

### `create_support_request`

Create a formatted support request:

```python
prompt = create_support_request(
    order_id="ORD-123",
    request_type="track"
)
```

## Integration with Backend

The backend can use MCP in two ways:

1. **Direct Integration** (Recommended): Uses `SimpleOrchestratorClient` directly
2. **MCP Server**: Connects to running MCP server via stdio or HTTP

To enable MCP in backend:

```bash
# In .env file
USE_MCP=true
```

## Example: Full Request Flow

```python
from Orchestrator.mcp_client import SimpleOrchestratorClient

# Initialize client
client = SimpleOrchestratorClient()

# Handle a complex request
result = client.handle_request(
    "I want to check if red shirts size small are in stock, "
    "and if available, calculate the price with my loyalty points",
    user_id="CUSTOMER-456"
)

# The client will:
# 1. Analyze intent (may detect multiple agents needed)
# 2. Route to appropriate agent(s)
# 3. Return combined results

print(f"Agent: {result['primary_agent']}")
print(f"Success: {result['routing_success']}")
print(f"Response: {result['agent_response']}")
```

## Advantages Over Direct Orchestrator Calls

1. **Simplified API**: Single `handle_request()` method instead of multiple routing functions
2. **Automatic Intent Analysis**: Intent is analyzed automatically before routing
3. **Standardized Responses**: Consistent response format across all agents
4. **Discoverable Tools**: MCP tools can be discovered by LLM clients
5. **Resource Access**: Agent capabilities are exposed as queryable resources
6. **Prompt Templates**: Pre-built prompts for common patterns

## Troubleshooting

### MCP SDK Not Found

```bash
pip install 'mcp[cli]'
```

### Import Errors

Make sure the Orchestrator directory is in your Python path:

```python
import sys
sys.path.insert(0, 'path/to/Orchestrator')
```

### Server Connection Issues

If using MCP server mode, ensure the server is running:

```bash
python Orchestrator/mcp_server.py
```

## Next Steps

1. **Enable MCP in Backend**: Set `USE_MCP=true` in environment
2. **Test Integration**: Try the example code above
3. **Customize Prompts**: Add custom prompt templates for your use cases
4. **Extend Resources**: Add more resources for additional metadata
5. **LLM Integration**: Connect LLM clients that support MCP protocol

## See Also

- [System Explanation](./SYSTEM_EXPLANATION.md) - Overall system architecture
- [Orchestrator Tools](./orchestrator_tools.py) - Underlying tool implementations
- [MCP Documentation](https://modelcontextprotocol.io) - Official MCP documentation

