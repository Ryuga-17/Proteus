"""
Authentication Handler - Handles OTP-based authentication flow
"""
import logging
import re
from typing import Optional, Tuple
from datetime import datetime

from whatsapp_integration.models import WhatsAppMessage, WhatsAppResponse, AuthState
from whatsapp_integration.session_manager import session_manager
from whatsapp_integration.otp_service import otp_service
from whatsapp_integration.database import db

logger = logging.getLogger(__name__)


class AuthHandler:
    """Handles authentication flow for WhatsApp users"""
    
    # Common greeting patterns
    GREETING_PATTERNS = [
        r'\b(hi|hello|hey|start|begin)\b',
        r'\b(help|support)\b'
    ]
    
    def is_greeting(self, message_text: str) -> bool:
        """Check if message is a greeting that should start auth flow"""
        message_lower = message_text.lower().strip()
        
        # Check against patterns
        for pattern in self.GREETING_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return True
        
        # Very short messages might be greetings
        if len(message_lower) <= 5 and message_lower in ['hi', 'hey', 'hello', 'start']:
            return True
        
        return False
    
    def looks_like_phone_number(self, text: str) -> bool:
        """Check if text looks like a phone number"""
        # Remove common separators
        normalized = re.sub(r'[\s\-\(\)\.]', '', text)
        
        # Check if it's mostly digits or has country code
        if re.match(r'^\+?\d{10,15}$', normalized):
            return True
        
        return False
    
    def looks_like_otp(self, text: str) -> bool:
        """Check if text looks like an OTP (6 digits)"""
        # Remove whitespace
        text = text.strip()
        return bool(re.match(r'^\d{6}$', text))
    
    def handle_message(self, message: WhatsAppMessage) -> Tuple[WhatsAppResponse, bool]:
        """
        Handle incoming message in authentication flow
        
        Returns:
            Tuple of (response, continue_auth_flow)
            - continue_auth_flow: True if still in auth flow, False if authenticated
        """
        whatsapp_user_id = message.sender_id
        message_text = message.message_text.strip()
        
        # Get current session
        session = session_manager.get_session(whatsapp_user_id)
        
        # Check if user has a valid session first (returning user)
        if session and session_manager.is_valid_session(whatsapp_user_id):
            # User has valid session - should not reach here from auth handler
            # This is handled by message handler
            response = WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text="You are already authenticated. Your request is being processed.")
            return response, False
        
        # No session or expired - check if this is a greeting to start auth
        if not session or session.auth_state == AuthState.EXPIRED:
            if self.is_greeting(message_text):
                # Start authentication flow
                session = session_manager.start_auth_flow(whatsapp_user_id)
                response = WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=(
                        "👋 Hi! Welcome to our shopping assistant!\n\n"
                        "To get started, I need to link your WhatsApp to your account.\n"
                        "Please enter your registered mobile number (with country code, e.g., +1234567890):"
                    )
                )
                return response, True
            else:
                # Not authenticated and not a greeting - ask to start
                response = WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=(
                        "👋 Hello! To use our shopping assistant, please start by sending 'Hi' or 'Hello'.\n"
                        "We'll help you link your WhatsApp account."
                    )
                )
                return response, True
        
        # Handle based on auth state
        auth_state = session.auth_state
        
        if auth_state == AuthState.UNAUTHENTICATED:
            if self.is_greeting(message_text):
                # Restart auth flow
                session = session_manager.start_auth_flow(whatsapp_user_id)
                response = WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=(
                        "👋 Hi! To get started, I need to link your WhatsApp to your account.\n"
                        "Please enter your registered mobile number (with country code, e.g., +1234567890):"
                    )
                )
                return response, True
            else:
                # Not authenticated - ask to start
                response = WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=(
                        "Please send 'Hi' to start and link your WhatsApp account."
                    )
                )
                return response, True
        
        elif auth_state == AuthState.WAITING_FOR_PHONE:
            if self.looks_like_phone_number(message_text):
                # Process phone number
                phone_number = otp_service.normalize_phone_number(message_text)
                
                # Check if customer exists
                customer_id = db.get_customer_by_phone(phone_number)
                
                if not customer_id:
                    # Customer not found
                    response = WhatsAppResponse(
                        recipient_id=whatsapp_user_id,
                        message_text=(
                            "❌ We couldn't find an account with that phone number.\n\n"
                            "Please make sure you're using the same number you registered with.\n"
                            "Or send 'cancel' to start over."
                        )
                    )
                    return response, True
                
                # Request OTP
                session = session_manager.request_otp(whatsapp_user_id, phone_number)
                success, message, test_otp = otp_service.request_otp(
                    whatsapp_user_id, phone_number
                )
                
                if success:
                    response_text = f"✅ {message}"
                    # In development, include OTP for testing
                    if test_otp:
                        response_text += f"\n\n[DEV MODE] Your OTP: {test_otp}"
                    
                    response = WhatsAppResponse(
                        recipient_id=whatsapp_user_id,
                        message_text=response_text
                    )
                    return response, True
                else:
                    response = WhatsAppResponse(
                        recipient_id=whatsapp_user_id,
                        message_text=f"❌ {message}\n\nSend 'retry' to try again or 'cancel' to start over."
                    )
                    return response, True
            elif message_text.lower() in ['cancel', 'reset', 'start over']:
                # Cancel auth flow
                session = session_manager.reset_auth_flow(whatsapp_user_id)
                response = WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text="Authentication cancelled. Send 'Hi' to start again.")
                return response, True
            else:
                # Invalid input
                response = WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=(
                        "Please enter a valid phone number with country code (e.g., +1234567890).\n"
                        "Or send 'cancel' to start over."
                    )
                )
                return response, True
        
        elif auth_state == AuthState.WAITING_FOR_OTP:
            if self.looks_like_otp(message_text):
                # Verify OTP
                phone_number = session.phone_number
                if not phone_number:
                    # Shouldn't happen, but handle it
                    response = WhatsAppResponse(
                        recipient_id=whatsapp_user_id,
                        message_text="An error occurred. Please send 'Hi' to start again.")
                    return response, True
                
                is_valid, message = otp_service.verify_otp(
                    whatsapp_user_id, phone_number, message_text
                )
                
                if is_valid:
                    # Get customer ID
                    customer_id = db.get_customer_by_phone(phone_number)
                    
                    if customer_id:
                        # Complete authentication
                        session = session_manager.complete_auth_flow(
                            whatsapp_user_id, customer_id, phone_number
                        )
                        response = WhatsAppResponse(
                            recipient_id=whatsapp_user_id,
                            message_text=(
                                "✅ Account linked successfully!\n\n"
                                "You can now use our shopping assistant. How can I help you today?\n"
                                "Try asking:\n"
                                "• 'Show me products'\n"
                                "• 'Check my order status'\n"
                                "• 'What are my loyalty points?'\n"
                                "• Or any other shopping question!"
                            )
                        )
                        return response, False  # Auth complete, continue to agent
                    else:
                        # Shouldn't happen, but handle it
                        response = WhatsAppResponse(
                            recipient_id=whatsapp_user_id,
                            message_text="An error occurred. Please send 'Hi' to start again.")
                        return response, True
                else:
                    # Invalid OTP
                    response = WhatsAppResponse(
                        recipient_id=whatsapp_user_id,
                        message_text=(
                            f"❌ {message}\n\n"
                            "Please check the code and try again, or send 'cancel' to start over."
                        )
                    )
                    return response, True
            elif message_text.lower() in ['cancel', 'reset', 'start over', 'resend']:
                if message_text.lower() == 'resend':
                    # Resend OTP
                    phone_number = session.phone_number
                    if phone_number:
                        success, message, test_otp = otp_service.request_otp(
                            whatsapp_user_id, phone_number
                        )
                        response_text = f"✅ {message}" if success else f"❌ {message}"
                        if success and test_otp:
                            response_text += f"\n\n[DEV MODE] Your OTP: {test_otp}"
                        response = WhatsAppResponse(
                            recipient_id=whatsapp_user_id,
                            message_text=response_text
                        )
                        return response, True
                else:
                    # Cancel auth flow
                    session = session_manager.reset_auth_flow(whatsapp_user_id)
                    response = WhatsAppResponse(
                        recipient_id=whatsapp_user_id,
                        message_text="Authentication cancelled. Send 'Hi' to start again.")
                    return response, True
            else:
                # Invalid input
                response = WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=(
                        "Please enter the 6-digit OTP code you received.\n"
                        "Or send 'resend' to get a new code, or 'cancel' to start over."
                    )
                )
                return response, True
        
        elif auth_state == AuthState.AUTHENTICATED:
            # Already authenticated - should not reach here from auth handler
            # This will be handled by message handler
            response = WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text="You are already authenticated. Your request is being processed.")
            return response, False
        
        else:
            # Unknown state
            response = WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text="An error occurred. Please send 'Hi' to start again.")
            return response, True


# Global auth handler instance
auth_handler = AuthHandler()
