"""
Test script for WhatsApp integration
Simulates a complete authentication flow and message routing
"""
import requests
import time
import json

BASE_URL = "http://localhost:8000/whatsapp"


def test_whatsapp_integration():
    """Test complete WhatsApp integration flow"""
    
    print("=" * 70)
    print("🧪 Testing WhatsApp Integration")
    print("=" * 70)
    print()
    
    sender_id = "+1234567890"
    
    # Test 1: Start conversation
    print("📱 Test 1: Starting conversation with 'Hi'")
    print("-" * 70)
    response = requests.post(
        f"{BASE_URL}/simulate/message",
        json={
            "sender_id": sender_id,
            "message_text": "Hi"
        }
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result.get('response_text', '')}")
    print()
    time.sleep(1)
    
    # Test 2: Enter phone number
    print("📱 Test 2: Entering phone number")
    print("-" * 70)
    response = requests.post(
        f"{BASE_URL}/simulate/message",
        json={
            "sender_id": sender_id,
            "message_text": "+1234567890"
        }
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result.get('response_text', '')}")
    print()
    
    # Extract OTP from response (dev mode only)
    response_text = result.get('response_text', '')
    if '[DEV MODE] Your OTP:' in response_text:
        otp = response_text.split('[DEV MODE] Your OTP:')[1].strip().split('\n')[0]
        print(f"🔑 Extracted OTP: {otp}")
        print()
        time.sleep(1)
        
        # Test 3: Verify OTP
        print("📱 Test 3: Verifying OTP")
        print("-" * 70)
        response = requests.post(
            f"{BASE_URL}/simulate/message",
            json={
                "sender_id": sender_id,
                "message_text": otp
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result.get('response_text', '')}")
        print()
        time.sleep(1)
        
        # Test 4: Send authenticated message
        print("📱 Test 4: Sending authenticated message (product query)")
        print("-" * 70)
        response = requests.post(
            f"{BASE_URL}/simulate/message",
            json={
                "sender_id": sender_id,
                "message_text": "Show me red shirts"
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result.get('response_text', '')[:200]}...")  # Truncate for display
        print()
    else:
        print("⚠️  Could not extract OTP from response")
        print("   (This is expected if not in development mode)")
        print()
    
    # Test 5: Health check
    print("📱 Test 5: Health check")
    print("-" * 70)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    print("=" * 70)
    print("✅ Testing complete!")
    print("=" * 70)


if __name__ == "__main__":
    print("Make sure the backend server is running on http://localhost:8000")
    print("Press Enter to start tests...")
    input()
    
    try:
        test_whatsapp_integration()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to backend server.")
        print("   Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
