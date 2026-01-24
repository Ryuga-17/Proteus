"""
Test script for Session-Based Authentication with Step-Up Authentication
"""
import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
# Try both possible endpoint paths
WHATSAPP_ENDPOINT = f"{BASE_URL}/whatsapp/simulate/message"
WHATSAPP_ENDPOINT_ALT = f"{BASE_URL}/simulate/message"

# Test phone numbers
TEST_PHONE = "+918850833367"
TEST_PHONE_2 = "+919876543210"


def send_message(phone: str, message: str) -> Dict[str, Any]:
    """Send a simulated WhatsApp message"""
    payload = {
        "sender_id": f"whatsapp:{phone}",
        "message_text": message
    }
    
    print(f"\n📤 Sending: {message}")
    print(f"   From: {phone}")
    
    try:
        # Try primary endpoint first
        try:
            response = requests.post(WHATSAPP_ENDPOINT, json=payload, timeout=5)
            response.raise_for_status()
            result = response.json()
            
            print(f"📥 Response: {result.get('response_text', result.get('message', 'No response'))[:200]}")
            return result
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # Try alternate endpoint
                print(f"   ⚠️  Primary endpoint not found, trying alternate...")
                response = requests.post(WHATSAPP_ENDPOINT_ALT, json=payload, timeout=5)
                response.raise_for_status()
                result = response.json()
                
                print(f"📥 Response: {result.get('response_text', result.get('message', 'No response'))[:200]}")
                return result
            else:
                raise
    except Exception as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status: {e.response.status_code}")
            print(f"   Response: {e.response.text[:200]}")
        return {}


def test_scenario(name: str, steps: list):
    """Run a test scenario"""
    print(f"\n{'='*70}")
    print(f"🧪 TEST SCENARIO: {name}")
    print(f"{'='*70}")
    
    for i, step in enumerate(steps, 1):
        print(f"\n--- Step {i} ---")
        send_message(step['phone'], step['message'])
        if step.get('wait'):
            time.sleep(step['wait'])


def main():
    """Run all test scenarios"""
    print("🚀 Starting Session-Based Authentication Tests")
    print(f"Backend URL: {BASE_URL}")
    print(f"Make sure the backend is running on port 8000!")
    
    # Test 1: First-Time Login
    test_scenario("First-Time User Login", [
        {"phone": TEST_PHONE, "message": "Hi", "wait": 1},
        {"phone": TEST_PHONE, "message": "+918850833367", "wait": 1},
        {"phone": TEST_PHONE, "message": "123456", "wait": 1},  # OTP (check logs for actual OTP)
    ])
    
    # Test 2: Returning User (Welcome Back)
    test_scenario("Returning User - Welcome Back", [
        {"phone": TEST_PHONE, "message": "Hi", "wait": 1},
    ])
    
    # Test 3: Low-Risk Action (No Step-Up)
    test_scenario("Low-Risk Action - Browse Products", [
        {"phone": TEST_PHONE, "message": "Show me products", "wait": 2},
        {"phone": TEST_PHONE, "message": "What are my loyalty points?", "wait": 2},
        {"phone": TEST_PHONE, "message": "Check inventory for item ABC123", "wait": 2},
    ])
    
    # Test 4: High-Risk Action - Payment (Step-Up Required)
    test_scenario("High-Risk Action - Payment (Step-Up)", [
        {"phone": TEST_PHONE, "message": "I want to pay ₹15,000", "wait": 2},
        {"phone": TEST_PHONE, "message": "YES", "wait": 1},
        {"phone": TEST_PHONE, "message": "654321", "wait": 1},  # Step-up OTP (check logs)
    ])
    
    # Test 5: High-Risk Action - Refund
    test_scenario("High-Risk Action - Refund", [
        {"phone": TEST_PHONE, "message": "I want a refund for order 12345", "wait": 2},
        {"phone": TEST_PHONE, "message": "YES", "wait": 1},
        {"phone": TEST_PHONE, "message": "789012", "wait": 1},  # Step-up OTP
    ])
    
    # Test 6: Address Change
    test_scenario("High-Risk Action - Address Change", [
        {"phone": TEST_PHONE, "message": "Change my delivery address", "wait": 2},
        {"phone": TEST_PHONE, "message": "YES", "wait": 1},
        {"phone": TEST_PHONE, "message": "345678", "wait": 1},  # Step-up OTP
    ])
    
    # Test 7: Low-Value Payment (No OTP, Just Confirmation)
    test_scenario("Low-Value Payment (Confirmation Only)", [
        {"phone": TEST_PHONE, "message": "I want to pay ₹500", "wait": 2},
        {"phone": TEST_PHONE, "message": "YES", "wait": 1},
    ])
    
    # Test 8: Cancel Step-Up
    test_scenario("Cancel Step-Up Flow", [
        {"phone": TEST_PHONE, "message": "I want to pay ₹20,000", "wait": 2},
        {"phone": TEST_PHONE, "message": "NO", "wait": 1},
    ])
    
    # Test 9: Logout
    test_scenario("Logout", [
        {"phone": TEST_PHONE, "message": "logout", "wait": 1},
        {"phone": TEST_PHONE, "message": "Hi", "wait": 1},  # Should ask for phone again
    ])
    
    # Test 10: Second User (Different Phone)
    test_scenario("Second User - First-Time Login", [
        {"phone": TEST_PHONE_2, "message": "Hi", "wait": 1},
        {"phone": TEST_PHONE_2, "message": "+919876543210", "wait": 1},
        {"phone": TEST_PHONE_2, "message": "111222", "wait": 1},  # OTP
    ])
    
    print(f"\n{'='*70}")
    print("✅ All test scenarios completed!")
    print(f"{'='*70}")
    print("\n📝 Note: Check the backend logs for actual OTP codes")
    print("   OTPs are displayed in DEV MODE in the response messages")


if __name__ == "__main__":
    main()
