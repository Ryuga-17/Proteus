# WhatsApp Integration Module

Channel-agnostic messaging interface with OTP-based authentication for the Agentic AI system.

## Overview

This module provides a WhatsApp integration layer that acts as a communication channel between users and the Master Agent (Orchestrator). It handles:

- **WhatsApp Webhook Interface**: Receives incoming WhatsApp messages
- **OTP-based Authentication**: Secure account linking via one-time passwords
- **Session Management**: Maintains authenticated sessions across messages
- **Message Routing**: Routes authenticated messages to the Master Agent
- **Edge Case Handling**: Handles abandoned flows, invalid inputs, and errors gracefully

## Architecture

The integration is designed to be **channel-agnostic** - the core logic (authentication, session management, message routing) is separate from the WhatsApp-specific webhook interface. This allows easy extension to other channels (web chat, kiosk, voice).

```
WhatsApp User → WhatsApp Business API → Webhook → Message Handler
                                                         ↓
                                              ┌──────────┴──────────┐
                                              ↓                     ↓
                                    Auth Handler         Orchestrator (Master Agent)
                                    (OTP Flow)                  ↓
                                                          Worker Agents
```

## Components

### 1. Database (`database.py`)
- Manages WhatsApp sessions and OTP storage
- Links WhatsApp user IDs to customer IDs
- Handles OTP verification and expiry

### 2. OTP Service (`otp_service.py`)
- Generates 6-digit OTPs
- Stores OTPs with expiry timestamps
- Validates OTP codes
- Mock SMS service (replace with real WhatsApp Business API in production)

### 3. Session Manager (`session_manager.py`)
- Tracks user authentication state
- Manages session lifecycle
- Links WhatsApp user IDs to customer accounts

### 4. Auth Handler (`auth_handler.py`)
- Handles complete OTP-based authentication flow
- Processes phone number collection
- Manages OTP verification
- Handles edge cases (cancellations, retries, etc.)

### 5. Message Handler (`message_handler.py`)
- Routes messages based on authentication state
- Handles authenticated messages → routes to Orchestrator
- Handles unauthenticated messages → routes to Auth Handler

### 6. Webhook Interface (`webhook.py`)
- FastAPI endpoints for WhatsApp Business API
- Webhook verification (GET)
- Message reception (POST)
- Simulation endpoint for testing

## Setup

### 1. Database Setup

The module automatically creates required tables on initialization:

```sql
-- whatsapp_sessions: Stores user sessions and authentication state
-- whatsapp_otps: Stores OTP codes with expiry
```

These tables are created automatically when you call `initialize_whatsapp_integration()`.

### 2. Environment Variables

Add to your `.env` file:

```env
# Database Configuration (if not already set)
DB_HOST=localhost
DB_NAME=retail_agent_system
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432

# WhatsApp Webhook Verification Token
WHATSAPP_WEBHOOK_TOKEN=your_secure_token_here

# Environment (development/production)
ENVIRONMENT=development  # In dev mode, OTP is returned in response for testing
```

### 3. Integration with Backend

The module is already integrated into `backend/main.py`. The WhatsApp endpoints are mounted at `/whatsapp/*`:

- `GET /whatsapp/webhook` - Webhook verification
- `POST /whatsapp/webhook` - Receive messages
- `POST /whatsapp/simulate/message` - Test endpoint

## Usage

### Testing with Simulation Endpoint

```bash
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "+1234567890",
    "message_text": "Hi"
  }'
```

### Authentication Flow

1. **User sends "Hi"** → System requests phone number
2. **User sends phone number** → System generates and sends OTP
3. **User sends OTP code** → System verifies and links account
4. **User sends shopping queries** → System routes to Orchestrator → Worker Agents

### Example Conversation

```
User: Hi
Bot: 👋 Hi! Welcome to our shopping assistant!
     To get started, I need to link your WhatsApp to your account.
     Please enter your registered mobile number (with country code, e.g., +1234567890):

User: +1234567890
Bot: ✅ An OTP has been sent to +1234567890. Please enter the 6-digit code to verify your account.
     [DEV MODE] Your OTP: 123456

User: 123456
Bot: ✅ Account linked successfully!
     You can now use our shopping assistant. How can I help you today?
     Try asking:
     • 'Show me products'
     • 'Check my order status'
     • 'What are my loyalty points?'
     • Or any other shopping question!

User: Show me red shirts
Bot: [Response from Orchestrator → Recommendation Agent]
```

## API Endpoints

### GET `/whatsapp/webhook`
WhatsApp Business API webhook verification endpoint.

