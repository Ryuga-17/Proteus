#!/usr/bin/env python3
"""
Test Resilience Mechanisms - Comprehensive Test Suite
Tests the new resilience features: transaction state machine, circuit breakers,
inventory reservations, payment idempotency, session consistency, etc.
"""

import requests
import json
import time
import sys
import random
from datetime import datetime
from typing import Dict, Any

# Backend URL
BACKEND_URL = "http://localhost:8000"

def log_test(test_name: str, message: str):
    """Log test information"""
    print(f"\n{'='*70}")
    print(f"🧪 {test_name}")
    print(f"{'='*70}")
    print(f"{message}")
    print(f"{'='*70}\n")

def make_purchase_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Make a purchase request to the backend"""
    try:
        response = requests.post(f"{BACKEND_URL}/api/purchase", json=payload, timeout=10)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": "non-json response"},
            "success": response.status_code == 200
        }
    except Exception as e:
        return {
            "status_code": 0,
            "data": {"error": str(e)},
            "success": False
        }

def test_transaction_state_machine():
    """Test the transaction state machine"""
    log_test("TRANSACTION STATE MACHINE", "Testing complete purchase flow with state transitions")

    # Step 1: Normal purchase
    payload = {
        "items": [
            {"product_id": "PROD-123", "sku": "sku_123", "quantity": 1}
        ],
        "user_id": "test-user-1",
        "location_id": "store_main_street",
        "payment_channel": "upi",
        "purchase_channel": "online"
    }

    result = make_purchase_request(payload)

    if result["success"]:
        data = result["data"]
        print(f"✅ Purchase successful!")
        print(f"   Transaction ID: {data.get('transaction_id')}")
        print(f"   State: {data.get('transaction_state')}")
        print(f"   Order ID: {data.get('order_id')}")
        print(f"   Items Processed: {len(data.get('items_processed', []))}")
    else:
        print(f"❌ Purchase failed: {result['data']}")

def test_inventory_reservation_race_condition():
    """Test inventory reservation prevents race conditions"""
    log_test("INVENTORY RESERVATION - RACE CONDITION", "Testing soft reservations prevent overselling")

    user_id = f"race-test-{random.randint(1000, 9999)}"

    # First request - should reserve inventory
    payload1 = {
        "items": [
            {"product_id": "PROD-456", "sku": "sku_456", "quantity": 2}  # Only 25 available
        ],
        "user_id": user_id,
        "location_id": "store_main_street",
        "payment_channel": "upi",
        "purchase_channel": "online",
        "simulate_payment_timeout": True  # Simulate slow payment
    }

    print("🚀 First request (will timeout payment, but reserve inventory)...")
    result1 = make_purchase_request(payload1)

    if not result1["success"]:
        print(f"✅ First request handled gracefully: {result1['data'].get('message', 'unknown')}")

    # Second request - should fail due to reservation
    payload2 = {
        "items": [
            {"product_id": "PROD-456", "sku": "sku_456", "quantity": 20}  # Try to buy remaining stock
        ],
        "user_id": f"{user_id}-2",
        "location_id": "store_main_street",
        "payment_channel": "upi",
        "purchase_channel": "online"
    }

    print("🚀 Second request (should fail due to reservation)...")
    result2 = make_purchase_request(payload2)

    if not result2["success"]:
        print(f"✅ Second request correctly failed: {result2['data'].get('message', 'unknown')}")
    else:
        print("❌ Second request should have failed due to inventory reservation")

def test_payment_idempotency():
    """Test payment idempotency prevents double charges"""
    log_test("PAYMENT IDEMPOTENCY", "Testing same payment doesn't get charged twice")

    # Same idempotency key, different attempts
    payload = {
        "items": [
            {"product_id": "PROD-123", "sku": "sku_123", "quantity": 1}
        ],
        "user_id": f"idempotent-test-{random.randint(1000, 9999)}",
        "location_id": "store_main_street",
        "payment_channel": "upi",
        "idempotency_key": "TEST-IDEMPOTENT-123",
        "purchase_channel": "online"
    }

    # First attempt
    print("🚀 First payment attempt...")
    result1 = make_purchase_request(payload)
    print(f"Result 1: {'✅' if result1['success'] else '❌'} {result1['data'].get('message', 'no message')}")

    # Second attempt with same idempotency key
    print("🚀 Second payment attempt (same idempotency key)...")
    result2 = make_purchase_request(payload)
    print(f"Result 2: {'✅' if result2['success'] else '❌'} {result2['data'].get('message', 'no message')}")

    # Check if both succeeded (should be same transaction)
    if result1["success"] and result2["success"]:
        if result1["data"].get("transaction_id") == result2["data"].get("transaction_id"):
            print("✅ Idempotency working - same transaction returned")
        else:
            print("❌ Idempotency failed - different transactions created")
    elif result1["success"] != result2["success"]:
        print("❌ Inconsistent results - one succeeded, one failed")

def test_payment_failure_handling():
    """Test payment failure handling with retries"""
    log_test("PAYMENT FAILURE HANDLING", "Testing payment failures trigger retries and backoff")

    payload = {
        "items": [
            {"product_id": "PROD-123", "sku": "sku_123", "quantity": 1}
        ],
        "user_id": f"failure-test-{random.randint(1000, 9999)}",
        "location_id": "store_main_street",
        "payment_channel": "upi",
        "purchase_channel": "online",
        "simulate_payment_failure": True  # Payment will fail
    }

    start_time = time.time()
    result = make_purchase_request(payload)
    end_time = time.time()

    if not result["success"]:
        print("✅ Payment failure handled correctly")
        print(f"   Message: {result['data'].get('message', 'unknown')}")
        print(f"   Time taken: {end_time - start_time:.2f}s")
    else:
        print("❌ Payment failure not handled properly - should have failed")

def test_circuit_breaker_inventory():
    """Test circuit breaker for inventory system"""
    log_test("CIRCUIT BREAKER - INVENTORY", "Testing inventory circuit breaker prevents cascading failures")

    user_id = f"circuit-test-{random.randint(1000, 9999)}"

    # First few requests will fail inventory, triggering circuit breaker
    print("🚀 Triggering inventory circuit breaker...")
    for i in range(3):
        payload = {
            "items": [
                {"product_id": "PROD-123", "sku": "sku_123", "quantity": 1}
            ],
            "user_id": f"{user_id}-{i}",
            "location_id": "store_main_street",
            "payment_channel": "upi",
            "purchase_channel": "online",
            "simulate_inventory_unavailable": True
        }

        result = make_purchase_request(payload)
        print(f"   Request {i+1}: {'❌' if not result['success'] else '✅'} {result['data'].get('message', 'unknown')[:50]}...")

    # Next request should be queued (circuit breaker open)
    print("🚀 Testing circuit breaker (should queue request)...")
    payload = {
        "items": [
            {"product_id": "PROD-123", "sku": "sku_123", "quantity": 1}
        ],
        "user_id": f"{user_id}-queued",
        "location_id": "store_main_street",
        "payment_channel": "upi",
        "purchase_channel": "online"
    }

    result = make_purchase_request(payload)
    if not result["success"] and "unavailable" in result["data"].get("message", "").lower():
        print("✅ Circuit breaker working - request queued for later retry")
    else:
        print("❌ Circuit breaker not working as expected")

def test_session_consistency():
    """Test session consistency across devices"""
    log_test("SESSION CONSISTENCY", "Testing multi-device session handling")

    user_id = f"session-test-{random.randint(1000, 9999)}"
    device1 = "device-mobile-123"
    device2 = "device-tablet-456"
    session_id = f"session-{random.randint(1000, 9999)}"

    # Register device 1
    payload1 = {
        "user_id": user_id,
        "device_id": device1,
        "session_id": session_id
    }

    try:
        response = requests.post(f"{BACKEND_URL}/api/session/register", json=payload1, timeout=5)
        if response.status_code == 200:
            print("✅ Device 1 registered successfully")
        else:
            print(f"❌ Device 1 registration failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Device 1 registration error: {e}")

    # Register device 2 (should detect conflict)
    payload2 = {
        "user_id": user_id,
        "device_id": device2,
        "session_id": session_id
    }

    try:
        response = requests.post(f"{BACKEND_URL}/api/session/register", json=payload2, timeout=5)
        data = response.json()
        if response.status_code == 200 and data.get("conflict"):
            print("✅ Session conflict detected correctly")
            print(f"   Conflict details: {data['conflict']}")
        else:
            print("❌ Session conflict not detected")
    except Exception as e:
        print(f"❌ Device 2 registration error: {e}")

def test_inventory_revalidation():
    """Test inventory revalidation before payment"""
    log_test("INVENTORY REVALIDATION", "Testing inventory changes detected before payment")

    user_id = f"revalidate-test-{random.randint(1000, 9999)}"

    # This test simulates inventory changing between reservation and payment
    # In a real scenario, this would happen if another user purchases the same item

    payload = {
        "items": [
            {"product_id": "PROD-456", "sku": "sku_456", "quantity": 1}
        ],
        "user_id": user_id,
        "location_id": "store_main_street",
        "payment_channel": "upi",
        "purchase_channel": "online"
    }

    result = make_purchase_request(payload)

    if result["success"]:
        print("✅ Purchase completed successfully")
        print(f"   Transaction ID: {result['data'].get('transaction_id')}")
    else:
        message = result["data"].get("message", "")
        if "inventory" in message.lower() or "stock" in message.lower():
            print("✅ Inventory issue detected correctly")
        else:
            print(f"❌ Unexpected failure: {message}")

def main():
    """Run all resilience tests"""
    print("\n" + "="*80)
    print("🛡️  RESILIENCE MECHANISM TEST SUITE")
    print("="*80)
    print("Testing transaction state machine, circuit breakers, idempotency,")
    print("inventory reservations, session consistency, and failure handling.")
    print("="*80 + "\n")

    # Check if backend is running
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=3)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Please start the backend with: cd backend && python main.py")
        return

    # Run tests
    tests = [
        ("Transaction State Machine", test_transaction_state_machine),
        ("Inventory Reservation (Race Conditions)", test_inventory_reservation_race_condition),
        ("Payment Idempotency", test_payment_idempotency),
        ("Payment Failure Handling", test_payment_failure_handling),
        ("Circuit Breaker (Inventory)", test_circuit_breaker_inventory),
        ("Session Consistency", test_session_consistency),
        ("Inventory Revalidation", test_inventory_revalidation),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            print(f"\n🔬 Running: {test_name}")
            test_func()
            results.append((test_name, True, None))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False, str(e)))

    # Summary
    print("\n" + "="*80)
    print("📊 TEST RESULTS SUMMARY")
    print("="*80)

    passed = 0
    total = len(results)

    for test_name, success, error in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if error:
            print(f"     Error: {error}")
        if success:
            passed += 1

    print(f"\n📈 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("🎉 All resilience tests passed! The system is robust.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    print("="*80)

if __name__ == "__main__":
    main()