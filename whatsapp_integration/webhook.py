"""
WhatsApp Webhook Interface - FastAPI endpoints for WhatsApp Business API
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from whatsapp_integration.models import WhatsAppMessage, WhatsAppResponse
from whatsapp_integration.message_handler import message_handler
from whatsapp_integration.whatsapp_sender import whatsapp_sender

logger = logging.getLogger(__name__)

# Initialize FastAPI app (can be mounted to main app or run standalone)
app = FastAPI(
    title="WhatsApp Integration API",
    description="Webhook endpoints for WhatsApp Business API integration",
    version="1.0.0"
)


# ============================================================================
# Request/Response Models
# ============================================================================

class WhatsAppWebhookPayload(BaseModel):
    """WhatsApp webhook payload model"""
    # This model can be extended based on actual WhatsApp Business API format
    object: Optional[str] = None
    entry: Optional[list] = None
    
    # Simplified format for simulation
    sender_id: Optional[str] = Field(None, alias="From")
    message_text: Optional[str] = Field(None, alias="Body")
    message_id: Optional[str] = Field(None, alias="MessageId")
    timestamp: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class WebhookVerification(BaseModel):
    """Webhook verification request"""
    hub_mode: str
    hub_verify_token: str
    hub_challenge: str


class WhatsAppWebhookResponse(BaseModel):
    """Response from WhatsApp webhook processing"""
    success: bool
    message: str
    response_text: Optional[str] = None


class SimulateMessageRequest(BaseModel):
    """Request model for simulate message endpoint"""
    sender_id: str = Field(..., description="WhatsApp sender ID (phone number)")
    message_text: str = Field(..., description="Message content")


# ============================================================================
# Webhook Verification (WhatsApp Business API requirement)
# ============================================================================

WEBHOOK_VERIFY_TOKEN = "your_secure_verify_token_here"  # Set via env var in production


@app.get("/webhook")
async def verify_webhook(
    hub_mode: str,
    hub_verify_token: str,
    hub_challenge: str
):
    """
    Webhook verification endpoint (GET)
    WhatsApp Business API will call this to verify the webhook
    """
    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return int(hub_challenge)  # Return challenge as integer
    else:
        logger.warning(f"Webhook verification failed: mode={hub_mode}, token={hub_verify_token}")
        raise HTTPException(status_code=403, detail="Verification failed")


# ============================================================================
# Message Webhook (WhatsApp Business API)
# ============================================================================

@app.post("/webhook", response_model=WhatsAppWebhookResponse)
async def receive_whatsapp_message(request: Request):
    """
    Receive incoming WhatsApp messages (POST)
    This endpoint receives webhooks from WhatsApp Business API
    """
    try:
        # Twilio sends form-encoded data, not JSON
        # Try to get as form data first, then JSON
        content_type = request.headers.get("content-type", "")
        
        if "application/x-www-form-urlencoded" in content_type:
            # Twilio sends form-encoded data
            form_data = await request.form()
            body = dict(form_data)
            logger.info(f"Received Twilio webhook (form): {body}")
        else:
            # Try JSON (for testing/simulation)
            try:
                body = await request.json()
                logger.info(f"Received webhook (JSON): {body}")
            except Exception:
                # If JSON parsing fails, try reading raw body
                raw_body = await request.body()
                logger.warning(f"Could not parse webhook body. Content-Type: {content_type}, Body: {raw_body}")
                # Try to parse as form data
                try:
                    from urllib.parse import parse_qs
                    parsed = parse_qs(raw_body.decode())
                    body = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
                    logger.info(f"Parsed as form data: {body}")
                except Exception as e:
                    logger.error(f"Could not parse webhook body: {e}")
                    return WhatsAppWebhookResponse(
                        success=False,
                        message=f"Could not parse webhook: {str(e)}"
                    )
        
        # Check if this is a webhook verification (GET request would be handled separately)
        # Or a status callback (no Body field)
        if "Body" not in body or not body.get("Body"):
            # This might be a status callback or other webhook type
            logger.info(f"Received non-message webhook: {list(body.keys())}")
            # Return success but don't process as message
            return WhatsAppWebhookResponse(
                success=True,
                message="Webhook received (not a message)",
                response_text=""
            )
        
        # Parse WhatsApp message from webhook payload
        # Twilio sends form-encoded data with: From, Body, To, MessageSid
        message = _parse_twilio_webhook(body)
        
        if not message:
            # Try fallback parser
            message = _parse_webhook_payload(body)
        
        if not message:
            logger.warning(f"Could not parse message from webhook. Keys: {list(body.keys())}, Body: {body}")
            return WhatsAppWebhookResponse(
                success=False,
                message="Could not parse message"
            )
        
        # Handle message through message handler
        response = message_handler.handle_message(message)
        
        # Send response back via WhatsApp API
        message_sent = False
        if whatsapp_sender.is_available():
            # Extract phone number from sender_id (remove whatsapp: prefix if present)
            phone_number = message.sender_id.replace("whatsapp:", "")
            message_sent = whatsapp_sender.send_message(phone_number, response.message_text)
            
            if message_sent:
                logger.info(f"Response sent via WhatsApp to {phone_number}")
            else:
                logger.warning(f"Failed to send WhatsApp message to {phone_number}")
        else:
            logger.warning("WhatsApp sender not available - response not sent via WhatsApp")
        
        logger.info(f"Processed message from {message.sender_id}: {response.message_text[:100]}")
        
        # Return 200 OK immediately (message sent async via Twilio)
        return WhatsAppWebhookResponse(
            success=True,
            message="Message processed successfully" + (" and sent via WhatsApp" if message_sent else " (WhatsApp sender not configured)"),
            response_text=response.message_text
        )
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


def _parse_twilio_webhook(payload: Dict[str, Any]) -> Optional[WhatsAppMessage]:
    """
    Parse Twilio WhatsApp webhook payload
    
    Twilio sends form-encoded data with:
    - From: whatsapp:+918850833367 (sender)
    - Body: Message text
    - To: whatsapp:+14155238886 (Twilio's number)
    - MessageSid: Unique message ID
    """
    try:
        # Twilio format
        if "From" in payload and "Body" in payload:
            sender_id = payload.get("From", "")
            message_text = payload.get("Body", "")
            message_id = payload.get("MessageSid")
            
            # Remove "whatsapp:" prefix if present
            if sender_id.startswith("whatsapp:"):
                sender_id = sender_id.replace("whatsapp:", "")
            
            if sender_id and message_text:
                logger.info(f"Parsed Twilio message: From={sender_id}, Body={message_text[:50]}")
                return WhatsAppMessage(
                    sender_id=f"whatsapp:{sender_id}",  # Keep whatsapp: prefix for internal use
                    message_text=message_text,
                    message_id=message_id,
                    timestamp=datetime.now()
                )
        
        logger.warning(f"Could not parse Twilio webhook. Keys: {list(payload.keys())}")
        return None
    except Exception as e:
        logger.error(f"Error parsing Twilio webhook: {e}")
        return None


def _parse_webhook_payload(payload: Dict[str, Any]) -> Optional[WhatsAppMessage]:
    """
    Parse WhatsApp Business API webhook payload into WhatsAppMessage
    
    This is a simplified parser - actual format depends on WhatsApp Business API version
    Adjust this based on your actual webhook format
    """
    try:
        # Try simplified format first (for testing/simulation)
        if "sender_id" in payload or "From" in payload:
            sender_id = payload.get("sender_id") or payload.get("From", "")
            message_text = payload.get("message_text") or payload.get("Body", "")
            message_id = payload.get("message_id") or payload.get("MessageId")
            
            if sender_id and message_text:
                return WhatsAppMessage(
                    sender_id=sender_id,
                    message_text=message_text,
                    message_id=message_id,
                    timestamp=datetime.now()
                )
        
        # Try standard WhatsApp Business API format
        if "entry" in payload and isinstance(payload["entry"], list):
            for entry in payload["entry"]:
                if "changes" in entry and isinstance(entry["changes"], list):
                    for change in entry["changes"]:
                        if "value" in change:
                            value = change["value"]
                            
                            # Check for messages
                            if "messages" in value and isinstance(value["messages"], list):
                                for msg in value["messages"]:
                                    if "from" in msg and "text" in msg:
                                        return WhatsAppMessage(
                                            sender_id=msg["from"],
                                            message_text=msg["text"]["body"],
                                            message_id=msg.get("id"),
                                            timestamp=datetime.now()
                                        )
        
        return None
    
    except Exception as e:
        logger.error(f"Error parsing webhook payload: {e}")
        return None


# ============================================================================
# Test/Simulation Endpoint
# ============================================================================

@app.post("/simulate/message", response_model=WhatsAppWebhookResponse)
async def simulate_whatsapp_message(request: SimulateMessageRequest):
    """
    Simulate incoming WhatsApp message (for testing)
    This endpoint allows testing without actual WhatsApp Business API
    
    Example request body:
    {
        "sender_id": "whatsapp:+1234567890",
        "message_text": "Hi"
    }
    """
    try:
        message = WhatsAppMessage(
            sender_id=request.sender_id,
            message_text=request.message_text,
            timestamp=datetime.now()
        )
        
        # Handle message
        response = message_handler.handle_message(message)
        
        # Optionally send via WhatsApp if Twilio is configured
        # (For simulation, we just return the response)
        message_sent = False
        if whatsapp_sender.is_available():
            # Extract phone number from sender_id
            phone_number = request.sender_id.replace("whatsapp:", "")
            message_sent = whatsapp_sender.send_message(phone_number, response.message_text)
            if message_sent:
                logger.info(f"Simulated message response sent via WhatsApp to {phone_number}")
        
        return WhatsAppWebhookResponse(
            success=True,
            message="Message processed successfully" + (" and sent via WhatsApp" if message_sent else ""),
            response_text=response.message_text
        )
    
    except Exception as e:
        logger.error(f"Error simulating message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "whatsapp_integration"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
