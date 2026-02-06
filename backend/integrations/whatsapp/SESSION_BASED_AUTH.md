# Session-Based Authentication with Step-Up Authentication

## Overview

This WhatsApp integration implements a secure, session-based authentication system with step-up authentication for high-risk actions. Users authenticate once via OTP and maintain persistent sessions, avoiding repeated logins.

## Key Features

### 1. **Session-Based Authentication**
- **First-Time Login**: Users authenticate once via OTP
- **Persistent Sessions**: Sessions persist for 24 hours (configurable)
- **Returning Users**: Valid sessions are automatically restored - no re-authentication needed
- **Welcome Back**: Returning users get a welcome message instead of OTP prompt

### 2. **Step-Up Authentication**
- **Low-Risk Actions**: No additional verification needed
  - Browsing products
  - Recommendations
  - Inventory checks
  - Reserving items
  - Order status checks
  - Loyalty points queries

- **High-Risk Actions**: Require step-up authentication
  - Payments (especially high-value)
  - Refunds
  - Address changes
  - Account modifications

### 3. **Smart Authentication Flow**

#### First-Time User Flow
```
User sends "Hi"
  ↓
System asks for phone number
  ↓
User enters phone number
  ↓
System generates and sends OTP
  ↓
User enters OTP
  ↓
Session created (24-hour expiry)
  ↓
User can now use the system
```

#### Returning User Flow
```
User sends "Hi" (with valid session)
  ↓
System: "👋 Welcome back! You're already logged in."
  ↓
User can immediately use the system
```

#### High-Risk Action Flow
```
User: "I want to pay ₹15,000"
  ↓
System: "⚠️ Security Check Required. Reply YES to continue."
  ↓
User: "YES"
  ↓
System checks:
  - Session age > 24 hours? → Request OTP
  - Payment > ₹10,000? → Request OTP
  - Otherwise → Just confirmation
  ↓
If OTP needed:
  System sends OTP
  User enters OTP
  ↓
Action proceeds
```

## Architecture

### Components

1. **Session Manager** (`session_manager.py`)
   - Manages user sessions
   - Handles session expiry
   - Tracks authentication state
   - Provides welcome-back messages

2. **Action Risk Detector** (`action_risk_detector.py`)
   - Detects high-risk actions in messages
   - Extracts payment amounts
   - Determines if step-up auth is needed

3. **Step-Up Auth Handler** (`stepup_auth.py`)
   - Handles step-up authentication flow
   - Requests confirmation
   - Manages OTP for step-up
   - Verifies step-up OTP

4. **Auth Handler** (`auth_handler.py`)
   - Handles initial OTP authentication
   - Manages first-time login flow
   - Checks for valid sessions before prompting

5. **Message Handler** (`message_handler.py`)
   - Routes messages to appropriate handlers
   - Checks session validity
   - Handles logout command
   - Integrates step-up authentication

### Session States

- `UNAUTHENTICATED`: No session or expired session
- `WAITING_FOR_PHONE`: Waiting for phone number input
- `WAITING_FOR_OTP`: Waiting for OTP verification
- `AUTHENTICATED`: Valid authenticated session
- `WAITING_FOR_STEPUP`: Waiting for step-up authentication
- `EXPIRED`: Session expired

### Authentication Levels

- `BASIC`: Standard authenticated session (for low-risk actions)
- `VERIFIED`: Verified session after step-up auth (for high-risk actions)

## Configuration

### Session Timeouts

```python
SESSION_TIMEOUT_HOURS = 24  # Session expiry time
INACTIVITY_TIMEOUT_HOURS = 48  # Inactivity timeout
```

### Risk Thresholds

```python
PAYMENT_RISK_THRESHOLD = 10000  # ₹10,000 - above this requires step-up
SESSION_AGE_FOR_STEPUP_HOURS = 24  # Sessions older than 24 hours need step-up
```

## Usage Examples

