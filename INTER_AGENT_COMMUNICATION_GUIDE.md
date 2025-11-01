# Inter-Agent Communication Guide 🤝

## Overview

Agents in this system can communicate with each other through the **Orchestrator**. This enables agents to request help from other specialist agents while maintaining centralized communication control.

---

## How It Works

### Communication Flow

```
Agent A needs help
    ↓
Agent A uses inter-agent communication tool
    ↓
Request flows through Orchestrator
    ↓
Orchestrator routes to Agent B
    ↓
Agent B processes request
    ↓
Response flows back through Orchestrator
    ↓
Agent A receives response
```

**Key Principle:** All agent-to-agent communication flows through the Orchestrator. Agents never communicate directly with each other.

---

## Available Communication Tools

### 1. Request Help from Inventory Agent 📦

```python
request_inventory_help(
    request_description="Check stock for SKU-123",
    context="Verifying availability before processing order"
)
```

**When to use:**
- Need to check stock levels
- Verify item availability
- Get inventory data
- Request transfers or orders

**Example:**
```python
# Fulfillment Agent checking stock before shipping
result = request_inventory_help(
    "Check stock for SKU-123 at warehouse_1",
    "Need to verify stock before fulfilling order ORD-456"
)
```

---

### 2. Request Help from Fulfillment Agent 🚚

```python
request_fulfillment_help(
    request_description="Ship order ORD-123 to customer address",
    context="Order is confirmed and paid, ready to ship"
)
```

**When to use:**
- Need to ship an order
- Reserve items at a store
- Get tracking information
- Check fulfillment status

**Example:**
```python
# Support Agent processing a return replacement
result = request_fulfillment_help(
    "Ship replacement item SKU-123 to customer C-456",
    "Processing replacement for damaged item return"
)
```

---

### 3. Request Help from Payment Agent 💳

```python
request_payment_help(
    request_description="Process $150 payment for customer C-456",
    context="Order total is $150, customer ready to pay"
)
```

**When to use:**
- Process payments
- Verify transactions
- Handle refunds
- Check payment status

**Example:**
```python
# Support Agent processing a refund
result = request_payment_help(
    "Process refund of $50 for order ORD-12345",
    "Customer returning damaged item, processing refund"
)
```

---

### 4. Request Help from Loyalty Agent 🎁

```python
request_loyalty_help(
    request_description="Calculate price with coupon SAVE20",
    context="Customer wants to checkout, need final price"
)
```

**When to use:**
- Calculate prices with discounts
- Apply coupons
- Check loyalty point balances
- Get pricing breakdowns

**Example:**
```python
# Inventory Agent checking pricing before ordering
result = request_loyalty_help(
    "Calculate price for order with items A, B, C",
    "Need pricing for cost analysis before procurement"
)
```

---

### 5. Request Help from Support Agent 🎧

```python
request_support_help(
    request_description="Track order ORD-12345 for customer",
    context="Customer is asking about delivery status"
)
```

**When to use:**
- Get order tracking information
- Process returns/exchanges
- Collect customer feedback
- Get support-related data

**Example:**
```python
# Fulfillment Agent checking order status
result = request_support_help(
    "Get tracking details for order ORD-12345",
    "Verifying shipment status before updating customer"
)
```

---

### 6. Generic Agent Help Request 🔄

```python
request_agent_help(
    target_agent="inventory",  # or "fulfillment", "payment", "loyalty", "support"
    request_description="Check stock for SKU-123",
    context="Verifying before order processing"
)
```

**When to use:**
- When you're not sure which specific tool to use
- When you want a unified interface
- Dynamic agent selection based on runtime conditions

**Example:**
```python
# Dynamic agent selection
agent_needed = determine_which_agent()  # Some logic
result = request_agent_help(
    agent_needed,
    "Process this request",
    "Context information"
)
```

---

## Agents with Communication Capabilities

### ✅ Support Agent
**Can communicate with:**
- Inventory Agent (for checking stock during exchanges)
- Fulfillment Agent (for fulfillment status)
- Payment Agent (for refunds)
- Loyalty Agent (for pricing info)

**Use cases:**
- "Customer wants to exchange item - check inventory for replacement"
- "Process refund through payment agent"
- "Get fulfillment status for tracking"

---

### ✅ Fulfillment Agent
**Can communicate with:**
- Inventory Agent (verify stock before shipping)
- Payment Agent (verify payment before fulfillment)
- Support Agent (get order/tracking info)

**Use cases:**
- "Check stock before reserving at store"
- "Verify payment status before shipping"
- "Get order details from support agent"

---

### ✅ Inventory Agent
**Can communicate with:**
- Fulfillment Agent (check fulfillment status)
- Payment Agent (verify payment before ordering)
- Loyalty Agent (get pricing information)

**Use cases:**
- "Check if items are being fulfilled before ordering more"
- "Verify payment before placing supplier order"
- "Get pricing info for cost analysis"

---

