"""
Data models for WhatsApp integration
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AuthState(str, Enum):
    """Authentication state enumeration"""
    UNAUTHENTICATED = "unauthenticated"
    WAITING_FOR_PHONE = "waiting_for_phone"
    WAITING_FOR_OTP = "waiting_for_otp"
    AUTHENTICATED = "authenticated"
    EXPIRED = "expired"
    WAITING_FOR_STEPUP = "waiting_for_stepup"  # Waiting for step-up authentication confirmation


class AuthLevel(str, Enum):
    """Authentication level enumeration"""
    BASIC = "BASIC"  # Basic authenticated session (for low-risk actions)
    VERIFIED = "VERIFIED"  # Verified session (for high-risk actions, requires step-up auth)


class WhatsAppMessage(BaseModel):
    """Incoming WhatsApp message model"""
    sender_id: str = Field(..., description="WhatsApp user ID (phone number with country code)")
    message_text: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Message timestamp")
    message_id: Optional[str] = Field(None, description="WhatsApp message ID")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class WhatsAppResponse(BaseModel):
    """Outgoing WhatsApp message response"""
    recipient_id: str = Field(..., description="WhatsApp user ID to send message to")
    message_text: str = Field(..., description="Response message content")
    message_type: str = Field(default="text", description="Message type (text, image, etc.)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class OTPRequest(BaseModel):
    """OTP generation request"""
    phone_number: str = Field(..., description="Phone number to send OTP to")
    whatsapp_user_id: str = Field(..., description="WhatsApp user ID requesting OTP")
    expiry_minutes: int = Field(default=10, description="OTP expiry time in minutes")


class OTPVerification(BaseModel):
    """OTP verification request"""
    whatsapp_user_id: str = Field(..., description="WhatsApp user ID")
    otp_code: str = Field(..., description="6-digit OTP code")
    phone_number: str = Field(..., description="Phone number associated with OTP")


class SessionInfo(BaseModel):
    """Session information model"""
    whatsapp_user_id: str
    customer_id: Optional[str] = None
    auth_state: AuthState
    auth_level: Optional[str] = "BASIC"  # BASIC or VERIFIED
    phone_number: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    expires_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AuthFlowContext(BaseModel):
    """Authentication flow context"""
    whatsapp_user_id: str
    phone_number: Optional[str] = None
    otp_code: Optional[str] = None
    otp_expiry: Optional[datetime] = None
    attempts: int = Field(default=0, description="Number of OTP verification attempts")
    max_attempts: int = Field(default=3, description="Maximum allowed attempts")
    state: AuthState = AuthState.UNAUTHENTICATED
    created_at: datetime = Field(default_factory=datetime.now)
