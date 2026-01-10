"""
Test In-Store Try-On Booking
"""
import requests
import sys

API_BASE_URL = "http://localhost:8000"

def test_instore_tryon():
    print("\n" + "="*70)
    print("  🏪 TESTING IN-STORE TRY-ON BOOKING")
    print("="*70 + "\n")
    
    request_data = {
        "product_id": "PROD-123",
        "sku": "sku_123",
        "user_id": "test_user",
        "store_location": "store_main_street",
        "preferred_date": "2024-12-25",
        "preferred_time": "14:00",
        "size": "L"
    }
    
    print(f"📝 Request:")
    print(f"   Product ID: {request_data['product_id']}")
    print(f"   SKU: {request_data['sku']}")
    print(f"   Store: {request_data['store_location']}")
    print(f"   Date: {request_data['preferred_date']}")
    print(f"   Time: {request_data['preferred_time']}")
    print(f"   Size: {request_data['size']}\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/instore-tryon/book",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"📋 Booking ID: {data.get('booking_id')}")
            print(f"📍 Store: {data.get('store_location')}")
            print(f"📦 Product: {data.get('product_id')}")
            print(f"📊 Stock Available: {data.get('current_stock')} units")
            print(f"⏰ Reserved Until: {data.get('reserved_until')}")
            print(f"💬 Message: {data.get('message', '')[:100]}...")
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
    test_instore_tryon()




