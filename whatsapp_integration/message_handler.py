"""
Message Handler - Routes messages to appropriate handlers (auth or orchestrator)
"""
import logging
import os
import sys
from typing import Tuple

from whatsapp_integration.models import WhatsAppMessage, WhatsAppResponse, AuthState
from whatsapp_integration.auth_handler import auth_handler
from whatsapp_integration.session_manager import session_manager

logger = logging.getLogger(__name__)


class MessageHandler:
    """Handles incoming messages and routes to appropriate handlers"""
    
    def __init__(self):
        """Initialize message handler with orchestrator integration"""
        self.orchestrator_client = None
        self._init_orchestrator()
    
    def _init_orchestrator(self):
        """Initialize connection to orchestrator"""
        try:
            # Try to import orchestrator client
            orchestrator_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "Orchestrator"
            )
            if orchestrator_path not in sys.path:
                sys.path.insert(0, orchestrator_path)
            
            # Try MCP client first
            try:
                from mcp_client import SimpleOrchestratorClient
                self.orchestrator_client = SimpleOrchestratorClient()
                logger.info("Initialized MCP orchestrator client")
                return
            except ImportError:
                pass
            
            # Fallback to direct orchestrator import
            try:
                # This will be used to call handle_custom_request
                self.orchestrator_client = "direct"
                logger.info("Using direct orchestrator import")
                return
            except ImportError:
                pass
            
            logger.warning("Could not initialize orchestrator client")
        except Exception as e:
            logger.error(f"Error initializing orchestrator: {e}")
    
    def handle_message(self, message: WhatsAppMessage) -> WhatsAppResponse:
        """
        Main message handler - routes messages to auth or orchestrator
        
        Args:
            message: Incoming WhatsApp message
        
        Returns:
            WhatsApp response to send back
        """
        whatsapp_user_id = message.sender_id
        message_text = message.message_text.strip().lower()
        
        # Handle logout command
        if message_text in ["logout", "sign out", "log out"]:
            session = session_manager.get_session(whatsapp_user_id)
            if session and session.auth_state == AuthState.AUTHENTICATED:
                session_manager.invalidate_session(whatsapp_user_id)
                return WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text="✅ You have been logged out. Send 'Hi' to log in again."
                )
            else:
                return WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text="You are not currently logged in."
                )
        
        # Check if user has a valid session
        is_valid_session = session_manager.is_valid_session(whatsapp_user_id)
        session = session_manager.get_session(whatsapp_user_id)
        
        # If valid session exists and user sends greeting, welcome them back
        if is_valid_session and auth_handler.is_greeting(message.message_text):
            welcome_message = session_manager.get_welcome_back_message(whatsapp_user_id)
            if welcome_message:
                # Update last activity
                session_manager.update_last_activity(whatsapp_user_id)
                return WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=welcome_message
                )
        
        # If not authenticated or in auth flow, handle via auth handler
        if not session or session.auth_state != AuthState.AUTHENTICATED:
            # Handle authentication flow
            response, auth_complete = auth_handler.handle_message(message)
            
            # If auth just completed, this response is already sent
            # Next message will go to orchestrator
            return response
        
        # User is authenticated - check for step-up authentication
        if session.auth_state == AuthState.WAITING_FOR_STEPUP:
            # Handle step-up authentication flow
            action_details = session.metadata.get("stepup_action") if session.metadata else None
            if action_details:
                return stepup_auth_handler.handle_stepup_flow(message, action_details)
        
        # Check if this action requires step-up authentication
        # Only check if session is authenticated (not in step-up flow)
        if session.auth_state == AuthState.AUTHENTICATED:
            requires_stepup, action_details = stepup_auth_handler.check_stepup_required(
                message,
                {
                    "auth_state": session.auth_state,
                    "last_activity": session.last_activity,
                    "metadata": session.metadata or {}
                }
            )
            
            if requires_stepup and action_details:
                # Start step-up flow
                return stepup_auth_handler.handle_stepup_flow(message, action_details)
        
        # Update last activity
        session_manager.update_last_activity(whatsapp_user_id)
        
        # User is authenticated - route to orchestrator
        try:
            customer_id = session_manager.get_customer_id(whatsapp_user_id)
            
            if not customer_id:
                # Shouldn't happen, but handle it
                return WhatsAppResponse(
                    recipient_id=whatsapp_user_id,
                    message_text=(
                        "❌ Session error. Please send 'Hi' to re-authenticate."
                    )
                )
            
            # Route to orchestrator
            orchestrator_response = self._route_to_orchestrator(
                message.message_text,
                customer_id
            )
            
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text=orchestrator_response
            )
        
        except Exception as e:
            logger.error(f"Error handling authenticated message: {e}", exc_info=True)
            return WhatsAppResponse(
                recipient_id=whatsapp_user_id,
                message_text=(
                    "❌ Sorry, I encountered an error processing your request.\n"
                    "Please try again or send 'Hi' to restart."
                )
            )
    
    def _route_to_orchestrator(self, message_text: str, customer_id: str) -> str:
        """
        Route message to orchestrator for processing
        
        Args:
            message_text: User's message
            customer_id: Authenticated customer ID
        
        Returns:
            Response text from orchestrator
        """
        try:
            if self.orchestrator_client and self.orchestrator_client != "direct":
                # Use MCP client
                result = self.orchestrator_client.handle_request(
                    message_text,
                    user_id=customer_id
                )
                response_text = result.get("agent_response", "No response received")
                return response_text
            
            # Fallback to direct orchestrator call
            orchestrator_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "Orchestrator"
            )
            if orchestrator_path not in sys.path:
                sys.path.insert(0, orchestrator_path)
            
            from main import handle_custom_request
            
            # Call orchestrator
            result = handle_custom_request(message_text)
            
            # Extract text from result (may be a string or an object)
            if isinstance(result, str):
                return result
            elif hasattr(result, 'raw'):
                return str(result.raw)
            else:
                return str(result)
        
        except ImportError as e:
            logger.error(f"Could not import orchestrator: {e}")
            return (
                "Sorry, the agent system is temporarily unavailable.\n"
                "Please try again later."
            )
        except Exception as e:
            logger.error(f"Error routing to orchestrator: {e}")
            return (
                "Sorry, I encountered an error processing your request.\n"
                "Please try rephrasing or try again later."
            )


# Global message handler instance
message_handler = MessageHandler()
