#!/usr/bin/env python3
"""
Simple test script for the Payment Agent system.
This tests the core functionality without requiring LLM configuration.
"""

import json

def test_basic_functionality():
    """Test the basic payment functionality"""
    print("🚀 PAYMENT AGENT SIMPLE TEST")
    print("="*50)
    
    # Test 1: Import and basic tool functionality
    print("\n1. Testing tool imports...")
    try:
        from tools import process_standard_payment, generate_kiosk_to_mobile_handoff, debit_loyalty_points
        print("✅ All tools imported successfully")
    except Exception as e:
        print(f"❌ Tool import failed: {e}")
        return False
    
    # Test 2: Payment processing
    print("\n2. Testing payment processing...")
    try:
        # Test successful payment
        result = process_standard_payment.func(
            customer_id="test-123",
            amount=25.00,
            payment_method="credit_card",
            details={"card_number": "1234-5678"}
        )
        parsed = json.loads(result)
        if parsed.get("status") == "success":
            print("✅ Payment processing works")
        else:
            print("❌ Payment processing failed")
            return False
    except Exception as e:
        print(f"❌ Payment processing error: {e}")
        return False
    
    # Test 3: Kiosk handoff
    print("\n3. Testing kiosk handoff...")
    try:
        result = generate_kiosk_to_mobile_handoff.func(
            customer_id="test-456",
            amount=50.00,
            session_id="kiosk-001"
        )
        parsed = json.loads(result)
        if "payment_url_for_qr_code" in parsed:
            print("✅ Kiosk handoff works")
        else:
            print("❌ Kiosk handoff failed")
            return False
    except Exception as e:
        print(f"❌ Kiosk handoff error: {e}")
        return False
    
    # Test 4: Loyalty points
    print("\n4. Testing loyalty points...")
    try:
        result = debit_loyalty_points.func(
            customer_id="test-789",
            points_to_debit=100
        )
        parsed = json.loads(result)
        if parsed.get("status") == "success":
            print("✅ Loyalty points work")
        else:
            print("❌ Loyalty points failed")
            return False
    except Exception as e:
        print(f"❌ Loyalty points error: {e}")
        return False
    
    return True

def test_scenario_simulation():
    """Simulate the payment scenarios without agents"""
    print("\n" + "="*50)
    print("SCENARIO SIMULATION")
    print("="*50)
    
    from tools import process_standard_payment, generate_kiosk_to_mobile_handoff, debit_loyalty_points
    
    # Scenario 1: Payment failure
    print("\n📋 Scenario 1: Payment Failure")
    print("Customer: cust-789, Amount: $150.00, Card: fail-1234")
    result = process_standard_payment.func(
        customer_id="cust-789",
        amount=150.00,
        payment_method="credit_card",
        details={"card_number": "fail-1234"}
    )
    print(f"Result: {result}")
    
    # Scenario 2: Kiosk handoff
    print("\n📋 Scenario 2: Kiosk-to-Mobile Handoff")
    print("Customer: cust-303, Amount: $85.20, Session: kiosk-A9")
    result = generate_kiosk_to_mobile_handoff.func(
        customer_id="cust-303",
        amount=85.20,
        session_id="kiosk-A9"
    )
    print(f"Result: {result}")
    
    # Scenario 3: Loyalty points
    print("\n📋 Scenario 3: Pay with Points")
    print("Customer: cust-555, Points: 500")
    result = debit_loyalty_points.func(
        customer_id="cust-555",
        points_to_debit=500
    )
    print(f"Result: {result}")

def main():
    """Main test function"""
    success = test_basic_functionality()
    
    if success:
        print("\n🎉 BASIC FUNCTIONALITY TEST PASSED!")
        test_scenario_simulation()
        
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        print("✅ Your payment agent tools are working correctly!")
        print("✅ All three payment scenarios can be processed")
        print("✅ The system is ready for agent integration")
        print("\n📝 Next steps:")
        print("   1. Set up OpenAI API key for full agent functionality")
        print("   2. Run: export OPENAI_API_KEY='your-key-here'")
        print("   3. Test with: python main.py")
    else:
        print("\n❌ BASIC FUNCTIONALITY TEST FAILED!")
        print("   Check the errors above for details.")

if __name__ == "__main__":
    main()
