# WhatsApp Integration - Architecture Overview

## Overview

The WhatsApp integration module provides a **channel-agnostic** messaging interface with OTP-based authentication. It acts as a bridge between WhatsApp users and the existing Master Agent (Orchestrator) system.

## Key Design Principles

### 1. Channel Agnostic
- Core authentication and session management logic is separate from WhatsApp-specific code
- Easy to extend to other channels (web chat, kiosk, voice assistants)
- Message routing logic is channel-independent

### 2. Loose Coupling
- WhatsApp integration does NOT hardcode logic inside agents
- All intelligence lives in the Orchestrator and Worker Agents
- WhatsApp acts purely as a communication channel

### 3. Modular Design
- Each component has a single responsibility
- Clear separation of concerns
- Easy to test and maintain

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     WhatsApp User                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ WhatsApp Messages
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              WhatsApp Business API                               │
│              (External Service)                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Webhook (POST)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              WhatsApp Webhook Interface                          │
│              (webhook.py)                                        │
│              - Verification (GET)                                │
│              - Message Reception (POST)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ WhatsAppMessage
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Message Handler                                     │
│              (message_handler.py)                                │
│              - Route based on auth state                         │
└──────────┬──────────────────────────────┬───────────────────────┘
           │                              │
           │ Not Authenticated            │ Authenticated
           ▼                              ▼
┌──────────────────────────┐  ┌──────────────────────────────────┐
│   Auth Handler           │  │   Orchestrator (Master Agent)    │
│   (auth_handler.py)      │  │   - Analyze intent                │
│   - OTP Flow             │  │   - Route to worker agents        │
│   - Phone Collection     │  └──────────┬───────────────────────┘
└──────────┬───────────────┘             │
           │                              │
           │                              │ Route based on intent
           │                              ▼
           │              ┌──────────────────────────────────────┐
           │              │   Worker Agents                      │
           │              │   - Inventory Agent                  │
           │              │   - Payment Agent                    │
           │              │   - Loyalty Agent                    │
           │              │   - Support Agent                    │
           │              │   - Recommendation Agent             │
           │              └──────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│              Session Manager                                     │
│              (session_manager.py)                                │
│              - Track auth state                                  │
│              - Link WhatsApp ID to Customer ID                   │
└──────────┬──────────────────────────────┬───────────────────────┘
           │                              │
           │                              │
           ▼                              ▼
┌──────────────────────────┐  ┌──────────────────────────────────┐
│   OTP Service            │  │   Database                       │
│   (otp_service.py)       │  │   (database.py)                  │
│   - Generate OTP         │  │   - whatsapp_sessions            │
│   - Send OTP (mock)      │  │   - whatsapp_otps                │
│   - Validate OTP         │  │   - customers (existing)         │
└──────────────────────────┘  └──────────────────────────────────┘
```

## Component Responsibilities

### 1. Webhook Interface (`webhook.py`)
- **Purpose**: Receive WhatsApp messages from WhatsApp Business API
- **Responsibilities**:
  - Webhook verification (GET endpoint)
  - Message reception (POST endpoint)
  - Parse WhatsApp webhook payload
  - Return responses

### 2. Message Handler (`message_handler.py`)
- **Purpose**: Route messages based on authentication state
- **Responsibilities**:
  - Check if user is authenticated
  - Route to Auth Handler (if not authenticated)
  - Route to Orchestrator (if authenticated)
  - Handle errors gracefully

### 3. Auth Handler (`auth_handler.py`)
- **Purpose**: Handle complete OTP-based authentication flow
- **Responsibilities**:
  - Detect greetings ("Hi", "Hello")
  - Request phone number
  - Request OTP generation
  - Validate OTP codes
  - Link WhatsApp user to customer account
  - Handle edge cases (cancel, retry, invalid input)

### 4. Session Manager (`session_manager.py`)
- **Purpose**: Manage user sessions and authentication state
- **Responsibilities**:
  - Track authentication state (unauthenticated, waiting_for_phone, waiting_for_otp, authenticated)
  - Link WhatsApp user ID to customer ID
  - Handle session lifecycle (create, update, expire)
  - Check if user is authenticated

### 5. OTP Service (`otp_service.py`)
- **Purpose**: Generate, store, and validate OTPs
- **Responsibilities**:
  - Generate 6-digit OTP codes
  - Store OTPs with expiry timestamps
  - Send OTP via WhatsApp (mock implementation - replace in production)
  - Validate OTP codes
  - Handle OTP expiry and attempts

### 6. Database (`database.py`)
- **Purpose**: Data persistence for sessions and OTPs
- **Responsibilities**:
  - Create database tables
  - Store and retrieve sessions
  - Store and retrieve OTPs
  - Link WhatsApp user IDs to customer IDs
  - Clean up expired data

## Authentication Flow

### State Machine

```
UNAUTHENTICATED
    │
    │ User sends "Hi"
    ▼
WAITING_FOR_PHONE
    │
    │ User sends phone number
    ▼
WAITING_FOR_OTP
    │
    │ User sends OTP code
    ▼
