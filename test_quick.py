"""
Quick Test Script - Fast way to test the system
Run this to quickly verify everything works
"""
# Load .env file if it exists
try:
    from dotenv import load_dotenv
    import os
    project_root = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

# Add Orchestrator to path before importing
import sys
import os
orchestrator_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Orchestrator')
if orchestrator_path not in sys.path:
    sys.path.insert(0, orchestrator_path)

from Orchestrator.main import handle_custom_request

def quick_test():
    """Run a quick test of each agent type"""
    print("\n" + "=" * 60)
    print("🚀 QUICK SYSTEM TEST")
    print("=" * 60 + "\n")
    
    tests = [
        ("Inventory", "Check stock for SKU-123"),
        ("Fulfillment", "Ship order ORD-123 to customer"),
        ("Payment", "Process $150 payment"),
        ("Loyalty", "Calculate price with coupon SAVE20"),
        ("Support", "Track order ORD-12345"),
    ]
    
    for agent_name, request in tests:
        print(f"\n📋 Testing {agent_name} Agent:")
        print(f"   Request: {request}")
        try:
            result = handle_custom_request(request)
            print(f"   ✅ SUCCESS - Response received")
            print(f"   Preview: {str(result)[:100]}...")
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Quick test completed!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    quick_test()

