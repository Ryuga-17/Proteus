"""
WhatsApp Message Sender - Send messages via Twilio WhatsApp API
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class WhatsAppSender:
    """Send WhatsApp messages via Twilio API"""
    
    def __init__(self):
        """Initialize Twilio client if credentials are available"""
        self.twilio_client = None
        self.whatsapp_from = None
        self._init_twilio()
    
    def _init_twilio(self):
        """Initialize Twilio client"""
        try:
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            whatsapp_from = os.getenv("TWILIO_WHATSAPP_FROM") or os.getenv("TWILIO_WHATSAPP_NUMBER") or "whatsapp:+14155238886"
            
            # Ensure whatsapp_from has proper format
            if whatsapp_from and not whatsapp_from.startswith("whatsapp:"):
                whatsapp_from = f"whatsapp:{whatsapp_from}"
            
            # Validate that whatsapp_from is not empty or just "whatsapp:"
            if not whatsapp_from or whatsapp_from == "whatsapp:" or whatsapp_from == "whatsapp:+":
                whatsapp_from = "whatsapp:+14155238886"  # Default sandbox number
                logger.warning(f"TWILIO_WHATSAPP_FROM not set or invalid, using default: {whatsapp_from}")
            
            if account_sid and auth_token:
                from twilio.rest import Client
                self.twilio_client = Client(account_sid, auth_token)
                self.whatsapp_from = whatsapp_from
                logger.info(f"Twilio WhatsApp sender initialized with From: {whatsapp_from}")
            else:
                logger.warning("Twilio credentials not found - WhatsApp messages will not be sent")
        except ImportError:
            logger.warning("Twilio SDK not installed - install with: pip install twilio")
        except Exception as e:
            logger.error(f"Error initializing Twilio: {e}")
    
    def send_message(self, to_number: str, message_text: str) -> bool:
        """
        Send WhatsApp message via Twilio
        
        Args:
            to_number: Recipient phone number (with country code, e.g., +918850833367)
            message_text: Message content to send
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.twilio_client:
            logger.warning("Twilio client not available - cannot send WhatsApp message")
            return False
        
        try:
            # Normalize phone number for Twilio (must include whatsapp: prefix)
            to_number_formatted = to_number if to_number.startswith("whatsapp:") else f"whatsapp:{to_number}"
            
            # Remove whatsapp: prefix from sender_id if present for phone lookup
            clean_to = to_number.replace("whatsapp:", "").replace("+", "")
            
            message = self.twilio_client.messages.create(
                body=message_text,
                from_=self.whatsapp_from,
                to=to_number_formatted
            )
            
            logger.info(f"WhatsApp message sent to {to_number}. Status: {message.status}, SID: {message.sid}")
            return message.status in ['queued', 'sent', 'accepted', 'delivered']
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message via Twilio: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Twilio sender is available"""
        return self.twilio_client is not None


# Global WhatsApp sender instance
whatsapp_sender = WhatsAppSender()
