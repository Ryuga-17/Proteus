"""
Action Risk Detector - Detects high-risk actions that require step-up authentication
"""
import logging
import re
from typing import Tuple, Optional, Dict, Any

logger = logging.getLogger(__name__)


class ActionRiskDetector:
    """Detects high-risk actions in user messages"""
    
    # High-risk action patterns
    HIGH_RISK_PATTERNS = {
        "payment": [
            r'\b(pay|payment|purchase|buy|checkout|transaction|charge|billing)\b',
            r'\b(credit\s*card|debit\s*card|card\s*number|payment\s*method)\b',
            r'\b(₹|rs\.?|rupees?|dollars?|\$)\s*\d+',  # Payment amounts
        ],
        "refund": [
            r'\b(refund|return|money\s*back|cancel\s*order|reverse)\b',
            r'\b(return\s*item|refund\s*request|cancel\s*purchase)\b',
        ],
        "address_change": [
            r'\b(change\s*address|update\s*address|new\s*address|modify\s*address)\b',
            r'\b(change\s*shipping|update\s*shipping|delivery\s*address)\b',
        ],
        "account_modification": [
            r'\b(change\s*password|update\s*password|reset\s*password)\b',
            r'\b(change\s*email|update\s*email|modify\s*account)\b',
            r'\b(delete\s*account|close\s*account|deactivate)\b',
        ],
    }
    
    # Low-risk action patterns (no step-up required)
    LOW_RISK_PATTERNS = [
        r'\b(browse|show|list|search|find|look|view|see)\b',
        r'\b(recommend|suggest|what|which|help|info|information)\b',
        r'\b(inventory|stock|available|availability|check\s*stock)\b',
        r'\b(reserve|hold|book)\b',  # Reserving items is low-risk
        r'\b(order\s*status|track|where\s*is|delivery\s*status)\b',
        r'\b(loyalty\s*points|points|rewards|offers|promotions)\b',
    ]
    
    # Risk thresholds
    PAYMENT_RISK_THRESHOLD = 10000  # ₹10,000 - above this requires step-up
    SESSION_AGE_FOR_STEPUP_HOURS = 24  # Sessions older than 24 hours need step-up for high-risk
    
    def detect_action_risk(self, message_text: str, session_info: Optional[Dict[str, Any]] = None) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Detect if message contains high-risk actions
        
        Args:
            message_text: User's message
            session_info: Optional session information (for checking session age)
        
        Returns:
            Tuple of (risk_level, action_details)
            - risk_level: "HIGH", "LOW", or "NONE"
            - action_details: Dict with action type, amount (if payment), etc.
        """
        message_lower = message_text.lower()
        
        # Check for high-risk actions
        for action_type, patterns in self.HIGH_RISK_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    # Extract payment amount if it's a payment action
                    amount = None
                    if action_type == "payment":
                        amount = self._extract_payment_amount(message_text)
                    
                    action_details = {
                        "type": action_type,
                        "amount": amount,
                        "requires_stepup": True,
                    }
                    
                    # Check if session age requires step-up
                    if session_info:
                        session_age_hours = self._get_session_age_hours(session_info)
                        if session_age_hours > self.SESSION_AGE_FOR_STEPUP_HOURS:
                            action_details["reason"] = "session_too_old"
                        elif amount and amount > self.PAYMENT_RISK_THRESHOLD:
                            action_details["reason"] = "high_amount"
                        else:
                            action_details["reason"] = "high_risk_action"
                    
                    logger.info(f"Detected high-risk action: {action_type}, amount: {amount}")
                    return "HIGH", action_details
        
        # Check for low-risk actions
        for pattern in self.LOW_RISK_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return "LOW", {"type": "low_risk", "requires_stepup": False}
        
        # Default to low-risk for unknown actions
        return "LOW", {"type": "unknown", "requires_stepup": False}
    
    def _extract_payment_amount(self, message_text: str) -> Optional[float]:
        """Extract payment amount from message"""
        # Look for currency symbols followed by numbers
        patterns = [
            r'[₹$]?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',  # ₹1000 or $1000 or 1000
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:rupees?|rs\.?|dollars?)',  # 1000 rupees
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message_text, re.IGNORECASE)
            if matches:
                try:
                    # Get the largest amount (likely the payment amount)
                    amounts = []
                    for match in matches:
                        # Remove commas
                        clean_amount = match.replace(',', '')
                        amounts.append(float(clean_amount))
                    return max(amounts) if amounts else None
                except ValueError:
                    continue
        
        return None
    
    def _get_session_age_hours(self, session_info: Dict[str, Any]) -> float:
        """Get session age in hours"""
        from datetime import datetime
        
        if "last_activity" in session_info and session_info["last_activity"]:
            if isinstance(session_info["last_activity"], str):
                last_activity = datetime.fromisoformat(session_info["last_activity"])
            else:
                last_activity = session_info["last_activity"]
            
            age = datetime.now() - last_activity
            return age.total_seconds() / 3600
        
        return 0.0
    
    def requires_stepup(self, message_text: str, session_info: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Check if action requires step-up authentication
        
        Returns:
            Tuple of (requires_stepup, action_details)
        """
        risk_level, action_details = self.detect_action_risk(message_text, session_info)
        
        if risk_level == "HIGH" and action_details.get("requires_stepup"):
            return True, action_details
        
        return False, None


# Global action risk detector instance
action_risk_detector = ActionRiskDetector()
