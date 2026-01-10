"""
User Query Simulator - Simulates real user interactions
"""
import requests
import time
import sys

API_BASE_URL = "http://localhost:8000"

def voice_query(query: str):
    """User voice search query"""
    print(f"\n👤 User: {query}\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/recommendations/voice",
            json={
                "query": query,
                "user_id": "user_001"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data.get('recommendations', []))} recommendations\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    time.sleep(1)

def user_query(request_text: str):
    """User query to the system"""
    print(f"\n👤 User: {request_text}\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/agent/query",
            json={
                "request": request_text,
                "user_id": "user_001"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Processed by {data.get('agent_used', 'system')}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    time.sleep(0.5)

def size_recommendation():
    """User requests size recommendation"""
    print(f"\n👤 User: What size should I get for this product?\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/size/recommend",
            json={
                "product_id": "PROD-123",
                "user_id": "user_001",
                "body_measurements": {
                    "chest": 42,
                    "waist": 36,
                    "hip": 42,
                    "shoulder": 18
                },
                "preferred_fit": "regular",
                "material_preference": "cotton"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recommended size: {data.get('recommended_size')}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    time.sleep(1)

def virtual_tryon():
    """User requests virtual try-on"""
    print(f"\n👤 User: Can I see how this looks on me?\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/virtual-tryon",
            json={
                "product_id": "PROD-123",
                "user_id": "user_001",
                "user_image_url": "https://example.com/user-photos/user_001.jpg",
                "pose_type": "standing"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Virtual try-on complete. Fit score: {data.get('fit_analysis', {}).get('overall_fit_score', 0):.1%}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    time.sleep(1)

def instore_tryon_booking():
    """User books in-store try-on"""
    print(f"\n👤 User: I'd like to book an in-store try-on for this product\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/instore-tryon/book",
                json={
                    "product_id": "PROD-123",
                    "sku": "sku_123",
                    "user_id": "user_001",
                    "store_location": "store_main_street",
                    "preferred_date": "2024-12-25",
                    "preferred_time": "14:00",
                    "size": "M"
                },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Booking confirmed: {data.get('booking_id')}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    time.sleep(1)

def main():
    """Simulate user interactions"""
    print("\n" + "="*70)
    print("  PROTEUS Retail System - User Interactions")
    print("="*70 + "\n")
    
    time.sleep(1)
    
    try:
        print("="*70)
        print("  USER JOURNEY: White Sweatshirt Purchase Flow")
        print("="*70 + "\n")
        
        voice_query("looking for a sweatshirt")
        
        time.sleep(1)
        
        user_query("check discount for this product")
        
        time.sleep(1)
        
        print(f"\n👤 User: What size should I get for this product?\n")
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/size/recommend",
                json={
                    "product_id": "PROD-123",
                    "user_id": "user_001",
                    "body_measurements": {
                        "chest": 40,
                        "waist": 34,
                        "hip": 40,
                        "shoulder": 17
                    },
                    "preferred_fit": "regular",
                    "material_preference": "cotton"
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Recommended size: {data.get('recommended_size')}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
        
        time.sleep(1)
        
        print(f"\n👤 User: Can I see how this looks on me?\n")
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/virtual-tryon",
                json={
                    "product_id": "PROD-123",
                    "user_id": "user_001",
                    "user_image_url": "https://example.com/user-photos/user_001.jpg",
                    "pose_type": "standing"
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Virtual try-on complete. Fit score: {data.get('fit_analysis', {}).get('overall_fit_score', 0):.1%}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
        
        time.sleep(1)
        
        print(f"\n👤 User: I'd like to book an in-store try-on for this product\n")
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/instore-tryon/book",
                json={
                    "product_id": "PROD-123",
                    "sku": "sku_123",
                    "user_id": "user_001",
                    "store_location": "store_main_street",
                    "preferred_date": "2024-12-25",
                    "preferred_time": "14:00",
                    "size": "M"
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Booking confirmed: {data.get('booking_id')}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

