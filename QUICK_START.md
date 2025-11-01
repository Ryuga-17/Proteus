# Quick Start Guide - Using the Orchestrator 🚀

## The Golden Rule

**🎯 ALL requests go through the Orchestrator Agent!**

The Orchestrator is your single entry point to access all agents. Don't call agents directly - always use the Orchestrator.

---

## How to Use the System

### Method 1: Using the Orchestrator (Recommended)

```python
from orchestrator.main import handle_custom_request

# Just describe what you need in plain English!
result = handle_custom_request("Check stock for red shirts size small")
print(result)
```

### Method 2: Pre-built Scenarios

```python
from orchestrator.main import run_example_scenarios

# Run all example scenarios
run_example_scenarios()

# Or run specific scenarios
from orchestrator.orchestrator_tasks import task_inventory_management
from orchestrator.main import run_orchestrator

run_orchestrator(task_inventory_management, "Inventory Check")
```

### Method 3: Direct Orchestrator Access

```python
from crewai import Crew, Process
from orchestrator.orchestrator_agent import orchestrator_agent
from orchestrator.orchestrator_tasks import create_custom_task

# Create a custom task
task = create_custom_task(
    "Process a complete order: check stock, calculate price, process payment, and ship"
)

# Create orchestrator crew
crew = Crew(
    agents=[orchestrator_agent],
    tasks=[task],
    process=Process.sequential,
    memory=True,
    verbose=2
)

result = crew.kickoff()
print(result)
```

---

## Example Requests

All of these go through the Orchestrator:

### Inventory Requests
```python
handle_custom_request("Check stock for SKU-123 at all locations")
handle_custom_request("Transfer 50 units from godown to store_main_street")
handle_custom_request("Order 100 more units of widget-X from supplier")
```

### Fulfillment Requests
```python
handle_custom_request("Ship order ORD-123 to 123 Main St, City, State")
handle_custom_request("Reserve item SKU-456 for customer C-789 at store S-102")
```

### Payment Requests
```python
handle_custom_request("Process $150 payment for customer cust-789 using credit card")
handle_custom_request("Generate kiosk-to-mobile handoff for customer at kiosk session kiosk-A9")
```

### Loyalty/Pricing Requests
```python
handle_custom_request("Calculate final price for cart ['prod-a', 'prod-b'] with coupon SAVE20")
handle_custom_request("Apply 500 loyalty points to order total of $50")
```

### Support Requests
```python
handle_custom_request("Track order ORD12345 and show current location")
handle_custom_request("Process return for damaged item from order ORD56789")
```

---

## Multi-Agent Workflows

The Orchestrator can coordinate multiple agents automatically:

```python
# This single request uses multiple agents!
handle_custom_request(
    "Customer wants to order 2 red shirts. "
    "Check if in stock, calculate price with coupon SAVE20, "
    "process payment, and ship to their address"
)

# Orchestrator will:
# 1. Check inventory (Inventory Agent)
# 2. Calculate price (Loyalty Agent)  
# 3. Process payment (Payment Agent)
# 4. Ship order (Fulfillment Agent)
# 5. Combine all results into one response
```

---

## Command Line Usage

```bash
# Navigate to orchestrator directory
cd orchestrator

# Run example scenarios
python main.py
```

---

## Key Points

✅ **Always use Orchestrator** - It routes to the right agents  
✅ **Describe requests clearly** - Plain English works best  
✅ **Let Orchestrator coordinate** - It handles multi-agent workflows  
✅ **Responses are unified** - Orchestrator formats everything consistently  

---

## What NOT to Do

❌ Don't call agents directly:
```python
# ❌ WRONG - Bypasses orchestrator
from inventory_agent.main import run_crew
run_crew()
```

✅ Do use Orchestrator:
```python
# ✅ CORRECT - Goes through orchestrator
handle_custom_request("Run inventory optimization")
```

---

## Need Help?

- Check `SYSTEM_EXPLANATION.md` for detailed architecture
- Check `AGENT_INTEGRATION_GUIDE.md` for agent integration details
- Check `orchestrator/README.md` for orchestrator-specific docs

---

**Remember: Orchestrator = Single Entry Point to All Agents! 🎯**