### Example 1: First-Time User
```
User: Hi
Bot: 👋 Hi! Welcome to our shopping assistant!
     To get started, I need to link your WhatsApp to your account.
     Please enter your registered mobile number (with country code, e.g., +1234567890):

User: +918850833367
Bot: ✅ Verification code sent to +918850833367
     [DEV MODE] Your OTP: 123456

User: 123456
Bot: ✅ Account linked successfully!
     You can now use our shopping assistant. How can I help you today?
```

### Example 2: Returning User
```
User: Hi
Bot: 👋 Welcome back!
     You're already logged in. How can I help you today?

User: Show me products
Bot: [Routes to orchestrator - shows products]
```

### Example 3: High-Risk Action (Payment)
```
User: I want to pay ₹15,000
Bot: ⚠️ Security Check Required
     You are about to proceed with a payment of ₹15,000.00.
     This is a high-value transaction. For your security, we need to verify your identity.
     Reply 'YES' to continue, or 'NO' to cancel.

User: YES
Bot: ✅ Verification code sent to +918850833367
     Please enter the 6-digit code to proceed.
     [DEV MODE] Your OTP: 654321

User: 654321
Bot: ✅ Verification successful!
     Proceeding with your request...
     [Routes to payment agent]
```

### Example 4: Low-Risk Action (No Step-Up)
```
User: Show me recommendations
Bot: [Routes to orchestrator - shows recommendations]
     (No step-up authentication needed)
```

### Example 5: Logout
```
User: logout
Bot: ✅ You have been logged out. Send 'Hi' to log in again.
```

## Security Features

1. **Session Expiry**: Sessions automatically expire after 24 hours
2. **Inactivity Timeout**: Sessions expire after 48 hours of inactivity
3. **Step-Up for High-Risk**: High-risk actions require additional verification
4. **OTP Expiry**: OTPs expire after 10 minutes
5. **No Credential Storage**: No passwords or sensitive data stored in messages
6. **Session Isolation**: Each WhatsApp user has an isolated session

## Database Schema

### whatsapp_sessions Table
- `whatsapp_user_id`: Unique WhatsApp user identifier
- `customer_id`: Linked customer ID
- `auth_state`: Current authentication state
- `auth_level`: Authentication level (BASIC/VERIFIED) - stored in metadata
- `phone_number`: User's phone number
- `expires_at`: Session expiry timestamp
- `last_activity`: Last activity timestamp
- `metadata`: JSONB field for additional data (auth_level, stepup_action, etc.)

## Testing

### Test Scenarios

1. **First-Time Login**
   - Send "Hi" → Should ask for phone number
   - Enter phone number → Should send OTP
   - Enter OTP → Should authenticate

2. **Returning User**
   - Send "Hi" with valid session → Should welcome back
   - Should NOT ask for OTP

3. **High-Risk Action**
   - Send payment request → Should request confirmation
   - Confirm → Should request OTP if needed
   - Enter OTP → Should proceed

4. **Low-Risk Action**
   - Send browsing request → Should proceed immediately
   - Should NOT request step-up

5. **Session Expiry**
   - Wait 24+ hours → Session should expire
   - Send message → Should ask to re-authenticate

6. **Logout**
   - Send "logout" → Should invalidate session
   - Send message → Should ask to re-authenticate

## Implementation Notes

- **Modular Design**: Each component is independent and testable
- **Database Fallback**: Uses in-memory database if PostgreSQL unavailable
- **Error Handling**: Graceful error handling throughout
- **Logging**: Comprehensive logging for debugging
- **Extensible**: Easy to add new risk patterns or authentication methods

## Future Enhancements

1. **Biometric Authentication**: Add fingerprint/face recognition for step-up
2. **Risk Scoring**: Dynamic risk scoring based on user behavior
3. **Multi-Factor Auth**: Additional factors for very high-risk actions
4. **Session Sharing**: Share sessions across devices
5. **Remember Device**: Skip step-up for trusted devices
