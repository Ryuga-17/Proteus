# 🚀 Run All Logs - Complete Testing Guide

This guide shows you how to see all the logs for every feature in the terminal.

## Quick Start

### 1. Start the Backend

Open a terminal and run:

```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000` and you'll see it ready to receive requests.

### 2. Run All Tests

In a **new terminal** (keep the backend running), run:

```bash
python test_all_logs.py
```

This will test all scenarios and trigger all logs in the backend terminal.

## What You'll See

### Backend Terminal Will Show:

All the detailed logs for:

1. **🎤 Voice Recommendation**
   - Query analysis
   - Product matching
   - Recommendations with scores

2. **🤖 Agent Queries** (6 different agents)
   - Intent detection
   - Agent routing
   - Processing steps
   - Results

3. **📏 Size Recommendation**
   - Body measurements analysis
   - Size chart matching
   - Material and fit adjustments
   - Final recommendation

4. **🖼️  Virtual Try-On**
   - Image validation
   - Nano Banana model processing
   - Pose detection
   - Garment alignment
   - Fit analysis

5. **🏪 In-Store Try-On Booking**
   - Inventory Agent integration
   - Stock check
   - Reservation creation
   - Booking confirmation

## Individual Test Scripts

You can also test individual features:

```bash
# Voice recommendation
python test_single_voice.py "looking for a shirt for date"

# Size recommendation
python test_size_recommendation.py

# Virtual try-on
python test_virtual_tryon.py

# In-store try-on booking
python test_instore_tryon.py

# All voice scenarios
python test_voice_scenarios.py
```

## Expected Log Output

### Example: Voice Recommendation

```
======================================================================
🎤 VOICE RECOMMENDATION REQUEST RECEIVED
======================================================================
📝 Query: looking for a shirt for date
👤 User ID: test_user
======================================================================

🔧 Processing recommendations...
🔍 Query analysis:
   - Query text: 'looking for a shirt for date'
   - Query length: 28 characters
   - Query words: 5 words

======================================================================
✅ VOICE RECOMMENDATION RESPONSE
======================================================================
✅ Success: True
📦 Recommendations: 4
⏱️  Processing time: 523.45ms
======================================================================
```

### Example: In-Store Try-On Booking

```
======================================================================
🏪 IN-STORE TRY-ON BOOKING REQUEST RECEIVED
======================================================================
📦 Product ID: PROD-123
🏷️  SKU: sku_123
👤 User ID: test_user
📍 Store Location: store_main_street
📏 Size: L
📅 Preferred Date: 2024-12-25
🕐 Preferred Time: 14:00
======================================================================

🔍 Step 1: Routing to Inventory Agent for stock check...
   - Requesting inventory check for SKU: sku_123
   - Store location: store_main_street
   - Checking availability at specified store...

======================================================================
📦 ROUTING TO INVENTORY AGENT
======================================================================
📝 Request: Check stock for sku_123 at store_main_street
🔍 Analyzing inventory request...
======================================================================

🔧 [INVENTORY] Setting up inventory crew...
   - Agents: Orchestrator, Logistics, Procurement
   - Request: 'Check stock for sku_123 at store_main_street'

🚀 [INVENTORY] Starting inventory processing...
⚙️  [INVENTORY] Processing inventory request...
   - Querying stock database...
   - Location: store_main_street
   - SKU: sku_123
   - Stock found at store_main_street: 5 units

✅ [INVENTORY] Inventory check complete!
   - Store: store_main_street
   - SKU: sku_123
   - Available stock: 5 units
======================================================================

🔍 Step 2: Validating stock availability...
   ✅ Stock available: 5 units
   - Sufficient stock for try-on reservation

🔍 Step 3: Creating reservation in inventory system...
   - Creating reservation for 24 hours
   - Reservation expires: 2024-12-24 15:30:45
   - Store: store_main_street
   - SKU: sku_123
   ✅ Reservation created
   - Booking ID: TRYON-TEST_U-1234567890
   - Reserved until: 2024-12-24 15:30:45

🔍 Step 4: Updating inventory system (reservation hold)...
   - Placing hold on 1 unit for try-on
   - Stock before reservation: 5 units
   - Available stock after reservation: 4 units
   - Note: Stock will be released if not picked up within 24 hours

🔍 Step 5: Generating booking confirmation...
   - Preferred slot: 2024-12-25 at 14:00
   ✅ Confirmation message generated

======================================================================
✅ IN-STORE TRY-ON BOOKING RESPONSE
======================================================================
✅ Success: True
📋 Booking ID: TRYON-TEST_U-1234567890
📍 Store: store_main_street
📦 Product: PROD-123 (sku_123)
📊 Stock Available: 5 units
⏰ Reserved Until: 2024-12-24 15:30:45
⏱️  Processing time: 1234.56ms
======================================================================
```

## Tips

1. **Keep Backend Running**: Don't close the backend terminal - it shows all the logs
2. **Watch Both Terminals**: 
   - Backend terminal = Detailed logs
   - Test script terminal = Summary results
3. **Scroll Up**: Logs can be long, scroll up in the backend terminal to see everything
4. **Check Timing**: Each log shows processing time for performance analysis

## Troubleshooting

### Backend Not Running
```
❌ Backend not running. Start it with: cd backend && python main.py
```
Solution: Start the backend first in a separate terminal.

### Connection Error
```
❌ Cannot connect to backend. Make sure backend is running on http://localhost:8000
```
Solution: Check that backend is running and accessible.

### No Logs Appearing
- Make sure backend is running
- Check that requests are being sent (test script should show results)
- Verify backend terminal is visible and not minimized

## Complete Log Reference

See `EXAMPLE_LOGS.md` for complete log examples for all scenarios:
- Scenario 1: Voice Recommendation
- Scenario 2: Inventory Agent
- Scenario 3: Payment Agent
- Scenario 4: Fulfillment Agent
- Scenario 5: Loyalty Agent
- Scenario 6: Support Agent
- Scenario 7: Recommendation Agent
- Scenario 8: Product Purchase
- Scenario 9: General Query
- Scenario 10: Size Recommendation
- Scenario 11: Virtual Try-On
- Scenario 12: In-Store Try-On Booking

All logs are designed to be clear, informative, and easy to follow!