AUTHENTICATED
    │
    │ Messages routed to Orchestrator
    ▼
[Continue using system]
```

### Detailed Flow

1. **User sends greeting** ("Hi", "Hello")
   - Auth Handler detects greeting
   - Session created with state: `WAITING_FOR_PHONE`
   - Bot requests phone number

2. **User sends phone number**
   - Phone number validated
   - Customer lookup in database
   - If found: OTP generated and sent
   - Session updated to state: `WAITING_FOR_OTP`
   - If not found: Error message, ask to retry

3. **User sends OTP code**
   - OTP validated against database
   - Check expiry and attempts
   - If valid: Customer ID linked to WhatsApp user ID
   - Session updated to state: `AUTHENTICATED`
   - If invalid: Error message, allow retry

4. **User sends shopping query**
   - Message Handler checks: authenticated = true
   - Message routed to Orchestrator
   - Orchestrator analyzes intent and routes to worker agents
   - Response sent back to WhatsApp user

## Edge Case Handling

### 1. Abandoned OTP Flow
- User can send `cancel` or `start over` at any time
- Auth flow resets to `UNAUTHENTICATED`
- Clear messaging about next steps

### 2. Invalid Phone Number
- Validation checks phone format
- Clear error message with example format
- Allow retry

### 3. Invalid OTP
- Tracks attempt count (max 3 attempts)
- Clear error message
- Allow retry or resend
- OTP expiry after 10 minutes (configurable)

### 4. Unrelated Messages During Auth
- Clear prompts to continue auth flow
- Option to cancel and start over
- Prevents confusion

### 5. Session Timeout
- Authenticated sessions expire after 24 hours (configurable)
- User can send "Hi" to re-authenticate
- Session state updated to `EXPIRED`

### 6. Payment/Inventory Failures
- Handled gracefully by Orchestrator
- Error messages returned to user via WhatsApp
- User can retry or ask for help

## Database Schema

### whatsapp_sessions
Stores user sessions and authentication state.

**Key Fields**:
- `whatsapp_user_id`: WhatsApp user ID (phone number with country code)
- `customer_id`: Linked customer ID (foreign key to customers table)
- `auth_state`: Current authentication state
- `phone_number`: Phone number used for authentication
- `last_activity`: Last activity timestamp (for session timeout)

### whatsapp_otps
Stores OTP codes with expiry and verification status.

**Key Fields**:
- `whatsapp_user_id`: WhatsApp user ID
- `phone_number`: Phone number OTP was sent to
- `otp_code`: 6-digit OTP code
- `expires_at`: OTP expiry timestamp
- `verified`: Whether OTP was verified
- `attempts`: Number of verification attempts

## Extension Points

### Adding New Channels

To add a new channel (e.g., web chat):

1. Create new webhook interface (similar to `webhook.py`)
2. Reuse existing components:
   - `message_handler.py` - Message routing
   - `auth_handler.py` - Authentication flow
   - `session_manager.py` - Session management
   - `otp_service.py` - OTP handling
   - `database.py` - Data persistence

3. Update channel-specific logic:
   - OTP delivery method (SMS, email, in-app, etc.)
   - Message format (plain text, rich media, etc.)
   - User ID format (phone number, email, user ID, etc.)

### Adding New Authentication Methods

To add new authentication methods:

1. Extend `AuthState` enum in `models.py`
2. Update `auth_handler.py` to handle new states
3. Update `session_manager.py` to manage new states
4. Modify OTP service or add new auth service (e.g., email link, magic link)

## Security Considerations

1. **OTP Security**:
   - OTPs expire after 10 minutes
   - Limited attempts (3 max)
   - OTPs are single-use (verified = true after use)

2. **Session Security**:
   - Sessions expire after 24 hours of inactivity
   - Session timeout enforced
   - Customer ID linking validated against database

3. **Webhook Security**:
   - Webhook verification token required
   - Validate sender authenticity (in production)
   - Rate limiting (recommended)

4. **Data Privacy**:
   - OTPs stored with expiry
   - Old OTPs cleaned up automatically
   - Session data linked to customer accounts

## Production Checklist

- [ ] Replace mock OTP service with real WhatsApp Business API
- [ ] Configure secure webhook verification token
- [ ] Set `ENVIRONMENT=production` to hide OTP codes
- [ ] Set up periodic cleanup jobs for expired data
- [ ] Implement rate limiting on webhook endpoints
- [ ] Add monitoring and logging
- [ ] Set up error alerting
- [ ] Test complete authentication flow
- [ ] Test with real WhatsApp Business API
- [ ] Load test webhook endpoints
- [ ] Set up database backups
- [ ] Document deployment process

## Future Enhancements

1. **Multi-channel Support**: Extend to web chat, voice, etc.
2. **Rich Media**: Handle images, videos, documents
3. **Message Templates**: Reusable message templates
4. **Analytics**: Track success rates, common queries
5. **Human Handoff**: Integration with live chat
6. **Multi-language**: Support multiple languages
7. **Voice OTP**: Voice-based OTP delivery
8. **Biometric Auth**: Fingerprint/face recognition for trusted devices
