"""
WhatsApp Integration Main Entry Point
Initializes database tables and provides setup functions
"""
import logging
import os
from whatsapp_integration.database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_whatsapp_integration():
    """
    Initialize WhatsApp integration - create database tables
    Call this once at application startup
    """
    try:
        logger.info("Initializing WhatsApp integration database tables...")
        db.initialize_tables()
        logger.info("✅ WhatsApp integration database tables initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error initializing WhatsApp integration: {e}")
        return False


def cleanup_expired_data():
    """
    Clean up expired OTPs and sessions
    Call this periodically (e.g., via cron job or background task)
    """
    try:
        logger.info("Cleaning up expired WhatsApp data...")
        deleted_otps = db.cleanup_expired_otps()
        deleted_sessions = db.cleanup_expired_sessions()
        logger.info(f"✅ Cleaned up: {deleted_otps} expired OTPs, {deleted_sessions} expired sessions")
        return deleted_otps, deleted_sessions
    except Exception as e:
        logger.error(f"❌ Error cleaning up WhatsApp data: {e}")
        return 0, 0


if __name__ == "__main__":
    # Initialize when run directly
    initialize_whatsapp_integration()
