# Testing Guide - Session-Based Authentication

## Quick Start Testing

### 1. Start the Backend

```bash
# Make sure you're in the project root
cd "/Users/viveksawant/Desktop/Complete System Techathon"

# Start the backend
cd backend
python main.py
# Or use the start script:
# ./start_backend.sh
```

The backend should start on `http://localhost:8000`

### 2. Run Automated Tests

```bash
# Install requests if needed
pip install requests

# Run the test script
cd whatsapp_integration
python test_session_auth.py
```

This will run all test scenarios automatically.

---

## Manual Testing with cURL

### Test 1: First-Time User Login

```bash
# Step 1: Send "Hi"
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "Hi"
  }'

# Step 2: Enter phone number
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "+918850833367"
  }'

# Step 3: Enter OTP (check the response from Step 2 for the OTP in DEV MODE)
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "123456"
  }'
```

### Test 2: Returning User (Welcome Back)

```bash
# Send "Hi" again - should get welcome back message
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "Hi"
  }'
```

**Expected Response:** "👋 Welcome back! You're already logged in..."

### Test 3: Low-Risk Action (No Step-Up)

```bash
# Browse products - should work immediately
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "Show me products"
  }'
```

**Expected:** Routes to orchestrator, no step-up authentication

### Test 4: High-Risk Action - Payment (Step-Up Required)

```bash
# Step 1: Request payment
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "I want to pay ₹15,000"
  }'

# Step 2: Confirm (reply YES)
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "YES"
  }'

# Step 3: Enter OTP (check response from Step 2)
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "654321"
  }'
```

**Expected Flow:**
1. Security check message
2. OTP sent (for high-value payments)
3. Verification successful

### Test 5: Low-Value Payment (Confirmation Only)

```bash
# Request small payment
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "I want to pay ₹500"
  }'

# Confirm
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "YES"
  }'
```

**Expected:** Just confirmation, no OTP needed (amount < ₹10,000)

### Test 6: Logout

```bash
# Logout
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "logout"
  }'

# Try to use system again - should ask for login
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "whatsapp:+918850833367",
    "message_text": "Hi"
  }'
```

---

## Testing with Python Script

### Run the Complete Test Suite

```bash
cd whatsapp_integration
python test_session_auth.py
```

This will test:
1. ✅ First-time login
2. ✅ Returning user welcome back
3. ✅ Low-risk actions (no step-up)
4. ✅ High-risk actions (step-up required)
5. ✅ Payment flows
6. ✅ Refund requests
7. ✅ Address changes
8. ✅ Logout
9. ✅ Multiple users

### Customize Test Scenarios

Edit `test_session_auth.py` to add your own test cases:

```python
test_scenario("My Custom Test", [
    {"phone": "+918850833367", "message": "Your message", "wait": 1},
    # Add more steps...
])
```

---

## Testing Scenarios Checklist

### ✅ Authentication Flow
- [ ] First-time user sends "Hi" → Asks for phone number
- [ ] User enters phone number → Sends OTP
- [ ] User enters correct OTP → Authenticated
- [ ] User enters wrong OTP → Error message
- [ ] User sends "Hi" again (with valid session) → Welcome back message

### ✅ Session Management
- [ ] Valid session persists across messages
- [ ] Logout command works
- [ ] After logout, user must re-authenticate
- [ ] Multiple users can have separate sessions

### ✅ Low-Risk Actions (No Step-Up)
- [ ] Browse products → Works immediately
- [ ] Check inventory → Works immediately
- [ ] Get recommendations → Works immediately
- [ ] Check loyalty points → Works immediately
- [ ] Reserve items → Works immediately
- [ ] Check order status → Works immediately

### ✅ High-Risk Actions (Step-Up Required)
- [ ] Payment > ₹10,000 → Requests confirmation → Requests OTP
- [ ] Payment < ₹10,000 → Requests confirmation → No OTP
- [ ] Refund request → Requests confirmation → Requests OTP
- [ ] Address change → Requests confirmation → Requests OTP
- [ ] Cancel step-up (reply NO) → Cancels action

### ✅ Edge Cases
- [ ] Invalid phone number → Error message
- [ ] Phone number not in database → Error message
- [ ] Expired OTP → Error message
- [ ] Multiple OTP attempts → Handles gracefully
- [ ] Unrelated message during auth flow → Handles gracefully

---

## Viewing Logs

### Backend Logs

The backend will log all activities. Watch for:
- Session creation/updates
- OTP generation
- Step-up authentication triggers
- Action risk detection

### Check Session State

You can check the database to see session state:

```sql
-- Connect to PostgreSQL
psql retail_agent_system

-- View all sessions
SELECT whatsapp_user_id, auth_state, customer_id, last_activity, expires_at 
FROM whatsapp_sessions;

-- View OTPs
SELECT whatsapp_user_id, phone_number, otp_code, expires_at, verified 
FROM whatsapp_otps 
ORDER BY created_at DESC 
LIMIT 10;
```

---

## Debugging Tips

### 1. Check if Backend is Running

```bash
curl http://localhost:8000/api/health
```

### 2. Check WhatsApp Endpoint

```bash
curl http://localhost:8000/whatsapp/health
```

### 3. View Real-Time Logs

Watch the backend terminal for detailed logs showing:
- Message received
- Session state
- OTP generation
- Step-up triggers
- Action risk detection

### 4. Common Issues

**Issue:** "Not Found" error
- **Solution:** Make sure backend is running and WhatsApp integration is mounted

**Issue:** OTP not working
- **Solution:** Check backend logs for the actual OTP (shown in DEV MODE)

**Issue:** Session not persisting
- **Solution:** Check database connection and session table

**Issue:** Step-up not triggering
- **Solution:** Check action risk detector patterns match your message

---

## Testing with Real WhatsApp (Optional)

If you have Twilio configured:

1. **Join Twilio Sandbox:**
   - Send "join [your-code]" to +1 415 523 8886

2. **Send Messages:**
   - Send "Hi" to the sandbox number
   - Follow the authentication flow

3. **Check Webhook:**
   - Make sure ngrok is running: `ngrok http 8000`
   - Update Twilio webhook URL to your ngrok URL

---

## Quick Test Commands

```bash
# Test health
curl http://localhost:8000/api/health

# Test first message
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{"sender_id": "whatsapp:+918850833367", "message_text": "Hi"}'

# Run full test suite
cd whatsapp_integration && python test_session_auth.py
```

---

## Next Steps

After testing:
1. ✅ Verify all scenarios work as expected
2. ✅ Check logs for any errors
3. ✅ Test with different phone numbers
4. ✅ Test session expiry (wait 24+ hours)
5. ✅ Test with real WhatsApp (if Twilio configured)

For more details, see `SESSION_BASED_AUTH.md`
