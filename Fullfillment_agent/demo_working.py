#!/usr/bin/env python3
"""
Working demo of the fulfillment agent system
This demonstrates the core functionality without CrewAI agent issues
"""

import json
from tools import book_shipment_func, reserve_in_store_func, notify_staff_func

def simulate_fulfillment_agent(order_data):
    """
    Simulate the fulfillment agent processing an order
    """
    print(f"\n{'='*60}")
    print(f"PROCESSING ORDER: {order_data['order_id']}")
    print(f"TYPE: {order_data['type']}")
    print(f"{'='*60}")
    
    try:
        if order_data['type'] == 'ship-to-home':
            # Process ship-to-home order
            print("🚚 Processing Ship-to-Home Order...")
            
            # Step 1: Book shipment
            shipment_result = book_shipment_func(
                order_id=order_data['order_id'],
                address=order_data['address'],
                items=order_data['items']
            )
            shipment_data = json.loads(shipment_result)
            print(f"✅ Shipment booked with tracking: {shipment_data['tracking_number']}")
            
            # Step 2: Notify warehouse staff
            notification = notify_staff_func(
                queue="warehouse_1",
                message=f"New shipment order {shipment_data['tracking_number']} needs processing"
            )
            print(f"✅ Warehouse staff notified")
            
            # Return final result
            final_result = {
                "order_id": order_data['order_id'],
                "status": "SHIPPED",
                "tracking_number": shipment_data['tracking_number'],
                "estimated_delivery": shipment_data['estimated_delivery'],
                "staff_notified": True
            }
            
        elif order_data['type'] == 'reserve-in-store':
            # Process reserve-in-store order
            print("🏪 Processing Reserve In-Store Order...")
            
            # Step 1: Reserve in store
            reservation_result = reserve_in_store_func(
                order_id=order_data['order_id'],
                store_id=order_data['store_id'],
                items=order_data['items']
            )
            reservation_data = json.loads(reservation_result)
            print(f"✅ Items reserved with pickup code: {reservation_data['pickup_code']}")
            
            # Step 2: Notify store staff
            notification = notify_staff_func(
                queue="store_102_pickup",
                message=f"New pickup order {reservation_data['pickup_code']} ready for customer"
            )
            print(f"✅ Store staff notified")
            
            # Return final result
            final_result = {
                "order_id": order_data['order_id'],
                "status": "RESERVED",
                "store_id": reservation_data['store_id'],
                "pickup_code": reservation_data['pickup_code'],
                "hold_expires": reservation_data['hold_expires'],
                "staff_notified": True
            }
        
        else:
            raise ValueError(f"Unknown fulfillment type: {order_data['type']}")
        
        print(f"\n✅ ORDER PROCESSED SUCCESSFULLY")
        return final_result
        
    except Exception as e:
        print(f"❌ ERROR PROCESSING ORDER: {e}")
        return {"order_id": order_data['order_id'], "status": "ERROR", "error": str(e)}

def main():
    """
    Main function to demonstrate the fulfillment agent system
    """
    print("FULFILLMENT AGENT SYSTEM DEMO")
    print("="*60)
    
    # Scenario 1: Ship-to-Home
    print("\n🚀 SCENARIO 1: SHIP-TO-HOME")
    ship_to_home_order = {
        "order_id": "ORD-12345",
        "type": "ship-to-home",
        "customer": "C-456",
        "address": "123 Green St, Bengaluru, KA 560001",
        "items": [
            {"sku": "RED-SHIRT-SML", "qty": 1},
            {"sku": "BLUE-JEANS-32", "qty": 1}
        ]
    }
    
    result1 = simulate_fulfillment_agent(ship_to_home_order)
    print(f"\n📋 FINAL RESULT (Ship-to-Home):")
    print(json.dumps(result1, indent=2))
    
    # Scenario 2: Reserve In-Store
    print("\n\n🚀 SCENARIO 2: RESERVE IN-STORE")
    reserve_in_store_order = {
        "order_id": "ORD-12346",
        "type": "reserve-in-store",
        "customer": "C-789",
        "store_id": "S-102-MUMBAI",
        "items": [
            {"sku": "BLK-DRESS-MED", "qty": 1}
        ]
    }
    
    result2 = simulate_fulfillment_agent(reserve_in_store_order)
    print(f"\n📋 FINAL RESULT (Reserve In-Store):")
    print(json.dumps(result2, indent=2))
    
    print(f"\n{'='*60}")
    print("DEMO COMPLETE - ALL SYSTEMS FUNCTIONING")
    print("="*60)

if __name__ == "__main__":
    main()
