"""
Inter-Agent Communication Test
Tests that agents can request help from each other through Orchestrator
"""
import sys
import os

# Add Orchestrator to path
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(base_dir, 'Orchestrator'))

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

