"""
Basic Functionality Test
Tests that all agents can be accessed through Orchestrator
"""
from Orchestrator.main import handle_custom_request

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

