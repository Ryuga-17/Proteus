# Testing Guide - How to Test Your Agent System 🧪

## Quick Start Testing

### Method 1: Test Through Orchestrator (Recommended)

```python
# Navigate to orchestrator directory
cd orchestrator

# Run the main script
python main.py
```

This will show you a menu to:
- Run example scenarios
- Handle custom requests
- Test different agents

---

## Testing Methods

### 1. Simple Custom Request Test

```python
from orchestrator.main import handle_custom_request

# Test a simple request
result = handle_custom_request("Check stock for SKU-123")
print(result)
```

**Test Cases:**
```python
# Inventory Tests
handle_custom_request("Check stock for red shirts size small")
handle_custom_request("Transfer 50 units from warehouse to store_main")
handle_custom_request("Order 100 more units of widget-X from supplier")

# Fulfillment Tests
handle_custom_request("Ship order ORD-123 to 123 Main St, City, State")
handle_custom_request("Reserve item SKU-456 for customer C-789 at store S-102")

# Payment Tests
handle_custom_request("Process $150 payment for customer cust-789 using credit card")
handle_custom_request("Generate kiosk-to-mobile handoff for customer at kiosk-A9")

# Loyalty Tests
handle_custom_request("Calculate price for cart ['prod-a', 'prod-b'] with coupon SAVE20")
handle_custom_request("Apply 500 loyalty points to order total of $50")

# Support Tests
handle_custom_request("Track order ORD12345 and show current location")
handle_custom_request("Process return for damaged item from order ORD56789")
```

---

### 2. Multi-Agent Workflow Tests

```python
from orchestrator.main import handle_custom_request

# Test complex workflows that need multiple agents
complex_requests = [
    # Complete order processing
    "Order 2 red shirts, check stock, calculate price with coupon SAVE20, process payment, and ship",
    
    # Exchange scenario
    "Customer wants to exchange damaged item SKU-123. Check inventory for replacement, process exchange, and ship new item",
    
    # Full checkout flow
    "Checkout: Check stock for SKU-123, calculate final price with coupon and loyalty points, process payment, ship order",
]
```

---

### 3. Test Individual Agents (For Development)

```python
# Test Inventory Agent directly
from Inventory agent.main import run_crew
run_crew()

# Test Fulfillment Agent directly
from Fullfillment_agent.main import *
# Run the scenarios in main.py

# Test Payment Agent directly
from payment_agent.main import *
# Run the scenarios in main.py

# Test Support Agent directly
from post purchase support agent.main import *
# Run the scenarios in main.py
```

---

### 4. Test Inter-Agent Communication

Create a test script to verify agents can communicate:

```python
# test_inter_agent_comm.py
import sys
import os

# Add orchestrator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'orchestrator'))

from inter_agent_communication import (
    request_inventory_help,
    request_fulfillment_help,
    request_payment_help,
    request_support_help
)

# Test Support Agent requesting Inventory help
print("Testing: Support Agent → Inventory Agent")
result = request_inventory_help(
    "Check stock for SKU-123 at all locations",
    "Testing inter-agent communication"
)
print(f"Result: {result}\n")

# Test Fulfillment Agent requesting Inventory help
print("Testing: Fulfillment Agent → Inventory Agent")
result = request_inventory_help(
    "Check stock for items in order ORD-123",
    "Verifying stock before shipping"
)
print(f"Result: {result}\n")

# Test Inventory Agent requesting Fulfillment help
print("Testing: Inventory Agent → Fulfillment Agent")
result = request_fulfillment_help(
    "Get fulfillment status for SKU-123",
    "Checking demand before ordering more stock"
)
print(f"Result: {result}\n")
```

---

## Test Scripts

### Script 1: Basic Functionality Test

Create `test_basic_functionality.py`:

