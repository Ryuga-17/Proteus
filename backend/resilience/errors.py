from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StructuredError:
    error_type: str
    code: str
    message: str
    retryable: bool
    user_message: str
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.error_type,
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
            "user_message": self.user_message,
            "details": self.details or {},
        }


def error_response(error: StructuredError) -> Dict[str, Any]:
    return {
        "success": False,
        "error": error.to_dict(),
    }
