-- ============================================================================
-- WhatsApp Integration - Database Schema
-- ============================================================================
-- These tables are automatically created by the WhatsApp integration module
-- Run initialize_whatsapp_integration() to create them
-- ============================================================================

-- WhatsApp Sessions Table
-- Stores user sessions and authentication state
CREATE TABLE IF NOT EXISTS whatsapp_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    whatsapp_user_id VARCHAR(50) UNIQUE NOT NULL,
    customer_id VARCHAR(50) REFERENCES customers(customer_id) ON DELETE SET NULL,
    auth_state VARCHAR(50) NOT NULL DEFAULT 'unauthenticated',
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    CONSTRAINT valid_auth_state CHECK (auth_state IN (
        'unauthenticated', 
        'waiting_for_phone', 
        'waiting_for_otp', 
        'authenticated', 
        'expired'
    ))
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_user_id 
ON whatsapp_sessions(whatsapp_user_id);

CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_customer_id 
ON whatsapp_sessions(customer_id);

CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_auth_state 
ON whatsapp_sessions(auth_state);

CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_last_activity 
ON whatsapp_sessions(last_activity);


-- WhatsApp OTPs Table
-- Stores OTP codes with expiry and verification status
CREATE TABLE IF NOT EXISTS whatsapp_otps (
    otp_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    whatsapp_user_id VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_otps_user_phone 
ON whatsapp_otps(whatsapp_user_id, phone_number);

CREATE INDEX IF NOT EXISTS idx_whatsapp_otps_expires 
ON whatsapp_otps(expires_at);

CREATE INDEX IF NOT EXISTS idx_whatsapp_otps_verified 
ON whatsapp_otps(verified);

CREATE INDEX IF NOT EXISTS idx_whatsapp_otps_code 
ON whatsapp_otps(otp_code);


-- ============================================================================
-- Triggers
-- ============================================================================

-- Update last_activity timestamp on session update
CREATE OR REPLACE FUNCTION update_whatsapp_session_activity()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_activity = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_whatsapp_sessions_activity 
BEFORE UPDATE ON whatsapp_sessions 
FOR EACH ROW 
EXECUTE FUNCTION update_whatsapp_session_activity();


-- ============================================================================
-- Views
-- ============================================================================

-- View: Active authenticated sessions
CREATE OR REPLACE VIEW v_active_whatsapp_sessions AS
SELECT 
    s.session_id,
    s.whatsapp_user_id,
    s.customer_id,
    c.name AS customer_name,
    c.email AS customer_email,
    s.phone_number,
    s.auth_state,
    s.created_at,
    s.last_activity,
    CASE 
        WHEN s.last_activity < CURRENT_TIMESTAMP - INTERVAL '24 hours' 
        THEN TRUE 
        ELSE FALSE 
    END AS is_expired
FROM whatsapp_sessions s
LEFT JOIN customers c ON s.customer_id = c.customer_id
WHERE s.auth_state = 'authenticated'
  AND s.last_activity > CURRENT_TIMESTAMP - INTERVAL '24 hours';


-- View: Pending OTPs (not verified, not expired)
CREATE OR REPLACE VIEW v_pending_whatsapp_otps AS
SELECT 
    otp_id,
    whatsapp_user_id,
    phone_number,
    created_at,
    expires_at,
    attempts,
    max_attempts,
    EXTRACT(EPOCH FROM (expires_at - CURRENT_TIMESTAMP)) / 60 AS minutes_remaining
FROM whatsapp_otps
WHERE verified = FALSE
  AND expires_at > CURRENT_TIMESTAMP
  AND attempts < max_attempts;
