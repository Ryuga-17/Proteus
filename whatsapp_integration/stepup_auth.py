"""
Step-Up Authentication Handler - Handles step-up authentication for high-risk actions
"""
import logging
from typing import Optional, Tuple, Dict, Any
from datetime import datetime, timedelta

from whatsapp_integration.models import WhatsAppMessage, WhatsAppResponse, AuthState
from whatsapp_integration.session_manager import session_manager
from whatsapp_integration.otp_service import otp_service
from whatsapp_integration.action_risk_detector import action_risk_detector

logger = logging.getLogger(__name__)


class StepUpAuthHandler:
    """Handles step-up authentication for high-risk actions"""
    
    STEPUP_CONFIRMATION_TIMEOUT_MINUTES = 5  # Timeout for confirmation
    STEPUP_OTP_EXPIRY_MINUTES = 10  # OTP expiry for step-up
    
    def check_stepup_required(self, message: WhatsAppMessage, session_info: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Check if step-up authentication is required for this message
        
        Args:
            message: User's message
            session_info: Current session information
        
        Returns:
            Tuple of (requires_stepup, action_details)
        """
        # Check if already in step-up flow
        if session_info.get("auth_state") == AuthState.WAITING_FOR_STEPUP:
            return True, session_info.get("metadata", {}).get("stepup_action")
        
        # Detect action risk
        requires_stepup, action_details = action_risk_detector.requires_stepup(
            message.message_text,
            session_info
        )
        
        return requires_stepup, action_details
    
    def handle_stepup_flow(self, message: WhatsAppMessage, action_details: Dict[str, Any]) -> WhatsAppResponse:
        """
        Handle step-up authentication flow
        
        Args:
            message: User's message
            action_details: Details about the high-risk action
        
        Returns:
            Response to send to user
        """
        whatsapp_user_id = message.sender_id
        message_text = message.message_text.strip().upper()
        session = session_manager.get_session(whatsapp_user_id)
        
        if not session:
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text="❌ Session error. Please send 'Hi' to restart."
            )
        
        # Check current step-up state
        auth_state = session.auth_state
        
        if auth_state != AuthState.WAITING_FOR_STEPUP:
            # Start step-up flow - ask for confirmation
            return self._request_confirmation(whatsapp_user_id, action_details)
        
        # Already in step-up flow - check for confirmation or OTP
        if message_text in ["YES", "Y", "CONFIRM", "PROCEED"]:
            # User confirmed - check if OTP is needed
            return self._request_otp_if_needed(whatsapp_user_id, action_details)
        elif message_text in ["NO", "N", "CANCEL"]:
            # User cancelled
            session_manager.update_session_state(
                whatsapp_user_id,
                AuthState.AUTHENTICATED,
                customer_id=session.customer_id,
                phone_number=session.phone_number
            )
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text="✅ Action cancelled. How can I help you?"
            )
        elif self._looks_like_otp(message_text):
            # User entered OTP
            return self._verify_stepup_otp(whatsapp_user_id, message_text, action_details)
        else:
            # Invalid input
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text=(
                    "Please reply 'YES' to confirm and proceed, or 'NO' to cancel.\n"
                    "Or enter the OTP code if you've already received it."
                )
            )
    
    def _request_confirmation(self, whatsapp_user_id: str, action_details: Dict[str, Any]) -> WhatsAppResponse:
        """Request confirmation for high-risk action"""
        action_type = action_details.get("type", "action")
        amount = action_details.get("amount")
        
        # Build confirmation message
        if action_type == "payment" and amount:
            confirmation_text = (
                f"⚠️ **Security Check Required**\n\n"
                f"You are about to proceed with a payment of ₹{amount:,.2f}.\n\n"
                f"This is a high-value transaction. For your security, we need to verify your identity.\n\n"
                f"Reply 'YES' to continue, or 'NO' to cancel."
            )
        elif action_type == "refund":
            confirmation_text = (
                f"⚠️ **Security Check Required**\n\n"
                f"You are about to request a refund.\n\n"
                f"For your security, we need to verify your identity.\n\n"
                f"Reply 'YES' to continue, or 'NO' to cancel."
            )
        elif action_type == "address_change":
            confirmation_text = (
                f"⚠️ **Security Check Required**\n\n"
                f"You are about to change your delivery address.\n\n"
                f"For your security, we need to verify your identity.\n\n"
                f"Reply 'YES' to continue, or 'NO' to cancel."
            )
        else:
            confirmation_text = (
                f"⚠️ **Security Check Required**\n\n"
                f"This action requires additional verification.\n\n"
                f"Reply 'YES' to continue, or 'NO' to cancel."
            )
        
        # Update session to waiting for step-up confirmation
        session = session_manager.get_session(whatsapp_user_id)
        session_manager.update_session_state(
            whatsapp_user_id,
            AuthState.WAITING_FOR_STEPUP,
            customer_id=session.customer_id if session else None,
            phone_number=session.phone_number if session else None,
            metadata={"stepup_action": action_details}
        )
        
        return WhatsAppResponse(
            recipient_id=whatsapp_user_id,
            message_text=confirmation_text
        )
    
    def _request_otp_if_needed(self, whatsapp_user_id: str, action_details: Dict[str, Any]) -> WhatsAppResponse:
        """Request OTP if needed based on action details"""
        session = session_manager.get_session(whatsapp_user_id)
        
        if not session or not session.phone_number:
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text="❌ Session error. Please send 'Hi' to restart."
            )
        
        # Check if OTP is required based on action risk
        reason = action_details.get("reason")
        requires_otp = False
        
        if reason == "session_too_old":
            requires_otp = True
        elif reason == "high_amount":
            requires_otp = True
        elif reason == "high_risk_action":
            # For very high-risk actions, always require OTP
            if action_details.get("type") in ["refund", "account_modification"]:
                requires_otp = True
        
        if requires_otp:
            # Generate and send OTP
            success, message, test_otp = otp_service.request_otp(
                whatsapp_user_id,
                session.phone_number,
                expiry_minutes=self.STEPUP_OTP_EXPIRY_MINUTES
            )
            
            if success:
                response_text = (
                    f"✅ Verification code sent to {session.phone_number}\n\n"
                    f"Please enter the 6-digit code to proceed."
                )
                if test_otp:
                    response_text += f"\n\n[DEV MODE] Your OTP: {test_otp}"
                
                # Update session metadata
                session_manager.update_session_state(
                    whatsapp_user_id,
                    AuthState.WAITING_FOR_STEPUP,
                    metadata={
                        "stepup_action": action_details,
                        "stepup_otp_sent": True
                    }
                )
                
                return WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=response_text
                )
            else:
                return WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=f"❌ {message}\n\nPlease try again or contact support."
                )
        else:
            # No OTP needed - just confirmation was enough
            # Mark session as VERIFIED and proceed
            from datetime import timedelta
            expires_at = datetime.now() + timedelta(hours=24)  # Refresh session expiry
            session_manager.update_session_state(
                whatsapp_user_id,
                AuthState.AUTHENTICATED,
                customer_id=session.customer_id,
                phone_number=session.phone_number,
                expires_at=expires_at,
                metadata={"auth_level": "VERIFIED", "stepup_completed": True}
            )
            
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text=(
                    "✅ Verification complete!\n\n"
                    "Proceeding with your request..."
                )
            )
    
    def _verify_stepup_otp(self, whatsapp_user_id: str, otp_code: str, action_details: Dict[str, Any]) -> WhatsAppResponse:
        """Verify step-up OTP"""
        session = session_manager.get_session(whatsapp_user_id)
        
        if not session or not session.phone_number:
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text="❌ Session error. Please send 'Hi' to restart."
            )
        
        # Verify OTP
        is_valid, message = otp_service.verify_otp(
            whatsapp_user_id,
            session.phone_number,
            otp_code
        )
        
        if is_valid:
            # Mark session as VERIFIED and proceed
            from datetime import timedelta
            expires_at = datetime.now() + timedelta(hours=24)  # Refresh session expiry
            session_manager.update_session_state(
                whatsapp_user_id,
                AuthState.AUTHENTICATED,
                customer_id=session.customer_id,
                phone_number=session.phone_number,
                expires_at=expires_at,
                metadata={"auth_level": "VERIFIED", "stepup_completed": True}
            )
            
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text=(
                    "✅ Verification successful!\n\n"
                    "Proceeding with your request..."
                )
            )
        else:
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text=(
                    f"❌ {message}\n\n"
                    "Please check the code and try again, or reply 'NO' to cancel."
                )
            )
    
    def _looks_like_otp(self, text: str) -> bool:
        """Check if text looks like an OTP (6 digits)"""
        import re
        text = text.strip()
        return bool(re.match(r'^\d{6}$', text))
    
    def is_stepup_complete(self, whatsapp_user_id: str) -> bool:
        """Check if step-up authentication is complete"""
        session = session_manager.get_session(whatsapp_user_id)
        if not session:
            return False
        
        # Check if session is VERIFIED
        metadata = session.metadata or {}
        return metadata.get("auth_level") == "VERIFIED" or metadata.get("stepup_completed", False)


# Global step-up auth handler instance
stepup_auth_handler = StepUpAuthHandler()