```python
"""
Basic Functionality Test
Tests that all agents can be accessed through Orchestrator
"""
from orchestrator.main import handle_custom_request

def test_inventory():
    print("=" * 60)
    print("TEST 1: Inventory Agent")
    print("=" * 60)
    result = handle_custom_request("Check stock for SKU-123")
    print(result)
    print()

def test_fulfillment():
    print("=" * 60)
    print("TEST 2: Fulfillment Agent")
    print("=" * 60)
    result = handle_custom_request("Ship order ORD-123 to customer address")
    print(result)
    print()

def test_payment():
    print("=" * 60)
    print("TEST 3: Payment Agent")
    print("=" * 60)
    result = handle_custom_request("Process $150 payment for customer")
    print(result)
    print()

def test_loyalty():
    print("=" * 60)
    print("TEST 4: Loyalty Agent")
    print("=" * 60)
    result = handle_custom_request("Calculate price with coupon SAVE20")
    print(result)
    print()

def test_support():
    print("=" * 60)
    print("TEST 5: Support Agent")
    print("=" * 60)
    result = handle_custom_request("Track order ORD-12345")
    print(result)
    print()

if __name__ == "__main__":
    print("\n🧪 RUNNING BASIC FUNCTIONALITY TESTS\n")
    test_inventory()
    test_fulfillment()
    test_payment()
    test_loyalty()
    test_support()
    print("✅ All basic tests completed!")
```

---

### Script 2: Multi-Agent Workflow Test

Create `test_multi_agent_workflows.py`:

```python
"""
Multi-Agent Workflow Test
Tests that Orchestrator can coordinate multiple agents
"""
from orchestrator.main import handle_custom_request

def test_complete_order():
    print("=" * 60)
    print("TEST: Complete Order Processing (Multiple Agents)")
    print("=" * 60)
    result = handle_custom_request(
        "Customer wants to order 2 red shirts. "
        "Check if in stock, calculate price with coupon SAVE20, "
        "process payment, and ship to their address"
    )
    print(result)
    print()

def test_exchange_scenario():
    print("=" * 60)
    print("TEST: Exchange Scenario (Multiple Agents)")
    print("=" * 60)
    result = handle_custom_request(
        "Customer received damaged item SKU-123 from order ORD-456. "
        "Check if replacement is available in inventory, "
        "process the exchange, and ship the replacement"
    )
    print(result)
    print()

def test_checkout_with_pricing():
    print("=" * 60)
    print("TEST: Checkout with Pricing (Loyalty + Payment)")
    print("=" * 60)
    result = handle_custom_request(
        "Customer wants to checkout. Order total is $50. "
        "Apply coupon SAVE20 and 500 loyalty points. "
        "Calculate final price and process payment"
    )
    print(result)
    print()

if __name__ == "__main__":
    print("\n🧪 RUNNING MULTI-AGENT WORKFLOW TESTS\n")
    test_complete_order()
    test_exchange_scenario()
    test_checkout_with_pricing()
    print("✅ All multi-agent tests completed!")
```

---

### Script 3: Inter-Agent Communication Test

Create `test_inter_agent_communication.py`:

```python
"""
Inter-Agent Communication Test
Tests that agents can request help from each other through Orchestrator
"""
import sys
import os

# Add orchestrator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'orchestrator'))

from inter_agent_communication import (
    request_inventory_help,
    request_fulfillment_help,
    request_payment_help,
    request_support_help,
    request_agent_help
)

def test_support_to_inventory():
    """Test Support Agent requesting Inventory Agent"""
    print("=" * 60)
    print("TEST: Support Agent → Inventory Agent")
    print("=" * 60)
    result = request_inventory_help(
        "Check stock for SKU-123 at all locations",
        "Customer wants exchange, need replacement availability"
    )
    print(result)
    print()

def test_fulfillment_to_inventory():
    """Test Fulfillment Agent requesting Inventory Agent"""
    print("=" * 60)
    print("TEST: Fulfillment Agent → Inventory Agent")
    print("=" * 60)
    result = request_inventory_help(
        "Check stock for items in order ORD-123",
        "Verifying availability before shipping"
    )
    print(result)
    print()

def test_fulfillment_to_payment():
    """Test Fulfillment Agent requesting Payment Agent"""
    print("=" * 60)
    print("TEST: Fulfillment Agent → Payment Agent")
    print("=" * 60)
    result = request_payment_help(
        "Verify payment status for order ORD-123",
        "Confirming payment before shipping"
    )
    print(result)
    print()

def test_inventory_to_fulfillment():
    """Test Inventory Agent requesting Fulfillment Agent"""
    print("=" * 60)
    print("TEST: Inventory Agent → Fulfillment Agent")
    print("=" * 60)
    result = request_fulfillment_help(
        "Get fulfillment demand for SKU-123",
        "Assessing demand before placing supplier order"
    )
    print(result)
    print()

def test_generic_agent_help():
    """Test generic agent help request"""
    print("=" * 60)
    print("TEST: Generic Agent Help (Dynamic Routing)")
    print("=" * 60)
    result = request_agent_help(
        "inventory",
        "Check stock for SKU-123",
        "Generic request test"
    )
    print(result)
    print()

if __name__ == "__main__":
    print("\n🧪 RUNNING INTER-AGENT COMMUNICATION TESTS\n")
    test_support_to_inventory()
    test_fulfillment_to_inventory()
    test_fulfillment_to_payment()
    test_inventory_to_fulfillment()
    test_generic_agent_help()
    print("✅ All inter-agent communication tests completed!")
```

