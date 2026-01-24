"""
OTP Service - Generate, store, and validate OTPs
"""
import os
import random
import string
import logging
from typing import Optional, Tuple
from datetime import datetime, timedelta

from whatsapp_integration.database import db
from whatsapp_integration.models import OTPRequest, OTPVerification

logger = logging.getLogger(__name__)


class OTPService:
    """Service for OTP generation and validation"""
    
    OTP_LENGTH = 6
    DEFAULT_EXPIRY_MINUTES = 10
    MAX_ATTEMPTS = 3
    
    @staticmethod
    def generate_otp(length: int = OTP_LENGTH) -> str:
        """Generate a random numeric OTP"""
        return ''.join(random.choices(string.digits, k=length))
    
    def generate_and_store_otp(self, whatsapp_user_id: str, phone_number: str, 
                               expiry_minutes: int = DEFAULT_EXPIRY_MINUTES) -> Tuple[str, datetime]:
        """
        Generate and store OTP in database
        
        Returns:
            Tuple of (otp_code, expires_at)
        """
        otp_code = self.generate_otp()
        expires_at = datetime.now() + timedelta(minutes=expiry_minutes)
        
        # Store in database
        db.store_otp(whatsapp_user_id, phone_number, otp_code, expiry_minutes)
        
        logger.info(f"Generated OTP for {whatsapp_user_id} / {phone_number}")
        return otp_code, expires_at
    
    def send_otp(self, whatsapp_user_id: str, phone_number: str, 
                 otp_code: str, expiry_minutes: int = DEFAULT_EXPIRY_MINUTES) -> bool:
        """
        Send OTP via WhatsApp
        
        Supports multiple providers:
        - Twilio (recommended for quick setup)
        - Meta WhatsApp Business API
        - Mock (for testing)
        
        Args:
            whatsapp_user_id: WhatsApp user ID
            phone_number: Phone number to send OTP to
            otp_code: OTP code to send
            expiry_minutes: OTP expiry time
        
        Returns:
            True if sent successfully
        """
        # Try Twilio first if configured
        if os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN"):
            return self._send_otp_twilio(phone_number, otp_code, expiry_minutes)
        
        # Try Meta WhatsApp Business API if configured
        if os.getenv("WHATSAPP_PHONE_NUMBER_ID") and os.getenv("WHATSAPP_ACCESS_TOKEN"):
            return self._send_otp_meta(phone_number, otp_code, expiry_minutes)
        
        # Fallback to mock for testing
        logger.info(f"[MOCK] Sending OTP to {phone_number}: {otp_code}")
        logger.info(f"[MOCK] OTP expires in {expiry_minutes} minutes")
        logger.warning("No WhatsApp API configured. Using mock mode. Set TWILIO_* or WHATSAPP_* env vars.")
        return True
    
    def _send_otp_twilio(self, phone_number: str, otp_code: str, expiry_minutes: int) -> bool:
        """Send OTP via Twilio WhatsApp API"""
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            whatsapp_from = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
            
            if not account_sid or not auth_token:
                logger.warning("Twilio credentials incomplete, falling back to mock")
                return False
            
            client = Client(account_sid, auth_token)
            
            # Normalize phone number for Twilio (must include whatsapp: prefix)
            to_number = phone_number if phone_number.startswith("whatsapp:") else f"whatsapp:{phone_number}"
            
            message_body = (
                f"Your verification code is: {otp_code}\n"
                f"This code expires in {expiry_minutes} minutes."
            )
            
            message = client.messages.create(
                body=message_body,
                from_=whatsapp_from,
                to=to_number
            )
            
            logger.info(f"OTP sent via Twilio to {phone_number}. Status: {message.status}, SID: {message.sid}")
            return message.status in ['queued', 'sent', 'accepted']
            
        except ImportError:
            logger.error("Twilio SDK not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            logger.error(f"Error sending OTP via Twilio: {e}")
            return False
    
    def _send_otp_meta(self, phone_number: str, otp_code: str, expiry_minutes: int) -> bool:
        """Send OTP via Meta WhatsApp Business API"""
        try:
            import requests
            
            phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
            access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
            api_version = os.getenv("WHATSAPP_API_VERSION", "v18.0")
            
            if not phone_number_id or not access_token:
                logger.warning("Meta WhatsApp credentials incomplete, falling back to mock")
                return False
            
            url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number.replace("whatsapp:", ""),  # Remove whatsapp: prefix if present
                "type": "text",
                "text": {
                    "body": (
                        f"Your verification code is: {otp_code}\n"
                        f"This code expires in {expiry_minutes} minutes."
                    )
                }
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"OTP sent via Meta WhatsApp to {phone_number}. Message ID: {result.get('messages', [{}])[0].get('id')}")
                return True
            else:
                logger.error(f"Meta WhatsApp API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending OTP via Meta WhatsApp: {e}")
            return False
    
    def verify_otp(self, whatsapp_user_id: str, phone_number: str, 
                   otp_code: str) -> Tuple[bool, str]:
        """
        Verify OTP code
        
        Returns:
            Tuple of (is_valid, message)
        """
        # Validate OTP format
        if not otp_code or len(otp_code) != self.OTP_LENGTH or not otp_code.isdigit():
            return False, "Invalid OTP format. Please enter a 6-digit code."
        
        # Verify against database
        is_valid = db.verify_otp(whatsapp_user_id, phone_number, otp_code)
        
        if is_valid:
            logger.info(f"OTP verified successfully for {whatsapp_user_id} / {phone_number}")
            return True, "OTP verified successfully!"
        else:
            # Get attempt count
            session = db.get_session(whatsapp_user_id)
            # Note: In a full implementation, you'd check attempts from the OTP table
            return False, "Invalid OTP. Please check and try again."
    
    def request_otp(self, whatsapp_user_id: str, phone_number: str, 
                    expiry_minutes: int = DEFAULT_EXPIRY_MINUTES) -> Tuple[bool, str, Optional[str]]:
        """
        Generate, store, and send OTP
        
        Returns:
            Tuple of (success, message, otp_code_for_testing)
        """
        try:
            # Normalize phone number (remove spaces, dashes, etc.)
            normalized_phone = self.normalize_phone_number(phone_number)
            
            if not self.is_valid_phone_number(normalized_phone):
                return False, "Invalid phone number format. Please enter a valid phone number with country code.", None
            
            # Generate and store OTP
            otp_code, expires_at = self.generate_and_store_otp(
                whatsapp_user_id, normalized_phone, expiry_minutes
            )
            
            # Send OTP (mock implementation)
            sent = self.send_otp(whatsapp_user_id, normalized_phone, otp_code, expiry_minutes)
            
            if sent:
                message = (
                    f"An OTP has been sent to {normalized_phone}. "
                    f"Please enter the 6-digit code to verify your account. "
                    f"The code expires in {expiry_minutes} minutes."
                )
                # In development/test mode, we can return the OTP for testing
                # In production, remove this!
                test_otp = os.getenv("ENVIRONMENT", "development").lower() == "development"
                return True, message, otp_code if test_otp else None
            else:
                return False, "Failed to send OTP. Please try again later.", None
                
        except Exception as e:
            logger.error(f"Error requesting OTP: {e}")
            return False, f"An error occurred: {str(e)}", None
    
    @staticmethod
    def normalize_phone_number(phone: str) -> str:
        """Normalize phone number (remove spaces, dashes, parentheses)"""
        # Remove all non-digit characters except +
        normalized = ''.join(c for c in phone if c.isdigit() or c == '+')
        
        # If no country code, assume default (you may want to make this configurable)
        if not normalized.startswith('+'):
            # Default to +1 (US) - adjust as needed
            normalized = '+1' + normalized
        
        return normalized
    
    @staticmethod
    def is_valid_phone_number(phone: str) -> bool:
        """Basic phone number validation"""
        # Remove + and check if all digits
        digits_only = phone.replace('+', '')
        
        # Should have at least 10 digits (country code + number)
        # Adjust validation based on your requirements
        return len(digits_only) >= 10 and len(digits_only) <= 15 and digits_only.isdigit()


# Global OTP service instance
otp_service = OTPService()