**Query Parameters:**
- `hub_mode`: Should be "subscribe"
- `hub_verify_token`: Must match `WHATSAPP_WEBHOOK_TOKEN`
- `hub_challenge`: Challenge string to return

### POST `/whatsapp/webhook`
Receive incoming WhatsApp messages.

**Request Body:** (WhatsApp Business API format)

**Response:**
```json
{
  "success": true,
  "message": "Message processed successfully",
  "response_text": "Response text to send to user"
}
```

### POST `/whatsapp/simulate/message`
Test endpoint for simulating WhatsApp messages.

**Request Body:**
```json
{
  "sender_id": "+1234567890",
  "message_text": "Hi"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Message processed successfully",
  "response_text": "Response text"
}
```

## Production Deployment

### 1. Replace Mock OTP Service

In `otp_service.py`, replace the mock SMS function with actual WhatsApp Business API integration:

```python
def send_otp(self, whatsapp_user_id: str, phone_number: str, otp_code: str) -> bool:
    # Integrate with:
    # - WhatsApp Business API (official)
    # - Twilio WhatsApp API
    # - Your SMS gateway provider
    
    from twilio.rest import Client
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=f"Your verification code is: {otp_code}",
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{phone_number}'
    )
    
    return message.status == 'queued'
```

### 2. Configure Webhook Verification Token

Set `WHATSAPP_WEBHOOK_TOKEN` in your production environment variables and configure it in WhatsApp Business API settings.

### 3. Set Production Mode

Set `ENVIRONMENT=production` to disable returning OTP codes in responses.

### 4. Schedule Cleanup Jobs

Set up periodic cleanup of expired OTPs and sessions:

```python
from whatsapp_integration.main import cleanup_expired_data
import schedule
import time

# Run cleanup daily
schedule.every().day.at("02:00").do(cleanup_expired_data)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

## Architecture Benefits

### 1. Channel Agnostic
The authentication flow, session management, and message routing logic are completely separate from WhatsApp-specific code. This makes it easy to add:
- Web chat interface
- Kiosk integration
- Voice assistants
- Other messaging platforms

### 2. Modular Design
Each component has a single responsibility:
- `database.py` - Data persistence
- `otp_service.py` - OTP generation/validation
- `session_manager.py` - Session state
- `auth_handler.py` - Authentication flow
- `message_handler.py` - Message routing
- `webhook.py` - Channel interface

### 3. Loose Coupling
The WhatsApp integration doesn't hardcode logic inside agents. All intelligence lives in the Orchestrator and Worker Agents, just as designed.

## Edge Case Handling

The module handles various edge cases:

1. **Abandoned OTP Flow**: Users can send `cancel` or `start over` at any time
2. **Invalid Inputs**: Clear error messages for invalid phone numbers or OTP codes
3. **OTP Expiry**: Automatic expiry after configured time (default 10 minutes)
4. **Max Attempts**: Limits OTP verification attempts (default 3)
5. **Session Timeout**: Authenticated sessions expire after configured time (default 24 hours)
6. **Unrelated Messages During Auth**: Clear prompts to continue auth flow or cancel
7. **Payment/Inventory Failures**: Gracefully handled by Orchestrator and returned to user

## Testing

Run the initialization script to set up database tables:

```bash
cd whatsapp_integration
python main.py
```

Test the integration:

```bash
# Start backend
cd backend
python main.py

# In another terminal, test simulation endpoint
curl -X POST "http://localhost:8000/whatsapp/simulate/message" \
  -H "Content-Type: application/json" \
  -d '{"sender_id": "+1234567890", "message_text": "Hi"}'
```

## Dependencies

See `requirements.txt`:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `psycopg2-binary` - PostgreSQL driver
- `pydantic` - Data validation
- `python-dotenv` - Environment variables

## Future Enhancements

1. **Multi-channel Support**: Extend to web chat, voice, etc.
2. **Rich Media Support**: Handle images, videos, documents
3. **Message Queue**: Add async message processing
4. **Analytics**: Track authentication success rates, common queries
5. **Human Handoff**: Integration with live chat support
6. **Message Templates**: Reusable message templates for common responses

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database tables exist (run `initialize_whatsapp_integration()`)

### OTP Not Working
- Check database connection
- Verify phone number format (must include country code)
- Check OTP expiry time (default 10 minutes)
- In dev mode, check response for test OTP code

### Messages Not Routing to Orchestrator
- Verify user is authenticated (check session state)
- Check Orchestrator import path
- Review logs for routing errors

## License

Part of the Complete System Techathon project.