---

### Script 4: Comprehensive System Test

Create `test_comprehensive_system.py`:

```python
"""
Comprehensive System Test
Tests the entire system end-to-end
"""
from orchestrator.main import handle_custom_request

# Test scenarios covering all aspects
test_scenarios = [
    # Single agent scenarios
    ("Inventory Check", "Check stock for SKU-123 at all locations"),
    ("Fulfillment Shipping", "Ship order ORD-123 to customer address"),
    ("Payment Processing", "Process $150 payment for customer C-456"),
    ("Loyalty Pricing", "Calculate price with coupon SAVE20 for order"),
    ("Support Tracking", "Track order ORD-12345"),
    
    # Multi-agent scenarios
    ("Stock Then Ship", "Check stock for SKU-123, then ship if available"),
    ("Price Then Pay", "Calculate final price with discounts, then process payment"),
    ("Complete Order", "Order 2 items: check stock, calculate price, process payment, ship"),
    
    # Complex workflows
    ("Return & Replace", "Customer returning damaged item. Process return, check inventory for replacement, ship new item"),
    ("Exchange Flow", "Exchange item: verify inventory, process exchange, calculate price difference, ship replacement"),
]

def run_comprehensive_test():
    print("\n" + "=" * 60)
    print("COMPREHENSIVE SYSTEM TEST")
    print("=" * 60 + "\n")
    
    passed = 0
    failed = 0
    
    for test_name, request in test_scenarios:
        print(f"\n{'='*60}")
        print(f"Test: {test_name}")
        print(f"Request: {request}")
        print('='*60)
        
        try:
            result = handle_custom_request(request)
            print(f"✅ PASSED - Result received")
            print(f"Result preview: {str(result)[:200]}...")
            passed += 1
        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            failed += 1
        
        print()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {passed + failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_comprehensive_test()
```

---

## Running Tests

### Option 1: Run Individual Test Scripts

```bash
# Navigate to project root
cd "/Users/viveksawant/Desktop/Sales Agent"

# Run basic functionality test
python test_basic_functionality.py

# Run multi-agent workflow test
python test_multi_agent_workflows.py

# Run inter-agent communication test
python test_inter_agent_communication.py

# Run comprehensive test
python test_comprehensive_system.py
```

### Option 2: Use Orchestrator Main Menu

```bash
cd orchestrator
python main.py

# Then select from menu:
# 1. Run example scenarios
# 2. Handle custom request
```

### Option 3: Interactive Python Testing

```python
# Start Python REPL
python

# Import and test
from orchestrator.main import handle_custom_request

# Test requests
handle_custom_request("Check stock for SKU-123")
handle_custom_request("Ship order ORD-123")
# ... etc
```

---

## Testing Checklist

### ✅ Basic Functionality
- [ ] Inventory Agent responds to stock requests
- [ ] Fulfillment Agent processes shipping requests
- [ ] Payment Agent processes payment requests
- [ ] Loyalty Agent calculates prices
- [ ] Support Agent handles tracking requests

### ✅ Orchestrator Routing
- [ ] Orchestrator correctly identifies intent
- [ ] Orchestrator routes to correct agent
- [ ] Responses flow back through Orchestrator
- [ ] Orchestrator formats responses correctly

