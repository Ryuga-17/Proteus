# MCP Integration Quick Start Guide

## What is MCP?

Model Context Protocol (MCP) provides a standardized interface for accessing orchestrator tools, making request handling simpler and more consistent.

## Quick Start

### 1. Install Dependencies

```bash
pip install 'mcp[cli]'
```

Or update all requirements:

```bash
pip install -r Orchestrator/requirements.txt
pip install -r backend/requirements.txt
```

### 2. Simple Usage (Recommended)

The easiest way to use MCP functionality:

```python
from Orchestrator.mcp_client import SimpleOrchestratorClient

# Create client
client = SimpleOrchestratorClient()

# Handle any request - automatically analyzes intent and routes
result = client.handle_request(
    "Check stock for SKU-123 at all locations",
    user_id="USER-123"
)

print(f"Agent: {result['primary_agent']}")
print(f"Response: {result['agent_response']}")
```

### 3. Enable in Backend (Optional)

To use MCP in the FastAPI backend, set an environment variable:

```bash
export USE_MCP=true
```

Then the `/api/agent/query` endpoint will automatically use MCP for request handling.

### 4. Run MCP Server (For LLM Integration)

If you want to use the MCP server for LLM client integration:

```bash
# Stdio transport (default)
python Orchestrator/mcp_server.py

# HTTP transport
export MCP_TRANSPORT=streamable-http
python Orchestrator/mcp_server.py
```

## Key Benefits

✅ **Single Method**: Use `handle_request()` for any request  
✅ **Auto Routing**: Intent analysis and routing happens automatically  
✅ **Consistent API**: Same interface for all agent types  
✅ **LLM Ready**: Can be used with MCP-compatible LLM clients  
✅ **Easy Integration**: Drop-in replacement for direct orchestrator calls  

## Examples

### Example 1: Inventory Check

```python
from Orchestrator.mcp_client import SimpleOrchestratorClient

client = SimpleOrchestratorClient()
result = client.handle_request("Check stock for SKU-123")
print(result['agent_response'])
```

### Example 2: Payment Processing

```python
result = client.handle_request(
    "Process payment of $150 using credit card card-4567",
    user_id="CUSTOMER-789"
)
```

### Example 3: Direct Agent Routing

```python
# Route directly to a specific agent
response = client.route_to_inventory("Check stock for SKU-456")
response = client.route_to_payment("Process payment for order")
response = client.route_to_support("Track order ORD-123")
```

### Example 4: Intent Analysis

```python
# Analyze intent separately
intent = client.analyze_intent("Check stock for red shirts")
print(intent)  # {"primary_agent": "inventory", "confidence": "high", ...}
```

## Available Methods

### SimpleOrchestratorClient Methods

- `handle_request(request, user_id)` - Smart handler (analyzes + routes)
- `analyze_intent(request)` - Analyze request intent
- `route_to_inventory(request)` - Route to Inventory Agent
- `route_to_fulfillment(request)` - Route to Fulfillment Agent
- `route_to_payment(request)` - Route to Payment Agent
- `route_to_loyalty(request)` - Route to Loyalty Agent
- `route_to_support(request)` - Route to Support Agent
- `route_to_recommendation(request, user_id)` - Route to Recommendation Agent
- `route_to_recommendation_v2(request, user_id)` - Route to Recommendation Agent 2

## Testing

Run the example script:

```bash
python Orchestrator/example_mcp_usage.py
```

## Documentation

- **Full Guide**: See `Orchestrator/MCP_INTEGRATION.md` for detailed documentation
- **System Overview**: See `SYSTEM_EXPLANATION.md` for overall architecture

## Troubleshooting

**MCP SDK not found:**
```bash
pip install 'mcp[cli]'
```

**Import errors:**
Make sure the Orchestrator directory is in your Python path.

**Backend MCP not working:**
- Check that `USE_MCP=true` is set in environment
- Verify MCP dependencies are installed
- Check backend logs for error messages

## Next Steps

1. Try the simple client examples above
2. Run `python Orchestrator/example_mcp_usage.py` to see it in action
3. Enable MCP in your backend with `USE_MCP=true`
4. Read the full integration guide for advanced usage

