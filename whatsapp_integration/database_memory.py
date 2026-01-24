"""
In-Memory Database for WhatsApp Integration (Testing/Development)
Use this instead of database.py when PostgreSQL is not available
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from whatsapp_integration.models import AuthState, SessionInfo

logger = logging.getLogger(__name__)


class WhatsAppDatabaseMemory:
    """In-memory database handler for WhatsApp integration (no PostgreSQL needed)"""
    
    def __init__(self):
        """Initialize in-memory storage"""
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.otps: Dict[str, Dict[str, Any]] = {}
        logger.info("Using in-memory database (no PostgreSQL required)")
    
    def initialize_tables(self):
        """No-op for in-memory database"""
        logger.info("In-memory database initialized (no tables needed)")
        return True
    
    def get_session(self, whatsapp_user_id: str) -> Optional[SessionInfo]:
        """Get session information for a WhatsApp user"""
        if whatsapp_user_id not in self.sessions:
            return None
        
        session_data = self.sessions[whatsapp_user_id]
        return SessionInfo(
            whatsapp_user_id=whatsapp_user_id,
            customer_id=session_data.get('customer_id'),
            auth_state=AuthState(session_data.get('auth_state', 'unauthenticated')),
            phone_number=session_data.get('phone_number'),
            created_at=session_data.get('created_at', datetime.now()),
            last_activity=session_data.get('last_activity', datetime.now()),
            metadata=session_data.get('metadata', {})
        )
    
    def create_or_update_session(self, whatsapp_user_id: str, auth_state: AuthState,
                                phone_number: Optional[str] = None,
                                customer_id: Optional[str] = None,
                                metadata: Optional[Dict[str, Any]] = None) -> SessionInfo:
        """Create or update a WhatsApp session"""
        now = datetime.now()
        
        if whatsapp_user_id not in self.sessions:
            self.sessions[whatsapp_user_id] = {
                'created_at': now,
                'last_activity': now,
                'auth_state': auth_state.value,
                'phone_number': phone_number,
                'customer_id': customer_id,
                'metadata': metadata or {}
            }
        else:
            # Update existing session
            self.sessions[whatsapp_user_id].update({
                'auth_state': auth_state.value,
                'last_activity': now,
                'phone_number': phone_number or self.sessions[whatsapp_user_id].get('phone_number'),
                'customer_id': customer_id or self.sessions[whatsapp_user_id].get('customer_id'),
                'metadata': metadata or self.sessions[whatsapp_user_id].get('metadata', {})
            })
        
        return self.get_session(whatsapp_user_id)
    
    def store_otp(self, whatsapp_user_id: str, phone_number: str, otp_code: str,
                  expiry_minutes: int = 10) -> str:
        """Store OTP in memory"""
        otp_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(minutes=expiry_minutes)
        
        self.otps[otp_id] = {
            'whatsapp_user_id': whatsapp_user_id,
            'phone_number': phone_number,
            'otp_code': otp_code,
            'created_at': datetime.now(),
            'expires_at': expires_at,
            'verified': False,
            'attempts': 0,
            'max_attempts': 3
        }
        
        return otp_id
    
    def verify_otp(self, whatsapp_user_id: str, phone_number: str, otp_code: str) -> bool:
        """Verify OTP and mark as verified if valid"""
        now = datetime.now()
        
        # Find latest unverified OTP for this user/phone
        matching_otps = [
            (otp_id, otp_data) for otp_id, otp_data in self.otps.items()
            if (otp_data['whatsapp_user_id'] == whatsapp_user_id and
                otp_data['phone_number'] == phone_number and
                not otp_data['verified'] and
                otp_data['expires_at'] > now and
                otp_data['attempts'] < otp_data['max_attempts'])
        ]
        
        if not matching_otps:
            return False
        
        # Get the most recent OTP
        otp_id, otp_data = max(matching_otps, key=lambda x: x[1]['created_at'])
        
        # Increment attempts
        otp_data['attempts'] += 1
        
        # Verify OTP code
        if otp_data['otp_code'] == otp_code:
            otp_data['verified'] = True
            otp_data['verified_at'] = now
            return True
        
        return False
    
    def get_customer_by_phone(self, phone_number: str) -> Optional[str]:
        """Get customer ID by phone number (mock - returns test customer for testing)"""
        # In a real implementation, this would query the customers table
        # For testing without PostgreSQL, we'll return a test customer ID
        # This allows the OTP flow to complete for testing
        
        # Normalize phone number
        normalized = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Return a test customer ID (you can customize this)
        # Format: C-{last_10_digits}
        if len(normalized) >= 10:
            test_customer_id = f"C-{normalized[-10:]}"
            logger.info(f"Using test customer ID for {phone_number}: {test_customer_id}")
            return test_customer_id
        
        logger.warning(f"get_customer_by_phone called for {phone_number} - no valid customer found")
        return None
    
    def cleanup_expired_otps(self):
        """Clean up expired OTPs"""
        now = datetime.now()
        expired = [
            otp_id for otp_id, otp_data in self.otps.items()
            if otp_data['expires_at'] < now - timedelta(days=1)
        ]
        for otp_id in expired:
            del self.otps[otp_id]
        return len(expired)
    
    def cleanup_expired_sessions(self, expiry_days: int = 30):
        """Clean up expired sessions"""
        cutoff = datetime.now() - timedelta(days=expiry_days)
        expired = [
            user_id for user_id, session_data in self.sessions.items()
            if (session_data.get('auth_state') == 'unauthenticated' and
                session_data.get('last_activity', datetime.now()) < cutoff)
        ]
        for user_id in expired:
            del self.sessions[user_id]
        return len(expired)


# Global in-memory database instance
db_memory = WhatsAppDatabaseMemory()
