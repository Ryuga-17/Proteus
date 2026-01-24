"""
Direct test of WhatsApp integration (without HTTP endpoint)
Use this if the HTTP endpoint isn't working
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from whatsapp_integration.models import WhatsAppMessage
from whatsapp_integration.message_handler import message_handler

def test_scenario(name, steps):
    """Test a scenario"""
    print(f"\n{'='*70}")
    print(f"🧪 TEST: {name}")
    print(f"{'='*70}")
    
    for i, (message_text, description) in enumerate(steps, 1):
        print(f"\n--- Step {i}: {description} ---")
        print(f"📤 Sending: {message_text}")
        
        message = WhatsAppMessage(
            sender_id="whatsapp:+918850833367",
            message_text=message_text
        )
        
        response = message_handler.handle_message(message)
        print(f"📥 Response: {response.message_text[:300]}")
        
        # Check if OTP is in response (for manual entry)
        if "[DEV MODE] Your OTP:" in response.message_text:
            otp_line = [line for line in response.message_text.split('\n') if 'OTP:' in line]
            if otp_line:
                print(f"🔑 {otp_line[0]}")

def main():
    print("🚀 Direct WhatsApp Integration Test")
    print("This tests the integration directly without HTTP endpoints\n")
    
    # Test 1: First-time login
    test_scenario("First-Time Login", [
        ("Hi", "Initial greeting"),
        ("+918850833367", "Enter phone number"),
        ("123456", "Enter OTP (check response above for actual OTP)"),
    ])
    
    # Test 2: Returning user
    test_scenario("Returning User", [
        ("Hi", "Greeting with valid session"),
    ])
    
    # Test 3: Low-risk action
    test_scenario("Low-Risk Action", [
        ("Show me products", "Browse products"),
    ])
    
    # Test 4: High-risk action
    test_scenario("High-Risk Action - Payment", [
        ("I want to pay ₹15,000", "Request payment"),
        ("YES", "Confirm action"),
        ("654321", "Enter step-up OTP (check response above)"),
    ])
    
    # Test 5: Logout
    test_scenario("Logout", [
        ("logout", "Logout command"),
        ("Hi", "Try to use system after logout"),
    ])
    
    print(f"\n{'='*70}")
    print("✅ All tests completed!")
    print(f"{'='*70}")
    print("\n💡 Tip: Check the responses above for OTP codes in DEV MODE")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
