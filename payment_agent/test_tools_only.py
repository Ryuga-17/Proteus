#!/usr/bin/env python3
"""
Test script focused on just the payment tools.
This helps isolate tool functionality from agent complexity.
"""

import json

def test_tools_directly():
    """Test the payment tools directly without agents"""
    print("🔧 TESTING PAYMENT TOOLS DIRECTLY")
    print("="*50)
    
    try:
        from tools import PaymentTools
        print("✅ PaymentTools imported successfully")
    except Exception as e:
        print(f"❌ PaymentTools import failed: {e}")
        return False
    
    # Test 1: Standard payment success
    print("\n1. Testing standard payment (success case):")
    try:
        result = PaymentTools.process_standard_payment(
            customer_id="test-customer-123",
            amount=50.00,
            payment_method="credit_card",
            details={"card_number": "1234-5678-9012-3456"}
        )
        print(f"   Result: {result}")
        
        # Verify it's valid JSON
        parsed = json.loads(result)
        if "status" in parsed:
            print("   ✅ Valid JSON response with status field")
        else:
            print("   ❌ Invalid JSON response")
            return False
            
    except Exception as e:
        print(f"   ❌ Tool execution failed: {e}")
        return False
    
    # Test 2: Standard payment failure
    print("\n2. Testing standard payment (failure case):")
    try:
        result = PaymentTools.process_standard_payment(
            customer_id="test-customer-456",
            amount=100.00,
            payment_method="credit_card",
            details={"card_number": "fail-1234"}
        )
        print(f"   Result: {result}")
        
        # Verify it's valid JSON
        parsed = json.loads(result)
        if parsed.get("status") == "failed":
            print("   ✅ Correctly returned failure status")
        else:
            print("   ❌ Expected failure status")
            return False
            
    except Exception as e:
        print(f"   ❌ Tool execution failed: {e}")
        return False
    
    # Test 3: Kiosk handoff
    print("\n3. Testing kiosk-to-mobile handoff:")
    try:
        result = PaymentTools.generate_kiosk_to_mobile_handoff(
            customer_id="test-customer-789",
            amount=75.50,
            session_id="kiosk-test-001"
        )
        print(f"   Result: {result}")
        
        # Verify it's valid JSON
        parsed = json.loads(result)
        if "payment_url_for_qr_code" in parsed:
            print("   ✅ Valid handoff response with QR URL")
        else:
            print("   ❌ Invalid handoff response")
            return False
            
    except Exception as e:
        print(f"   ❌ Tool execution failed: {e}")
        return False
    
    # Test 4: Loyalty points success
    print("\n4. Testing loyalty points (success case):")
    try:
        result = PaymentTools.debit_loyalty_points(
            customer_id="test-customer-999",
            points_to_debit=500
        )
        print(f"   Result: {result}")
        
        # Verify it's valid JSON
        parsed = json.loads(result)
        if parsed.get("status") == "success":
            print("   ✅ Correctly returned success status")
        else:
            print("   ❌ Expected success status")
            return False
            
    except Exception as e:
        print(f"   ❌ Tool execution failed: {e}")
        return False
    
    # Test 5: Loyalty points failure
    print("\n5. Testing loyalty points (failure case):")
    try:
        result = PaymentTools.debit_loyalty_points(
            customer_id="test-customer-888",
            points_to_debit=1500
        )
        print(f"   Result: {result}")
        
        # Verify it's valid JSON
        parsed = json.loads(result)
        if parsed.get("status") == "failed":
            print("   ✅ Correctly returned failure status")
        else:
            print("   ❌ Expected failure status")
            return False
            
    except Exception as e:
        print(f"   ❌ Tool execution failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 PAYMENT TOOLS TESTING")
    print("="*50)
    
    success = test_tools_directly()
    
    print("\n" + "="*50)
    print("TOOLS TEST SUMMARY")
    print("="*50)
    
    if success:
        print("🎉 All payment tools are working correctly!")
        print("   Your payment tools are functioning as expected.")
        print("   Next step: Test the full agent system.")
    else:
        print("❌ Some tool tests failed.")
        print("   Check the errors above for details.")

if __name__ == "__main__":
    main()
