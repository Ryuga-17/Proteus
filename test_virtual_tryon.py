"""
Test Virtual Try-On
"""
import requests
import sys

API_BASE_URL = "http://localhost:8000"

def test_virtual_tryon():
    print("\n" + "="*70)
    print("  🖼️  TESTING VIRTUAL TRY-ON")
    print("="*70 + "\n")
    
    request_data = {
        "product_id": "PROD-123",
        "user_id": "test_user",
        "user_image_url": "https://example.com/user-photos/test_user.jpg",
        "pose_type": "standing"
    }
    
    print(f"📝 Request:")
    print(f"   Product ID: {request_data['product_id']}")
    print(f"   User Image: {request_data['user_image_url']}")
    print(f"   Pose Type: {request_data['pose_type']}\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/virtual-tryon",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"🖼️  Result Image: {data.get('result_image_url')}")
            print(f"📊 Fit Score: {data.get('fit_analysis', {}).get('overall_fit_score', 0):.1%}")
            print(f"⏱️  Processing Time: {data.get('processing_time', 0):.2f}ms")
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
    test_virtual_tryon()