### 📝 Payment Agent & Loyalty Agent
These agents typically work within their own crews but can request help when needed through their sales_agent coordinator.

---

## Example Scenarios

### Scenario 1: Support Agent Processing Exchange

```
Customer: "I want to exchange my damaged item"

1. Support Agent receives request
2. Support Agent uses request_inventory_help()
   → "Check stock for SKU-123 at all locations"
   → Context: "Customer wants exchange for damaged item"
3. Orchestrator routes to Inventory Agent
4. Inventory Agent returns: "Stock available at Store A: 5 units"
5. Support Agent receives result
6. Support Agent processes exchange with inventory confirmation
```

### Scenario 2: Fulfillment Agent Verifying Before Shipping

```
Request: "Ship order ORD-123"

1. Fulfillment Agent receives request
2. Fulfillment Agent uses request_inventory_help()
   → "Check stock for items in ORD-123 at warehouse"
   → Context: "Verifying stock before shipping"
3. Orchestrator routes to Inventory Agent
4. Inventory Agent returns: "All items in stock"
5. Fulfillment Agent proceeds with shipping
6. Fulfillment Agent uses request_payment_help()
   → "Verify payment status for ORD-123"
   → Context: "Confirming payment before shipment"
7. Payment Agent returns: "Payment confirmed"
8. Fulfillment Agent books shipment
```

### Scenario 3: Inventory Agent Checking Before Ordering

```
Request: "Order more units of SKU-123"

1. Inventory Agent analyzes need
2. Inventory Agent uses request_fulfillment_help()
   → "Check fulfillment demand for SKU-123"
   → Context: "Assessing if we need more stock"
3. Orchestrator routes to Fulfillment Agent
4. Fulfillment Agent returns: "High demand, 20 pending orders"
5. Inventory Agent uses request_loyalty_help()
   → "Get pricing info for SKU-123"
   → Context: "Cost analysis for procurement decision"
6. Loyalty Agent returns pricing
7. Inventory Agent places supplier order
```

---

## Best Practices

### ✅ DO:

1. **Use context parameter**
   - Always provide context about why you need help
   - Helps the receiving agent understand the request better

2. **Be specific in requests**
   - Clear, specific requests get better responses
   - Include relevant IDs, SKUs, order numbers

3. **Chain requests when needed**
   - One agent can make multiple requests
   - Use results from one request in the next

4. **Handle responses appropriately**
   - Parse and use response data
   - Extract needed information
   - Format for final output

### ❌ DON'T:

1. **Don't assume direct communication**
   - Always use communication tools
   - Never try to bypass Orchestrator

2. **Don't make unnecessary requests**
   - Only request help when you truly need it
   - Use your own tools when possible

3. **Don't ignore context**
   - Always provide context parameter
   - Helps with better routing and responses

---

## Implementation in Agents

### Adding Communication Tools to Your Agent

```python
import sys
import os

# Add orchestrator to path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, 'orchestrator'))

# Import communication tools
from inter_agent_communication import (
    request_inventory_help,
    request_fulfillment_help,
    request_payment_help,
    request_loyalty_help,
    request_support_help,
    request_agent_help
)

# Add to agent's tools list
agent_tools = [
    # ... your existing tools ...
    request_inventory_help,
    request_fulfillment_help,
    request_agent_help  # Generic interface
]
```

---

## Architecture Benefits

### Why This Design?

1. **Centralized Communication**
   - All requests flow through Orchestrator
   - Single point of control and monitoring

2. **Maintains Orchestrator-Centric Design**
   - Agents don't bypass Orchestrator
   - Consistent with system architecture

3. **Enables Agent Collaboration**
   - Agents can request help when needed
   - Enables complex multi-agent workflows

4. **Better Coordination**
   - Orchestrator can track all communications
   - Easier to debug and monitor

5. **Flexible and Extensible**
   - Easy to add new communication patterns
   - Can evolve without breaking existing code

---

## Troubleshooting

### Agent Not Finding Communication Tools?

1. **Check imports:**
   ```python
   # Make sure orchestrator path is added
   sys.path.insert(0, os.path.join(base_dir, 'orchestrator'))
   ```

2. **Verify tool availability:**
   ```python
   try:
       from inter_agent_communication import request_inventory_help
   except ImportError:
       print("Inter-agent communication not available")
   ```

### Communication Not Working?

1. **Check Orchestrator is accessible**
   - Verify orchestrator directory exists
   - Check routing tools are available

2. **Verify agent has tools**
   - Confirm tools are added to agent's tool list
   - Check tool import statements

3. **Review request format**
   - Ensure clear request descriptions
   - Include helpful context

---

## Summary

Inter-agent communication enables:
- ✅ Agents to request help from other agents
- ✅ All communication through Orchestrator
- ✅ Better coordination and collaboration
- ✅ Complex multi-agent workflows
- ✅ Maintained centralized architecture

**Remember:** All agent-to-agent communication flows through the Orchestrator - this maintains the system's architecture while enabling powerful agent collaboration! 🤝

