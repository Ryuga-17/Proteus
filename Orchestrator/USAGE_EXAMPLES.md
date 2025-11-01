# Orchestrator Usage Examples

## Quick Start

```python
from main import run_orchestrator, handle_custom_request
from orchestrator_tasks import task_inventory_management

# Run a predefined task
run_orchestrator(task_inventory_management, "Inventory Check")

# Or handle a custom request
handle_custom_request(
    "Check stock for SKU-123 at all locations and transfer 50 units from godown to store_main_street if needed"
)
```

## Example Scenarios

### 1. Inventory Management

```python
from orchestrator_tasks import task_inventory_management

run_orchestrator(task_inventory_management, "Nightly Inventory Optimization")
```

### 2. Order Fulfillment Workflow

```python
from orchestrator_tasks import task_order_fulfillment

run_orchestrator(task_order_fulfillment, "Process New Order")
```

### 3. Payment Processing

```python
from orchestrator_tasks import task_payment_processing

run_orchestrator(task_payment_processing, "Process Payment")
```

### 4. Customer Support Query

```python
from orchestrator_tasks import task_customer_support

run_orchestrator(task_customer_support, "Order Tracking")
```

### 5. Complete Checkout with Loyalty

```python
from orchestrator_tasks import task_checkout_with_loyalty

run_orchestrator(task_checkout_with_loyalty, "Full Checkout")
```

### 6. Return/Exchange

```python
from orchestrator_tasks import task_return_exchange

run_orchestrator(task_return_exchange, "Handle Return")
```

## Custom Request Examples

### Simple Inventory Check
```python
handle_custom_request(
    "Check stock levels for SKU 'RED-SHIRT-SML' at all store locations"
)
```

### Multi-Step Workflow
```python
handle_custom_request(
    """A customer wants to order SKU 'BLUE-JEANS-32':
    1. Check if it's in stock
    2. If yes, process payment of $49.99
    3. If payment succeeds, ship to: 123 Main St, City, State 12345
    4. Confirm the order completion"""
)
```

### Payment with Loyalty Points
```python
handle_custom_request(
    """Customer 'c123' wants to checkout with:
    - Items: ['prod-a', 'prod-b']
    - Coupon: 'SAVE20'
    - Use 500 loyalty points
    Calculate total and process payment."""
)
```

## Advanced: Direct Crew Creation

```python
from crewai import Crew, Process
from orchestrator_agent import orchestrator_agent
from orchestrator_tasks import create_custom_task

# Create a custom task
task = create_custom_task(
    description="Your custom request here",
    expected_output="Expected output description"
)

# Create and run the crew
crew = Crew(
    agents=[orchestrator_agent],
    tasks=[task],
    process=Process.sequential,
    memory=True,  # Enable memory for context
    verbose=2    # Set verbosity (0-2)
)

result = crew.kickoff()
print(result)
```

## Command Line Usage

```bash
# Run from the orchestrator directory
cd orchestrator
python main.py
```

This will run all example scenarios defined in `main.py`. Edit `scenarios_to_run` in `main.py` to run specific scenarios.

## Integration with Other Systems

### API Wrapper Example

```python
from main import handle_custom_request
import json

def process_customer_request(request_text: str) -> dict:
    """
    API endpoint wrapper for the orchestrator
    """
    try:
        result = handle_custom_request(request_text)
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Example usage
response = process_customer_request("Track my order ORD12345")
print(json.dumps(response, indent=2))
```

### Batch Processing

```python
from main import handle_custom_request

requests = [
    "Check stock for SKU-123",
    "Process payment for order ORD-456",
    "Track order ORD-789"
]

results = []
for req in requests:
    try:
        result = handle_custom_request(req)
        results.append({"request": req, "status": "success", "result": result})
    except Exception as e:
        results.append({"request": req, "status": "error", "error": str(e)})

for r in results:
    print(f"Request: {r['request']}")
    print(f"Status: {r['status']}")
    print()
```


