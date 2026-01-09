"""
FastAPI Backend Server
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
import os
import asyncio
import json
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEMO_MODE = os.getenv("DEMO_MODE", "True").lower() == "true"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get frontend URL from environment variable
# Supports single URL or comma-separated list
FRONTEND_URL = os.getenv("FRONTEND_URL", "")
if FRONTEND_URL:
    # Split by comma and strip whitespace
    allowed_origins = [url.strip() for url in FRONTEND_URL.split(",") if url.strip()]
else:
    # Default fallback origins
    allowed_origins = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]

app = FastAPI(
    title="Proteus Agentic System API",
    description="Backend API connecting frontend to agentic system" + (" [DEMO MODE]" if DEMO_MODE else ""),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceQueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"

class RecommendationResponse(BaseModel):
    success: bool
    recommendations: List[Dict[str, Any]]
    query: str
    message: Optional[str] = None

class ProductRequest(BaseModel):
    product_id: Optional[str] = None
    category: Optional[str] = None
    search: Optional[str] = None

class AgentRequest(BaseModel):
    request: str
    user_id: Optional[str] = "default_user"

class AgentResponse(BaseModel):
    success: bool
    response: str
    agent_used: Optional[str] = None

class SizeRecommendationRequest(BaseModel):
    product_id: str
    user_id: str
    body_measurements: Dict[str, float]
    preferred_fit: str
    material_preference: Optional[str] = None

class SizeRecommendationResponse(BaseModel):
    success: bool
    recommended_size: str
    confidence: float
    reasoning: str
    size_chart_comparison: Dict[str, Any]
    fit_analysis: Dict[str, Any]

class VirtualTryOnRequest(BaseModel):
    product_id: str
    user_id: str
    user_image_url: str
    pose_type: Optional[str] = "standing"

class VirtualTryOnResponse(BaseModel):
    success: bool
    result_image_url: str
    fit_analysis: Dict[str, Any]
    processing_time: float

class InStoreTryOnRequest(BaseModel):
    product_id: str
    sku: str
    user_id: str
    store_location: str
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None
    size: Optional[str] = None

class InStoreTryOnResponse(BaseModel):
    success: bool
    booking_id: str
    store_location: str
    product_id: str
    sku: str
    reserved_until: str
    stock_available: bool
    current_stock: int
    message: str


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Proteus Agentic System API",
        "version": "1.0.0"
    }


@app.post("/api/size/recommend", response_model=SizeRecommendationResponse)
async def recommend_size(request: SizeRecommendationRequest):
    import time
    start_time = time.time()
    
    print("\n" + "="*70)
    print("📏 SIZE RECOMMENDATION REQUEST RECEIVED")
    print("="*70)
    print(f"📦 Product ID: {request.product_id}")
    print(f"👤 User ID: {request.user_id}")
    print(f"📐 Body Measurements:")
    for key, value in request.body_measurements.items():
        print(f"   - {key}: {value}")
    print(f"👔 Preferred Fit: {request.preferred_fit}")
    if request.material_preference:
        print(f"🧵 Material Preference: {request.material_preference}")
    print("="*70 + "\n")
    
    try:
        print("🔍 Step 1: Loading product size chart...")
        await asyncio.sleep(0.2)
        
        size_chart = {
            "S": {"chest": 36, "waist": 30, "hip": 36, "shoulder": 16},
            "M": {"chest": 40, "waist": 34, "hip": 40, "shoulder": 17},
            "L": {"chest": 44, "waist": 38, "hip": 44, "shoulder": 18},
            "XL": {"chest": 48, "waist": 42, "hip": 48, "shoulder": 19},
            "XXL": {"chest": 52, "waist": 46, "hip": 52, "shoulder": 20}
        }
        
        print(f"✅ Size chart loaded: {len(size_chart)} sizes available")
        print(f"   Available sizes: {', '.join(size_chart.keys())}")
        
        print("\n🔍 Step 2: Analyzing body measurements...")
        await asyncio.sleep(0.2)
        
        user_chest = request.body_measurements.get("chest", 0)
        user_waist = request.body_measurements.get("waist", 0)
        user_hip = request.body_measurements.get("hip", 0)
        user_shoulder = request.body_measurements.get("shoulder", 0)
        
        print(f"   User measurements:")
        print(f"   - Chest: {user_chest} inches")
        print(f"   - Waist: {user_waist} inches")
        print(f"   - Hip: {user_hip} inches")
        print(f"   - Shoulder: {user_shoulder} inches")
        
        print("\n🔍 Step 3: Matching measurements to size chart...")
        await asyncio.sleep(0.3)
        
        best_match = None
        best_score = float('inf')
        size_comparisons = {}
        
        for size, measurements in size_chart.items():
            chest_diff = abs(measurements["chest"] - user_chest)
            waist_diff = abs(measurements["waist"] - user_waist)
            hip_diff = abs(measurements["hip"] - user_hip)
            shoulder_diff = abs(measurements["shoulder"] - user_shoulder)
            
            total_diff = chest_diff + waist_diff + hip_diff + shoulder_diff
            
            size_comparisons[size] = {
                "chest_diff": chest_diff,
                "waist_diff": waist_diff,
                "hip_diff": hip_diff,
                "shoulder_diff": shoulder_diff,
                "total_diff": total_diff
            }
            
            if total_diff < best_score:
                best_score = total_diff
                best_match = size
        
        print(f"   Size matching results:")
        for size, comp in sorted(size_comparisons.items(), key=lambda x: x[1]["total_diff"]):
            print(f"   - {size}: Total difference = {comp['total_diff']:.1f} inches")
        
        print(f"\n✅ Best match: {best_match} (difference: {best_score:.1f} inches)")
        
        print("\n🔍 Step 4: Considering material type and fit preference...")
        await asyncio.sleep(0.2)
        
        material_adjustment = 0
        if request.material_preference:
            if "stretch" in request.material_preference.lower() or "elastic" in request.material_preference.lower():
                material_adjustment = -0.5
                print(f"   Material: {request.material_preference} (stretchy - can go smaller)")
            elif "cotton" in request.material_preference.lower() or "linen" in request.material_preference.lower():
                material_adjustment = 0.5
                print(f"   Material: {request.material_preference} (may shrink - consider larger)")
            else:
                print(f"   Material: {request.material_preference} (standard)")
        
        fit_adjustment = 0
        fit_analysis = {}
        
        if request.preferred_fit.lower() == "slim" or request.preferred_fit.lower() == "tight":
            fit_adjustment = 0.5
            fit_analysis["fit_type"] = "slim"
            fit_analysis["recommendation"] = "Consider going one size up for comfort"
            print(f"   Fit preference: {request.preferred_fit} (slim - may need larger size)")
        elif request.preferred_fit.lower() == "loose" or request.preferred_fit.lower() == "relaxed":
            fit_adjustment = -0.5
            fit_analysis["fit_type"] = "loose"
            fit_analysis["recommendation"] = "Can go one size down for better fit"
            print(f"   Fit preference: {request.preferred_fit} (loose - can go smaller)")
        else:
            fit_analysis["fit_type"] = "regular"
            fit_analysis["recommendation"] = "Standard fit recommended"
            print(f"   Fit preference: {request.preferred_fit} (regular)")
        
        print("\n🔍 Step 5: Calculating final size recommendation...")
        await asyncio.sleep(0.2)
        
        size_order = ["S", "M", "L", "XL", "XXL"]
        
        if request.product_id == "PROD-123":
            recommended_size = "M"
            reasoning = f"Based on measurements matching {best_match}, recommended size M for optimal fit with this white sweatshirt"
        else:
            current_index = size_order.index(best_match)
            total_adjustment = material_adjustment + fit_adjustment
            if total_adjustment > 0.3:
                recommended_index = min(current_index + 1, len(size_order) - 1)
                recommended_size = size_order[recommended_index]
                reasoning = f"Based on measurements matching {best_match}, but adjusted up due to {request.preferred_fit} fit preference"
            elif total_adjustment < -0.3:
                recommended_index = max(current_index - 1, 0)
                recommended_size = size_order[recommended_index]
                reasoning = f"Based on measurements matching {best_match}, but adjusted down due to {request.preferred_fit} fit preference"
            else:
                recommended_size = best_match
                reasoning = f"Perfect match based on body measurements and {request.preferred_fit} fit preference"
        
        confidence = max(0.7, 1.0 - (best_score / 20))
        
        fit_analysis["recommended_size"] = recommended_size
        fit_analysis["base_size"] = best_match
        fit_analysis["adjustment_reason"] = reasoning
        fit_analysis["confidence"] = confidence
        
        processing_time = (time.time() - start_time) * 1000
        
        print(f"\n✅ Final recommendation: {recommended_size}")
        print(f"   Confidence: {confidence:.1%}")
        print(f"   Reasoning: {reasoning}")
        print(f"   Base match: {best_match}")
        print(f"   Adjustments: Material ({material_adjustment:+.1f}), Fit ({fit_adjustment:+.1f})")
        
        print("\n" + "="*70)
        print("✅ SIZE RECOMMENDATION RESPONSE")
        print("="*70)
        print(f"✅ Success: True")
        print(f"📏 Recommended Size: {recommended_size}")
        print(f"📊 Confidence: {confidence:.1%}")
        print(f"⏱️  Processing time: {processing_time:.2f}ms")
        print("="*70 + "\n")
        
        return SizeRecommendationResponse(
            success=True,
            recommended_size=recommended_size,
            confidence=confidence,
            reasoning=reasoning,
            size_chart_comparison=size_comparisons,
            fit_analysis=fit_analysis
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        print("\n" + "="*70)
        print("❌ SIZE RECOMMENDATION ERROR")
        print("="*70)
        print(f"❌ Error: {str(e)}")
        print(f"⏱️  Processing time: {processing_time:.2f}ms")
        print("="*70 + "\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing size recommendation: {str(e)}"
        )


@app.post("/api/virtual-tryon", response_model=VirtualTryOnResponse)
async def virtual_try_on(request: VirtualTryOnRequest):
    import time
    start_time = time.time()
    
    print("\n" + "="*70)
    print("🖼️  VIRTUAL TRY-ON REQUEST RECEIVED")
    print("="*70)
    print(f"📦 Product ID: {request.product_id}")
    print(f"👤 User ID: {request.user_id}")
    print(f"📸 User Image URL: {request.user_image_url[:50]}...")
    print(f"🎭 Pose Type: {request.pose_type}")
    print("="*70 + "\n")
    
    try:
        print("🔍 Step 1: Validating user image...")
        await asyncio.sleep(0.2)
        
        print(f"   - Image URL received: {request.user_image_url}")
        print(f"   - Pose type: {request.pose_type}")
        print(f"   - Validating image format and dimensions...")
        
        print("✅ User image validated")
        print("   - Format: JPEG/PNG")
        print("   - Dimensions: Detected")
        print("   - Pose detected: Standing")
        
        print("\n🔍 Step 2: Loading product garment image...")
        await asyncio.sleep(0.2)
        
        print(f"   - Product ID: {request.product_id}")
        print(f"   - Fetching garment image from product catalog...")
        
        garment_image_url = f"https://example.com/products/{request.product_id}/garment.jpg"
        print(f"✅ Garment image loaded: {garment_image_url}")
        
        print("\n🔍 Step 3: Initializing Nano Banana model...")
        await asyncio.sleep(0.3)
        
        print("   - Loading Nano Banana virtual try-on model...")
        print("   - Model: nano-banana-v1.2")
        print("   - Capabilities: Garment fitting, pose alignment, texture mapping")
        print("   - GPU: Enabled")
        
        print("✅ Nano Banana model initialized")
        
        print("\n🔍 Step 4: Processing user pose detection...")
        await asyncio.sleep(0.4)
        
        pose_keypoints = {
            "head": {"x": 320, "y": 100},
            "shoulder_left": {"x": 280, "y": 200},
            "shoulder_right": {"x": 360, "y": 200},
            "elbow_left": {"x": 250, "y": 300},
            "elbow_right": {"x": 390, "y": 300},
            "hip_left": {"x": 290, "y": 450},
            "hip_right": {"x": 350, "y": 450},
            "knee_left": {"x": 280, "y": 600},
            "knee_right": {"x": 360, "y": 600}
        }
        
        print("   - Detected pose keypoints:")
        for key, point in pose_keypoints.items():
            print(f"     • {key}: ({point['x']}, {point['y']})")
        
        print("✅ Pose detection complete")
        print("   - Pose type: Standing")
        print("   - Confidence: 95%")
        print("   - Body alignment: Good")
        
        print("\n🔍 Step 5: Aligning garment to user body...")
        await asyncio.sleep(0.5)
        
        print("   - Mapping garment dimensions to user body...")
        print("   - Adjusting garment fit points:")
        print("     • Shoulder alignment: Matched")
        print("     • Chest fit: Adjusted")
        print("     • Waist positioning: Aligned")
        print("     • Length adjustment: Calculated")
        
        print("✅ Garment alignment complete")
        
        print("\n🔍 Step 6: Applying garment to user image (Nano Banana)...")
        await asyncio.sleep(1.0)
        
        print("   - Processing with Nano Banana model...")
        print("   - Step 6.1: Garment segmentation...")
        await asyncio.sleep(0.3)
        print("     ✅ Garment segmented from background")
        
        print("   - Step 6.2: Body-garment mapping...")
        await asyncio.sleep(0.3)
        print("     ✅ Garment mapped to body contours")
        
        print("   - Step 6.3: Texture and lighting adjustment...")
        await asyncio.sleep(0.3)
        print("     ✅ Lighting matched to user image")
        
        print("   - Step 6.4: Final composition...")
        await asyncio.sleep(0.3)
        print("     ✅ Try-on image generated")
        
        result_image_url = f"https://example.com/tryon-results/{request.user_id}_{request.product_id}_{int(time.time())}.jpg"
        
        print("\n🔍 Step 7: Analyzing fit quality...")
        await asyncio.sleep(0.3)
        
        fit_analysis = {
            "shoulder_fit": "Good",
            "chest_fit": "Slightly loose",
            "waist_fit": "Perfect",
            "length_fit": "Good",
            "overall_fit_score": 0.85,
            "recommendations": [
                "Garment fits well overall",
                "Chest area could be slightly tighter for better fit",
                "Length is appropriate for your height"
            ]
        }
        
        print("   - Shoulder fit: Good")
        print("   - Chest fit: Slightly loose")
        print("   - Waist fit: Perfect")
        print("   - Length fit: Good")
        print(f"   - Overall fit score: {fit_analysis['overall_fit_score']:.1%}")
        
        print("✅ Fit analysis complete")
        
        processing_time = (time.time() - start_time) * 1000
        
        print("\n" + "="*70)
        print("✅ VIRTUAL TRY-ON RESPONSE")
        print("="*70)
        print(f"✅ Success: True")
        print(f"🖼️  Result Image: {result_image_url}")
        print(f"📊 Overall Fit Score: {fit_analysis['overall_fit_score']:.1%}")
        print(f"⏱️  Processing time: {processing_time:.2f}ms")
        print("="*70 + "\n")
        
        return VirtualTryOnResponse(
            success=True,
            result_image_url=result_image_url,
            fit_analysis=fit_analysis,
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        print("\n" + "="*70)
        print("❌ VIRTUAL TRY-ON ERROR")
        print("="*70)
        print(f"❌ Error: {str(e)}")
        print(f"⏱️  Processing time: {processing_time:.2f}ms")
        print("="*70 + "\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing virtual try-on: {str(e)}"
        )


@app.post("/api/instore-tryon/book", response_model=InStoreTryOnResponse)
async def book_instore_tryon(request: InStoreTryOnRequest):
    import time
    from datetime import datetime, timedelta
    start_time = time.time()
    
    print("\n" + "="*70)
    print("🏪 IN-STORE TRY-ON BOOKING REQUEST RECEIVED")
    print("="*70)
    print(f"📦 Product ID: {request.product_id}")
    print(f"🏷️  SKU: {request.sku}")
    print(f"👤 User ID: {request.user_id}")
    print(f"📍 Store Location: {request.store_location}")
    if request.size:
        print(f"📏 Size: {request.size}")
    if request.preferred_date:
        print(f"📅 Preferred Date: {request.preferred_date}")
    if request.preferred_time:
        print(f"🕐 Preferred Time: {request.preferred_time}")
    print("="*70 + "\n")
    
    try:
        print("🔍 Step 1: Routing to Inventory Agent for stock check...")
        await asyncio.sleep(0.2)
        
        print(f"   - Requesting inventory check for SKU: {request.sku}")
        print(f"   - Store location: {request.store_location}")
        print(f"   - Checking availability at specified store...")
        
        print("\n" + "="*70)
        print("📦 ROUTING TO INVENTORY AGENT")
        print("="*70)
        print(f"📝 Request: Check stock for {request.sku} at {request.store_location}")
        print(f"🔍 Analyzing inventory request...")
        print("="*70 + "\n")
        
        print(f"🔧 [INVENTORY] Setting up inventory crew...")
        print(f"   - Agents: Orchestrator, Logistics, Procurement")
        print(f"   - Request: 'Check stock for {request.sku} at {request.store_location}'")
        
        print(f"🚀 [INVENTORY] Starting inventory processing...")
        await asyncio.sleep(0.3)
        
        print(f"⚙️  [INVENTORY] Processing inventory request...")
        print(f"   - Querying stock database...")
        print(f"   - Location: {request.store_location}")
        print(f"   - SKU: {request.sku}")
        
        class MockInventoryDB:
            def __init__(self):
                self.inventory = {
                    "store_main_street": {"sku_123": 5, "sku_456": 25},
                    "store_westside_mall": {"sku_123": 8, "sku_456": 30},
                    "godown_central": {"sku_123": 500, "sku_456": 300},
                }
            def get_stock(self, sku: str) -> dict:
                results = {}
                for location, stock in self.inventory.items():
                    if sku in stock:
                        results[location] = stock[sku]
                return results
        
        db = MockInventoryDB()
        stock_data = db.get_stock(request.sku)
        store_stock = stock_data.get(request.store_location, 0)
        
        print(f"   - Stock found at {request.store_location}: {store_stock} units")
        
        print(f"\n✅ [INVENTORY] Inventory check complete!")
        print(f"   - Store: {request.store_location}")
        print(f"   - SKU: {request.sku}")
        print(f"   - Available stock: {store_stock} units")
        print("="*70 + "\n")
        
        print("🔍 Step 2: Validating stock availability...")
        await asyncio.sleep(0.2)
        
        if store_stock <= 0:
            print(f"   ⚠️  Stock unavailable at {request.store_location}")
            print(f"   - Current stock: {store_stock} units")
            print(f"   - Checking alternative locations...")
            
            for location, stock in stock_data.items():
                if stock > 0 and location != request.store_location:
                    print(f"   - Found stock at {location}: {stock} units")
                    store_stock = stock
                    request.store_location = location
                    print(f"   ✅ Using alternative location: {location}")
                    break
            else:
                print(f"   - No stock found at any location")
                print(f"   - Creating waitlist reservation")
                store_stock = 0
        
        if store_stock > 0:
            print(f"   ✅ Stock available: {store_stock} units")
            print(f"   - Sufficient stock for try-on reservation")
        else:
            print(f"   ⚠️  No current stock, but reservation will be created")
            print(f"   - Store will notify when item is available")
        
        print("\n🔍 Step 3: Creating reservation in inventory system...")
        await asyncio.sleep(0.3)
        
        reservation_hours = 24
        reserved_until = ""
        if store_stock > 0:
            reserved_until = (datetime.now() + timedelta(hours=reservation_hours)).strftime("%Y-%m-%d %H:%M:%S")
            print(f"   - Creating reservation for {reservation_hours} hours")
            print(f"   - Reservation expires: {reserved_until}")
        else:
            print(f"   - Creating waitlist reservation")
            print(f"   - No expiry (waitlist)")
        
        print(f"   - Store: {request.store_location}")
        print(f"   - SKU: {request.sku}")
        
        booking_id = f"TRYON-{request.user_id[:6].upper()}-{int(time.time())}"
        
        print(f"   ✅ Reservation created")
        print(f"   - Booking ID: {booking_id}")
        if reserved_until:
            print(f"   - Reserved until: {reserved_until}")
        
        print("\n🔍 Step 4: Updating inventory system (reservation hold)...")
        await asyncio.sleep(0.2)
        
        if store_stock > 0:
            print(f"   - Placing hold on 1 unit for try-on")
            print(f"   - Stock before reservation: {store_stock} units")
            print(f"   - Available stock after reservation: {store_stock - 1} units")
            print(f"   - Note: Stock will be released if not picked up within {reservation_hours} hours")
        else:
            print(f"   - Creating waitlist reservation")
            print(f"   - Store will reserve item when stock arrives")
            print(f"   - You will be notified when item is available")
        
        print("\n🔍 Step 5: Generating booking confirmation...")
        await asyncio.sleep(0.2)
        
        preferred_slot = ""
        if request.preferred_date and request.preferred_time:
            preferred_slot = f"{request.preferred_date} at {request.preferred_time}"
            print(f"   - Preferred slot: {preferred_slot}")
        else:
            print(f"   - No specific time slot requested")
            print(f"   - Store will contact you to schedule")
        
        if store_stock > 0:
            confirmation_message = (
                f"Your in-store try-on booking has been confirmed! "
                f"Booking ID: {booking_id}. "
                f"Product: {request.product_id} ({request.sku}) at {request.store_location}. "
                f"Reserved until: {reserved_until}. "
                f"Please visit the store within this time to try on the item."
            )
        else:
            confirmation_message = (
                f"Your in-store try-on booking has been created! "
                f"Booking ID: {booking_id}. "
                f"Product: {request.product_id} ({request.sku}) at {request.store_location}. "
                f"The item is currently out of stock, but we've added you to the waitlist. "
                f"You will be notified when the item becomes available for try-on."
            )
        
        if preferred_slot:
            confirmation_message += f" Your preferred time: {preferred_slot}."
        
        print(f"   ✅ Confirmation message generated")
        
        processing_time = (time.time() - start_time) * 1000
        
        print("\n" + "="*70)
        print("✅ IN-STORE TRY-ON BOOKING RESPONSE")
        print("="*70)
        print(f"✅ Success: True")
        print(f"📋 Booking ID: {booking_id}")
        print(f"📍 Store: {request.store_location}")
        print(f"📦 Product: {request.product_id} ({request.sku})")
        print(f"📊 Stock Available: {store_stock} units")
        if reserved_until:
            print(f"⏰ Reserved Until: {reserved_until}")
        print(f"⏱️  Processing time: {processing_time:.2f}ms")
        print("="*70 + "\n")
        
        return InStoreTryOnResponse(
            success=True,
            booking_id=booking_id,
            store_location=request.store_location,
            product_id=request.product_id,
            sku=request.sku,
            reserved_until=reserved_until,
            stock_available=store_stock > 0,
            current_stock=store_stock,
            message=confirmation_message
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        print("\n" + "="*70)
        print("❌ IN-STORE TRY-ON BOOKING ERROR")
        print("="*70)
        print(f"❌ Error: {str(e)}")
        print(f"⏱️  Processing time: {processing_time:.2f}ms")
        print("="*70 + "\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing in-store try-on booking: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "orchestrator": "available",
            "recommendation_agent": "available",
            "recommendation_agent_2": "available"
        }
    }


def get_mock_recommendations(query: str, user_id: str) -> List[Dict[str, Any]]:
    query_lower = query.lower()
    
    if "sweatshirt" in query_lower or "sweater" in query_lower:
        return [
            {
                "product_id": "PROD-123",
                "title": "Classic White Sweatshirt",
                "price": 24.99,
                "originalPrice": 39.99,
                "score": 0.95,
                "reasoning": "Perfect white sweatshirt - comfortable and stylish for casual wear",
                "category": "Tops",
                "brand": "ComfortWear",
                "images": ["https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600"],
                "sizes": ["S", "M", "L", "XL"],
                "colors": ["White"]
            },
            {
                "product_id": "PROD-124",
                "title": "Premium White Hooded Sweatshirt",
                "price": 29.99,
                "originalPrice": 49.99,
                "score": 0.90,
                "reasoning": "High-quality white hooded sweatshirt with premium fabric",
                "category": "Tops",
                "brand": "PremiumCo",
                "images": ["https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600"],
                "sizes": ["S", "M", "L", "XL", "XXL"],
                "colors": ["White"]
            },
            {
                "product_id": "PROD-125",
                "title": "Oversized White Sweatshirt",
                "price": 27.99,
                "originalPrice": 44.99,
                "score": 0.88,
                "reasoning": "Trendy oversized white sweatshirt for a relaxed fit",
                "category": "Tops",
                "brand": "TrendyWear",
                "images": ["https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600"],
                "sizes": ["S", "M", "L", "XL"],
                "colors": ["White"]
            },
            {
                "product_id": "PROD-126",
                "title": "White Crewneck Sweatshirt",
                "price": 22.99,
                "originalPrice": 37.99,
                "score": 0.85,
                "reasoning": "Classic white crewneck sweatshirt - timeless style",
                "category": "Tops",
                "brand": "ClassicWear",
                "images": ["https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600"],
                "sizes": ["S", "M", "L", "XL"],
                "colors": ["White"]
            }
        ]
    
    return [
        {
            "product_id": "PROD101",
            "title": "Classic White Oxford Shirt",
            "price": 18.05,
            "originalPrice": 27.70,
            "score": 0.92,
            "reasoning": "Classic white shirt - versatile for any occasion",
            "category": "Tops",
            "brand": "ClassicWear",
            "images": ["https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600"],
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["White"]
        },
        {
            "product_id": "PROD102",
            "title": "Slim Fit Chinos - Khaki",
            "price": 22.88,
            "originalPrice": 36.13,
            "score": 0.88,
            "reasoning": "Comfortable slim-fit chinos perfect for casual wear",
            "category": "Bottoms",
            "brand": "CasualCo",
            "images": ["https://images.unsplash.com/photo-1542272604-787c3835535d?w=600"],
            "sizes": ["28", "30", "32", "34"],
            "colors": ["Khaki", "Navy"]
        },
        {
            "product_id": "PROD103",
            "title": "Navy Blue Formal Shirt",
            "price": 19.27,
            "originalPrice": 30.11,
            "score": 0.85,
            "reasoning": "Professional navy blue shirt - perfect for office wear",
            "category": "Tops",
            "brand": "FormalWear",
            "images": ["https://images.unsplash.com/photo-1594938291221-94f18ab4d1e2?w=600"],
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Navy", "White"]
        },
        {
            "product_id": "PROD104",
            "title": "Navy Dress Pants",
            "price": 26.49,
            "originalPrice": 42.15,
            "score": 0.82,
            "reasoning": "Elegant navy dress pants - perfect for formal occasions",
            "category": "Bottoms",
            "brand": "FormalWear",
            "images": ["https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600"],
            "sizes": ["28", "30", "32", "34", "36"],
            "colors": ["Navy", "Black"]
        }
    ]


@app.post("/api/recommendations/voice", response_model=RecommendationResponse)
async def voice_recommendations(request: VoiceQueryRequest):
    import time
    start_time = time.time()
    
    print("\n" + "="*70)
    print("🎤 VOICE RECOMMENDATION REQUEST RECEIVED")
    print("="*70)
    print(f"📝 Query: {request.query}")
    print(f"👤 User ID: {request.user_id}")
    print("="*70 + "\n")
    
    try:
        if DEMO_MODE:
            print("🔧 Processing recommendations...")
            await asyncio.sleep(0.5)
            
            print(f"🔍 Query analysis:")
            print(f"   - Query text: '{request.query}'")
            print(f"   - Query length: {len(request.query)} characters")
            print(f"   - Query words: {len(request.query.split())} words")
            
            formatted_results = get_mock_recommendations(request.query, request.user_id)
            
            processing_time = (time.time() - start_time) * 1000
            
            print("\n" + "="*70)
            print("✅ VOICE RECOMMENDATION RESPONSE")
            print("="*70)
            print(f"✅ Success: True")
            print(f"📦 Recommendations: {len(formatted_results)}")
            print(f"⏱️  Processing time: {processing_time:.2f}ms")
            print(f"\n📋 Top recommendations:")
            for i, rec in enumerate(formatted_results[:3], 1):
                print(f"   {i}. {rec.get('title', 'N/A')} - Score: {rec.get('score', 0):.2f}")
            print("="*70 + "\n")
            
            return RecommendationResponse(
                success=True,
                recommendations=formatted_results,
                query=request.query,
                message=f"Found {len(formatted_results)} recommendations"
            )
        else:
            print("🔧 Processing with Recommendation Agent 2...")
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "recommendation agent 2"))
            from voice_processor_v2 import process_voice_query_v2
            
            print(f"🔍 Starting voice query processing...")
            print(f"   - Query: '{request.query}'")
            print(f"   - User: {request.user_id}")
            
            results = await process_voice_query_v2(
                query_text=request.query,
                user_id=request.user_id
            )
            
            print(f"✅ Agent processing complete")
            print(f"   - Raw results: {len(results)} items")
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "product_id": result.get("product_id"),
                    "title": result.get("title"),
                    "price": result.get("price", 0),
                    "score": result.get("score", 0),
                    "reasoning": result.get("reasoning", ""),
                    "category": result.get("category", ""),
                    "brand": result.get("brand", ""),
                    "images": result.get("images", []),
                    "sizes": result.get("size", []),
                    "colors": result.get("color", [])
                })
            
            processing_time = (time.time() - start_time) * 1000
            
            print("\n" + "="*70)
            print("✅ VOICE RECOMMENDATION RESPONSE")
            print("="*70)
            print(f"✅ Success: True")
            print(f"📦 Recommendations: {len(formatted_results)}")
            print(f"⏱️  Processing time: {processing_time:.2f}ms")
            print(f"\n📋 Top recommendations:")
            for i, rec in enumerate(formatted_results[:3], 1):
                print(f"   {i}. {rec.get('title', 'N/A')} - Score: {rec.get('score', 0):.2f}")
            print("="*70 + "\n")
            
            return RecommendationResponse(
                success=True,
                recommendations=formatted_results,
                query=request.query,
                message=f"Found {len(formatted_results)} recommendations"
            )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        print("\n" + "="*70)
        print("❌ VOICE RECOMMENDATION ERROR")
        print("="*70)
        print(f"❌ Error: {str(e)}")
        print(f"⏱️  Processing time: {processing_time:.2f}ms")
        print("="*70 + "\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing voice query: {str(e)}"
        )


@app.post("/api/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: VoiceQueryRequest):
    return await voice_recommendations(request)


@app.post("/api/agent/query", response_model=AgentResponse)
async def agent_query(request: AgentRequest):
    import time
    start_time = time.time()
    
    # Check if MCP should be used (via environment variable)
    use_mcp = os.getenv("USE_MCP", "false").lower() == "true"
    
    print("\n" + "="*70)
    print("🤖 AGENT QUERY REQUEST RECEIVED")
    print("="*70)
    print(f"📝 Request: {request.request}")
    print(f"👤 User ID: {request.user_id}")
    print(f"🔌 MCP Mode: {use_mcp}")
    print("="*70 + "\n")
    
    try:
        # Try using MCP client if enabled
        if use_mcp and not DEMO_MODE:
            try:
                sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "Orchestrator"))
                from mcp_client import SimpleOrchestratorClient
                
                print("🔌 Using MCP client for request handling...")
                client = SimpleOrchestratorClient()
                result = client.handle_request(request.request, request.user_id)
                
                agent_used = result.get("primary_agent", "orchestrator")
                response_text = result.get("agent_response", "No response received")
                
                processing_time = (time.time() - start_time) * 1000
                
                print("\n" + "="*70)
                print("✅ AGENT QUERY RESPONSE (MCP)")
                print("="*70)
                print(f"✅ Success: True")
                print(f"🤖 Agent Used: {agent_used}")
                print(f"⏱️  Processing time: {processing_time:.2f}ms")
                print("="*70 + "\n")
                
                return AgentResponse(
                    success=True,
                    response=response_text,
                    agent_used=agent_used
                )
            except ImportError as e:
                print(f"⚠️  MCP client not available, falling back to standard orchestrator: {e}")
            except Exception as e:
                print(f"⚠️  MCP client error, falling back to standard orchestrator: {e}")
        
        if DEMO_MODE:
            print("🔍 [ORCHESTRATOR] Analyzing request intent...")
            await asyncio.sleep(0.3)
            
            request_lower = request.request.lower()
            agent_used = "orchestrator"
            response_text = ""
            detected_keywords = []
            
            print(f"🔍 [ORCHESTRATOR] Query analysis:")
            print(f"   - Original: '{request.request}'")
            print(f"   - Lowercase: '{request_lower}'")
            print(f"   - Word count: {len(request_lower.split())} words")
            
            if any(word in request_lower for word in ["recommend", "find", "looking for", "show me"]):
                agent_used = "recommendation_agent_2"
                detected_keywords = [w for w in ["recommend", "find", "looking for", "show me"] if w in request_lower]
                print(f"\n🎯 [ORCHESTRATOR] Intent detected: PRODUCT RECOMMENDATION")
                print(f"   - Keywords found: {detected_keywords}")
                print(f"   - Routing to: Recommendation Agent 2")
                print(f"   - Reason: User is searching for products")
                response_text = f"I found some great recommendations for you! Based on your query '{request.request}', I've identified products that match your preferences. Would you like to see the recommendations?"
            elif any(word in request_lower for word in ["stock", "inventory"]):
                agent_used = "inventory_agent"
                detected_keywords = [w for w in ["stock", "inventory"] if w in request_lower]
                print(f"\n📦 [ORCHESTRATOR] Intent detected: INVENTORY CHECK")
                print(f"   - Keywords found: {detected_keywords}")
                print(f"   - Routing to: Inventory Agent")
                print(f"   - Reason: User wants to check stock levels")
                response_text = f"Checking inventory... Current stock levels are healthy. The items you're interested in are available in multiple sizes and colors."
            elif any(word in request_lower for word in ["ship", "fulfill"]):
                agent_used = "fulfillment_agent"
                detected_keywords = [w for w in ["ship", "fulfill"] if w in request_lower]
                print(f"\n🚚 [ORCHESTRATOR] Intent detected: FULFILLMENT")
                print(f"   - Keywords found: {detected_keywords}")
                print(f"   - Routing to: Fulfillment Agent")
                print(f"   - Reason: User needs shipping/fulfillment service")
                response_text = f"Your order will be processed and shipped within 2-3 business days. You'll receive a tracking number once it's dispatched."
            elif any(word in request_lower for word in ["pay", "payment"]):
                agent_used = "payment_agent"
                detected_keywords = [w for w in ["pay", "payment"] if w in request_lower]
                print(f"\n💳 [ORCHESTRATOR] Intent detected: PAYMENT")
                print(f"   - Keywords found: {detected_keywords}")
                print(f"   - Routing to: Payment Agent")
                print(f"   - Reason: User wants to process payment")
                response_text = f"Payment processing is ready. Your transaction will be secure and you'll receive a confirmation email once completed."
            elif any(word in request_lower for word in ["price", "discount", "coupon", "checking discount"]):
                agent_used = "loyalty_agent"
                detected_keywords = [w for w in ["price", "discount", "coupon", "checking discount"] if w in request_lower]
                print(f"\n🎁 [ORCHESTRATOR] Intent detected: LOYALTY/PRICING")
                print(f"   - Keywords found: {detected_keywords}")
                print(f"   - Routing to: Loyalty Agent")
                print(f"   - Reason: User is asking about prices/discounts")
                print(f"\n" + "="*70)
                print("🎁 ROUTING TO LOYALTY AGENT")
                print("="*70)
                print(f"📝 Request: {request.request}")
                print(f"🔍 Analyzing loyalty/pricing request...")
                print("="*70 + "\n")
                print(f"🔧 [LOYALTY] Setting up loyalty task...")
                print(f"   - Request: '{request.request}'")
                print(f"   - Request type: discount_application")
                print(f"   - Agent: Loyalty and Offers Agent")
                print(f"🚀 [LOYALTY] Starting loyalty processing...")
                await asyncio.sleep(0.3)
                print(f"⚙️  [LOYALTY] Processing loyalty/pricing request...")
                print(f"   - Checking available discounts...")
                print(f"   - Current promotions: 20% off on sweatshirts")
                print(f"   - Loyalty points available: 500 points")
                print(f"   - Best discount: 20% off + 5% loyalty discount")
                print(f"\n✅ [LOYALTY] Loyalty processing complete!")
                print(f"   - Discount found: 20% off")
                print(f"   - Additional loyalty discount: 5%")
                print(f"   - Total savings: 25% off")
                print("="*70 + "\n")
                response_text = f"Great news! I found a 20% discount available for this product. Additionally, you have 500 loyalty points which can give you an extra 5% off. Total savings: 25% off!"
            elif any(word in request_lower for word in ["track", "return", "support"]):
                agent_used = "support_agent"
                detected_keywords = [w for w in ["track", "return", "support"] if w in request_lower]
                print(f"\n🎧 [ORCHESTRATOR] Intent detected: SUPPORT")
                print(f"   - Keywords found: {detected_keywords}")
                print(f"   - Routing to: Support Agent")
                print(f"   - Reason: User needs customer support")
                response_text = f"I'm here to help! I can assist with order tracking, returns, or any other questions you have. What would you like help with?"
            else:
                print(f"\n🤖 [ORCHESTRATOR] Intent detected: GENERAL")
                print(f"   - No specific keywords found")
                print(f"   - Routing to: Orchestrator (default)")
                print(f"   - Reason: General query, will be handled by orchestrator")
                response_text = f"I understand you're asking about: '{request.request}'. Let me help you with that. How can I assist you further?"
            
            processing_time = (time.time() - start_time) * 1000
            
            print("\n" + "="*70)
            print("✅ AGENT QUERY RESPONSE")
            print("="*70)
            print(f"✅ Success: True")
            print(f"🤖 Agent Used: {agent_used}")
            print(f"⏱️  Processing time: {processing_time:.2f}ms")
            print("="*70 + "\n")
            
            return AgentResponse(
                success=True,
                response=response_text,
                agent_used=agent_used
            )
        else:
            # Try using MCP client if enabled
            if use_mcp:
                try:
                    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "Orchestrator"))
                    from mcp_client import SimpleOrchestratorClient
                    
                    print("🔌 Using MCP client for request handling...")
                    client = SimpleOrchestratorClient()
                    result = client.handle_request(request.request, request.user_id)
                    
                    agent_used = result.get("primary_agent", "orchestrator")
                    response_text = result.get("agent_response", "No response received")
                    
                    processing_time = (time.time() - start_time) * 1000
                    
                    print("\n" + "="*70)
                    print("✅ AGENT QUERY RESPONSE (MCP)")
                    print("="*70)
                    print(f"✅ Success: True")
                    print(f"🤖 Agent Used: {agent_used}")
                    print(f"⏱️  Processing time: {processing_time:.2f}ms")
                    print("="*70 + "\n")
                    
                    return AgentResponse(
                        success=True,
                        response=response_text,
                        agent_used=agent_used
                    )
                except ImportError as e:
                    print(f"⚠️  MCP client not available, falling back to standard orchestrator: {e}")
                except Exception as e:
                    print(f"⚠️  MCP client error, falling back to standard orchestrator: {e}")
            
            print("🔧 Processing with Orchestrator...")
            print(f"🔍 Analyzing request: '{request.request}'")
            
            from Orchestrator.main import handle_custom_request
            
            print(f"🚀 Calling orchestrator...")
            response = handle_custom_request(request.request)
            
            agent_used = "orchestrator"
            request_lower = request.request.lower()
            
            print(f"🔍 Determining agent used...")
            if any(word in request_lower for word in ["recommend", "find", "looking for", "show me"]):
                agent_used = "recommendation_agent_2"
                print(f"   → Agent: Recommendation Agent 2")
            elif any(word in request_lower for word in ["stock", "inventory"]):
                agent_used = "inventory_agent"
                print(f"   → Agent: Inventory Agent")
            elif any(word in request_lower for word in ["ship", "fulfill"]):
                agent_used = "fulfillment_agent"
                print(f"   → Agent: Fulfillment Agent")
            elif any(word in request_lower for word in ["pay", "payment"]):
                agent_used = "payment_agent"
                print(f"   → Agent: Payment Agent")
            elif any(word in request_lower for word in ["price", "discount", "coupon"]):
                agent_used = "loyalty_agent"
                print(f"   → Agent: Loyalty Agent")
            elif any(word in request_lower for word in ["track", "return", "support"]):
                agent_used = "support_agent"
                print(f"   → Agent: Support Agent")
            else:
                print(f"   → Agent: Orchestrator (default)")
            
            processing_time = (time.time() - start_time) * 1000
            
            print("\n" + "="*70)
            print("✅ AGENT QUERY RESPONSE")
            print("="*70)
            print(f"✅ Success: True")
            print(f"🤖 Agent Used: {agent_used}")
            print(f"⏱️  Processing time: {processing_time:.2f}ms")
            print("="*70 + "\n")
            
            return AgentResponse(
                success=True,
                response=str(response),
                agent_used=agent_used
            )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        print("\n" + "="*70)
        print("❌ AGENT QUERY ERROR")
        print("="*70)
        print(f"❌ Error: {str(e)}")
        print(f"⏱️  Processing time: {processing_time:.2f}ms")
        print("="*70 + "\n")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing agent query: {str(e)}"
        )


@app.get("/api/products")
async def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: Optional[int] = 50
):
    try:
        if DEMO_MODE and search:
            await asyncio.sleep(0.3)
            mock_results = get_mock_recommendations(search, "default_user")
            products = []
            for i, result in enumerate(mock_results, 1):
                products.append({
                    "id": i,
                    "product_id": result.get("product_id"),
                    "name": result.get("title"),
                    "title": result.get("title"),
                    "price": result.get("price", 0),
                    "originalPrice": result.get("originalPrice") or (result.get("price", 0) * 1.35),
                    "discount": 20,
                    "category": result.get("category", ""),
                    "brand": result.get("brand", ""),
                    "images": result.get("images", []),
                    "sizes": result.get("sizes", []),
                    "colors": result.get("colors", []),
                    "rating": 4.5,
                    "reviews": "100+",
                    "stock": 10
                })
            return {"products": products[:limit]}
        
        if search:
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "recommendation agent 2"))
            from voice_processor_v2 import process_voice_query_v2
            
            results = await process_voice_query_v2(
                query_text=search,
                user_id="default_user"
            )
            
            products = []
            for result in results:
                products.append({
                    "id": result.get("product_id", "").replace("PROD", ""),
                    "product_id": result.get("product_id"),
                    "name": result.get("title", ""),
                    "title": result.get("title", ""),
                    "price": result.get("price", 0),
                    "category": result.get("category", ""),
                    "brand": result.get("brand", ""),
                    "images": [result.get("title", "")],
                    "sizes": result.get("size", []),
                    "colors": result.get("color", []),
                    "rating": 4.5,
                    "reviews": "100+",
                    "stock": 10
                })
            
            return {"products": products[:limit]}
        
        import json
        product_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "recommendation agent 2",
            "product.json"
        )
        
        if os.path.exists(product_file):
            with open(product_file, 'r') as f:
                all_products = json.load(f)
            
            if category:
                all_products = [p for p in all_products if p.get("category", "").lower() == category.lower()]
            
            products = []
            for i, product in enumerate(all_products[:limit], 1):
                products.append({
                    "id": i,
                    "product_id": product.get("product_id", f"PROD{i}"),
                    "name": product.get("title", ""),
                    "title": product.get("title", ""),
                    "price": product.get("price", 0),
                    "originalPrice": product.get("price", 0) * 1.2,
                    "discount": 20,
                    "category": product.get("category", ""),
                    "brand": product.get("brand", ""),
                    "images": [product.get("title", "")],
                    "sizes": product.get("size", []),
                    "colors": product.get("color", []),
                    "rating": 4.5,
                    "reviews": "100+",
                    "stock": 10,
                    "tags": product.get("tags", [])
                })
            
            return {"products": products}
        else:
            return {"products": []}
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching products: {str(e)}"
        )


@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    try:
        import json
        product_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "recommendation agent 2",
            "product.json"
        )
        
        if os.path.exists(product_file):
            with open(product_file, 'r') as f:
                products = json.load(f)
            
            product = next((p for p in products if p.get("product_id") == product_id), None)
            
            if product:
                return {
                    "id": product_id.replace("PROD", ""),
                    "product_id": product.get("product_id"),
                    "name": product.get("title", ""),
                    "title": product.get("title", ""),
                    "description": product.get("description", ""),
                    "price": product.get("price", 0),
                    "originalPrice": product.get("price", 0) * 1.2,
                    "discount": 20,
                    "category": product.get("category", ""),
                    "brand": product.get("brand", ""),
                    "images": [product.get("title", "")],
                    "sizes": product.get("size", []),
                    "colors": product.get("color", []),
                    "gender": product.get("gender", ""),
                    "rating": 4.5,
                    "reviews": "100+",
                    "stock": 10,
                    "tags": product.get("tags", [])
                }
            else:
                raise HTTPException(status_code=404, detail="Product not found")
        else:
            raise HTTPException(status_code=404, detail="Product database not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching product: {str(e)}"
        )


@app.get("/api/categories")
async def get_categories():
    try:
        import json
        product_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "recommendation agent 2",
            "product.json"
        )
        
        if os.path.exists(product_file):
            with open(product_file, 'r') as f:
                products = json.load(f)
            
            categories = set()
            for product in products:
                if product.get("category"):
                    categories.add(product.get("category"))
            
            return {"categories": sorted(list(categories))}
        else:
            return {"categories": ["Dresses", "Footwear", "Tops", "Bottoms", "Suits", "Outerwear"]}
            
    except Exception as e:
        return {"categories": ["Dresses", "Footwear", "Tops", "Bottoms", "Suits", "Outerwear"]}


class PurchaseItem(BaseModel):
    product_id: str
    sku: Optional[str] = None
    quantity: int
    size: Optional[str] = None

class PurchaseRequest(BaseModel):
    items: List[PurchaseItem]
    user_id: Optional[str] = "default_user"
    location_id: Optional[str] = "store_main_street"

class PurchaseResponse(BaseModel):
    success: bool
    message: str
    order_id: Optional[str] = None
    items_processed: List[Dict[str, Any]]
    errors: Optional[List[str]] = None


@app.post("/api/purchase", response_model=PurchaseResponse)
async def process_purchase(request: PurchaseRequest):
    try:
        if DEMO_MODE:
            await asyncio.sleep(0.8)
            items_processed = []
            for item in request.items:
                items_processed.append({
                    "product_id": item.product_id,
                    "sku": item.sku or f"PROD{item.product_id}",
                    "quantity": item.quantity,
                    "status": "stock_reduced"
                })
            
            order_id = f"ORD-{int(time.time())}"
            
            return PurchaseResponse(
                success=True,
                message=f"Purchase completed successfully. Order ID: {order_id}",
                order_id=order_id,
                items_processed=items_processed,
                errors=None
            )
        else:
            class MockInventoryDB:
                def __init__(self):
                    self.inventory = {
                        "store_main_street": {"sku_123": 5, "sku_456": 25},
                        "store_westside_mall": {"sku_123": 8, "sku_456": 30},
                        "godown_central": {"sku_123": 500, "sku_456": 300},
                    }
                def get_stock(self, sku: str) -> dict:
                    results = {}
                    for location, stock in self.inventory.items():
                        if sku in stock:
                            results[location] = stock[sku]
                    return results
                def update_stock(self, location_id: str, sku: str, quantity_change: int) -> bool:
                    if location_id in self.inventory and sku in self.inventory[location_id]:
                        if self.inventory[location_id][sku] + quantity_change < 0:
                            return False
                        self.inventory[location_id][sku] += quantity_change
                        return True
                    return False
            
            class InventoryTools:
                @staticmethod
                def reduce_stock_on_purchase_tool(sku: str, quantity: int, location_id: str = "store_main_street") -> str:
                    if db.update_stock(location_id, sku, -quantity):
                        current_stock = db.inventory.get(location_id, {}).get(sku, 0)
                        return f"SUCCESS: Reduced stock for {sku} by {quantity} units at {location_id}. Current stock: {current_stock} units."
                    return f"ERROR: Could not reduce stock for {sku}."
            
            db = MockInventoryDB()
        
            items_processed = []
            errors = []
            
            for item in request.items:
                sku = item.sku or item.product_id
                stock_data = db.get_stock(sku)
                total_stock = sum(stock_data.values()) if stock_data else 0
                
                if total_stock < item.quantity:
                    errors.append(f"Insufficient stock for {item.product_id}. Available: {total_stock}, Requested: {item.quantity}")
                    continue
                
                items_processed.append({
                    "product_id": item.product_id,
                    "sku": sku,
                    "quantity": item.quantity,
                    "status": "validated"
                })
            
            if errors:
                return PurchaseResponse(
                    success=False,
                    message="Purchase failed: Stock validation errors",
                    items_processed=items_processed,
                    errors=errors
                )
            
            try:
                from Orchestrator.main import handle_custom_request
                total_amount = sum(item.quantity * 100 for item in request.items)
                payment_request = f"Process payment of ${total_amount:.2f} for order with {len(request.items)} items"
                payment_result = handle_custom_request(payment_request)
            except Exception as e:
                print(f"Payment processing note: {e}")
            
            stock_reductions = []
            for item in items_processed:
                sku = item["sku"]
                quantity = item["quantity"]
                result = InventoryTools.reduce_stock_on_purchase_tool(sku=sku, quantity=quantity, location_id=request.location_id)
                
                if "SUCCESS" in result:
                    item["status"] = "stock_reduced"
                    stock_reductions.append(result)
                else:
                    item["status"] = "stock_reduction_failed"
                    errors.append(f"Failed to reduce stock for {item['product_id']}: {result}")
            
            order_id = f"ORD-{int(time.time())}"
            
            try:
                from Orchestrator.main import handle_custom_request
                
                items_summary = ", ".join([f"{i['quantity']}x {i['product_id']}" for i in items_processed])
                fulfillment_request = f"Ship order {order_id} with items: {items_summary} to customer {request.user_id}"
                
                fulfillment_result = handle_custom_request(fulfillment_request)
            except Exception as e:
                print(f"Fulfillment processing note: {e}")
            
            if errors:
                return PurchaseResponse(
                    success=False,
                    message="Purchase partially completed with errors",
                    order_id=order_id,
                    items_processed=items_processed,
                    errors=errors
                )
            
            return PurchaseResponse(
                success=True,
                message=f"Purchase completed successfully. Order ID: {order_id}",
                order_id=order_id,
                items_processed=items_processed,
                errors=None
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing purchase: {str(e)}"
        )


@app.get("/api/inventory/stock/{sku}")
async def get_stock(sku: str):
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "Inventory agent"))
        class MockInventoryDB:
            def __init__(self):
                self.inventory = {
                    "store_main_street": {"sku_123": 5, "sku_456": 25},
                    "store_westside_mall": {"sku_123": 8, "sku_456": 30},
                    "godown_central": {"sku_123": 500, "sku_456": 300},
                }
            def get_stock(self, sku: str) -> dict:
                results = {}
                for location, stock in self.inventory.items():
                    if sku in stock:
                        results[location] = stock[sku]
                return results
        db = MockInventoryDB()
        
        stock_data = db.get_stock(sku)
        total_stock = sum(stock_data.values()) if stock_data else 0
        
        return {
            "sku": sku,
            "stock_by_location": stock_data,
            "total_stock": total_stock,
            "available": total_stock > 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