### ✅ Multi-Agent Workflows
- [ ] Orchestrator coordinates multiple agents
- [ ] Sequential agent calls work (Inventory → Fulfillment)
- [ ] Results are synthesized correctly
- [ ] Complex workflows complete successfully

### ✅ Inter-Agent Communication
- [ ] Support Agent can request Inventory help
- [ ] Fulfillment Agent can request Inventory help
- [ ] Fulfillment Agent can request Payment help
- [ ] Inventory Agent can request Fulfillment help
- [ ] All communication flows through Orchestrator

### ✅ Error Handling
- [ ] Invalid requests are handled gracefully
- [ ] Missing agents show helpful error messages
- [ ] Network/API errors are caught
- [ ] System continues after errors

---

## Test Scenarios by Category

### Inventory Tests
```python
# Stock checks
"Check stock for SKU-123"
"Check stock for SKU-123 at warehouse_1"
"Check stock levels across all locations"

# Transfers
"Transfer 50 units of SKU-123 from warehouse to store_main"
"Move stock between locations"

# Procurement
"Order 100 more units of SKU-123 from supplier"
"Place procurement order for widget-X"
```

### Fulfillment Tests
```python
# Shipping
"Ship order ORD-123 to customer address 123 Main St"
"Process shipment for order ORD-456"

# Reservations
"Reserve item SKU-123 for customer C-456 at store S-102"
"Hold product for in-store pickup"
```

### Payment Tests
```python
# Standard payment
"Process $150 payment for customer C-456 using credit card"
"Charge customer for order ORD-123"

# Kiosk-to-mobile
"Generate kiosk-to-mobile payment handoff"

# Loyalty points
"Process payment using 500 loyalty points"
```

### Loyalty Tests
```python
# Pricing
"Calculate price for order with items A, B, C"
"Apply coupon SAVE20 to order"

# Points
"Check loyalty point balance for customer"
"Apply 500 loyalty points to order"
```

### Support Tests
```python
# Tracking
"Track order ORD-12345"
"Where is my order?"

# Returns
"Process return for order ORD-123"
"Handle damaged item return"

# Exchanges
"Exchange item SKU-123 for different size"
```

---

## Debugging Tips

### 1. Enable Verbose Mode

Most agents have `verbose=True` which shows detailed output.

### 2. Check API Keys

Make sure your OpenAI API key is set:
```python
import os
os.environ["OPENAI_API_KEY"] = "your-key-here"
```

### 3. Test Individual Components

```python
# Test routing tools directly
from orchestrator.orchestrator_tools import route_to_inventory
result = route_to_inventory("Check stock for SKU-123")
print(result)
```

### 4. Check Import Paths

If you get import errors, verify paths:
```python
import sys
print(sys.path)  # Should include orchestrator directory
```

### 5. Use Mock LLMs for Testing

Some agents use MockLLM for testing without API keys. Check agent files.

---

## Performance Testing

```python
import time

def performance_test():
    """Test response times"""
    requests = [
        "Check stock for SKU-123",
        "Ship order ORD-123",
        "Process $150 payment",
    ]
    
    for request in requests:
        start = time.time()
        result = handle_custom_request(request)
        elapsed = time.time() - start
        print(f"{request}: {elapsed:.2f}s")
```

---

## Quick Test Command

```bash
# Quick test all agents
python -c "
from orchestrator.main import handle_custom_request
print('Testing Inventory:', handle_custom_request('Check stock for SKU-123'))
print('Testing Fulfillment:', handle_custom_request('Ship order ORD-123'))
print('Testing Payment:', handle_custom_request('Process $150 payment'))
print('Testing Loyalty:', handle_custom_request('Calculate price with coupon'))
print('Testing Support:', handle_custom_request('Track order ORD-12345'))
"
```

---

## Next Steps

1. **Start with basic tests** - Test each agent individually
2. **Test orchestrator routing** - Verify correct agent selection
3. **Test multi-agent workflows** - Complex scenarios
4. **Test inter-agent communication** - Agent-to-agent requests
5. **Run comprehensive test** - Full system test

Happy Testing! 🧪✨

