"""
Session Manager - Manage WhatsApp user sessions and authentication state
"""
import logging
from typing import Optional
from datetime import datetime, timedelta

from whatsapp_integration.database import db
from whatsapp_integration.models import SessionInfo, AuthState
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages WhatsApp user sessions and authentication state"""
    
    SESSION_TIMEOUT_HOURS = 24  # Authenticated session timeout
    AUTH_FLOW_TIMEOUT_MINUTES = 15  # Authentication flow timeout
    INACTIVITY_TIMEOUT_HOURS = 48  # Inactivity timeout (longer than session timeout)
    
    def get_session(self, whatsapp_user_id: str) -> Optional[SessionInfo]:
        """Get session information for a WhatsApp user"""
        return db.get_session(whatsapp_user_id)
    
    def create_session(self, whatsapp_user_id: str, auth_state: AuthState = AuthState.UNAUTHENTICATED,
                       phone_number: Optional[str] = None) -> SessionInfo:
        """Create a new session"""
        return db.create_or_update_session(
            whatsapp_user_id=whatsapp_user_id,
            auth_state=auth_state,
            phone_number=phone_number
        )
    
    def update_session_state(self, whatsapp_user_id: str, auth_state: AuthState,
                            phone_number: Optional[str] = None,
                            customer_id: Optional[str] = None,
                            expires_at: Optional[datetime] = None,
                            metadata: Optional[Dict[str, Any]] = None) -> SessionInfo:
        """Update session authentication state"""
        return db.create_or_update_session(
            whatsapp_user_id=whatsapp_user_id,
            auth_state=auth_state,
            phone_number=phone_number,
            customer_id=customer_id,
            expires_at=expires_at,
            metadata=metadata
        )
    
    def authenticate_session(self, whatsapp_user_id: str, customer_id: str,
                            phone_number: Optional[str] = None,
                            auth_level: str = "BASIC") -> SessionInfo:
        """Mark session as authenticated and link to customer"""
        # Set expiry time
        expires_at = datetime.now() + timedelta(hours=self.SESSION_TIMEOUT_HOURS)
        
        return db.create_or_update_session(
            whatsapp_user_id=whatsapp_user_id,
            auth_state=AuthState.AUTHENTICATED,
            customer_id=customer_id,
            phone_number=phone_number,
            expires_at=expires_at,
            metadata={"auth_level": auth_level}
        )
    
    def is_authenticated(self, whatsapp_user_id: str) -> bool:
        """Check if user is authenticated with a valid session"""
        session = self.get_session(whatsapp_user_id)
        if not session:
            return False
        
        # Check if session is authenticated and not expired
        if session.auth_state == AuthState.AUTHENTICATED:
            # Check session expiry
            if session.expires_at and datetime.now() > session.expires_at:
                # Session expired
                self.update_session_state(whatsapp_user_id, AuthState.EXPIRED)
                return False
            
            # Check inactivity timeout
            if session.last_activity:
                inactivity_timeout = timedelta(hours=self.INACTIVITY_TIMEOUT_HOURS)
                if (datetime.now() - session.last_activity) > inactivity_timeout:
                    # Session expired due to inactivity
                    self.update_session_state(whatsapp_user_id, AuthState.EXPIRED)
                    return False
            
            return True
        
        return False
    
    def is_valid_session(self, whatsapp_user_id: str) -> bool:
        """Check if user has a valid session (authenticated and not expired)"""
        return self.is_authenticated(whatsapp_user_id)
    
    def get_auth_level(self, whatsapp_user_id: str) -> Optional[str]:
        """Get authentication level (BASIC or VERIFIED)"""
        session = self.get_session(whatsapp_user_id)
        if session and self.is_authenticated(whatsapp_user_id):
            # Check metadata for auth_level
            metadata = session.metadata or {}
            return metadata.get("auth_level", "BASIC")
        return None
    
    def get_customer_id(self, whatsapp_user_id: str) -> Optional[str]:
        """Get customer ID for authenticated session"""
        session = self.get_session(whatsapp_user_id)
        if session and session.auth_state == AuthState.AUTHENTICATED:
            return session.customer_id
        return None
    
    def start_auth_flow(self, whatsapp_user_id: str) -> SessionInfo:
        """Start authentication flow - request phone number"""
        session = self.create_session(whatsapp_user_id, AuthState.WAITING_FOR_PHONE)
        logger.info(f"Started auth flow for {whatsapp_user_id}")
        return session
    
    def request_otp(self, whatsapp_user_id: str, phone_number: str) -> SessionInfo:
        """Move to OTP verification state"""
        session = self.update_session_state(
            whatsapp_user_id=whatsapp_user_id,
            auth_state=AuthState.WAITING_FOR_OTP,
            phone_number=phone_number
        )
        logger.info(f"Requested OTP for {whatsapp_user_id} / {phone_number}")
        return session
    
    def complete_auth_flow(self, whatsapp_user_id: str, customer_id: str,
                          phone_number: str) -> SessionInfo:
        """Complete authentication flow - link WhatsApp user to customer"""
        session = self.authenticate_session(
            whatsapp_user_id=whatsapp_user_id,
            customer_id=customer_id,
            phone_number=phone_number
        )
        logger.info(f"Completed auth flow for {whatsapp_user_id} -> {customer_id}")
        return session
    
    def reset_auth_flow(self, whatsapp_user_id: str) -> SessionInfo:
        """Reset authentication flow - start over"""
        return self.update_session_state(
            whatsapp_user_id=whatsapp_user_id,
            auth_state=AuthState.UNAUTHENTICATED
        )
    
    def invalidate_session(self, whatsapp_user_id: str) -> SessionInfo:
        """Invalidate session - logout user"""
        return self.update_session_state(
            whatsapp_user_id=whatsapp_user_id,
            auth_state=AuthState.UNAUTHENTICATED
        )
    
    def update_last_activity(self, whatsapp_user_id: str) -> Optional[SessionInfo]:
        """Update last activity timestamp for session"""
        session = self.get_session(whatsapp_user_id)
        if session:
            return db.create_or_update_session(
                whatsapp_user_id=whatsapp_user_id,
                auth_state=session.auth_state,
                customer_id=session.customer_id,
                phone_number=session.phone_number
            )
        return None
    
    def get_welcome_back_message(self, whatsapp_user_id: str) -> Optional[str]:
        """Get welcome back message for returning user"""
        session = self.get_session(whatsapp_user_id)
        if session and session.customer_id:
            return (
                f"👋 Welcome back!\n\n"
                f"You're already logged in. How can I help you today?\n\n"
                f"Try asking:\n"
                f"• 'Show me products'\n"
                f"• 'Check my order status'\n"
                f"• 'What are my loyalty points?'\n"
                f"• Or any other shopping question!"
            )
        return None


# Global session manager instance
session_manager = SessionManager()
