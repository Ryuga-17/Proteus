"""
Test Size Recommendation
"""
import requests
import sys

API_BASE_URL = "http://localhost:8000"

def test_size_recommendation():
    print("\n" + "="*70)
    print("  📏 TESTING SIZE RECOMMENDATION")
    print("="*70 + "\n")
    
    request_data = {
        "product_id": "PROD-123",
        "user_id": "test_user",
        "body_measurements": {
            "chest": 42,
            "waist": 36,
            "hip": 42,
            "shoulder": 18
        },
        "preferred_fit": "regular",
        "material_preference": "cotton"
    }
    
    print(f"📝 Request:")
    print(f"   Product ID: {request_data['product_id']}")
    print(f"   Body Measurements: {request_data['body_measurements']}")
    print(f"   Preferred Fit: {request_data['preferred_fit']}")
    print(f"   Material: {request_data['material_preference']}\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/size/recommend",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"📏 Recommended Size: {data.get('recommended_size')}")
            print(f"📊 Confidence: {data.get('confidence', 0):.1%}")
            print(f"💡 Reasoning: {data.get('reasoning', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Start it with: cd backend && python main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "="*70)
    print("Check backend terminal for detailed logs!")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_size_recommendation()




