"""
Redis-backed session and OTP store for WhatsApp integration.
Use when REDIS_URL is set; provides fast, fault-tolerant session persistence.
"""
import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

SESSION_PREFIX = "whatsapp:session:"
SESSION_TTL_SECONDS = 48 * 3600
OTP_PREFIX = "whatsapp:otp:"
OTP_ATTEMPTS_PREFIX = "whatsapp:otp_attempts:"
OTP_MAX_ATTEMPTS = 3


class WhatsAppRedisStore:
    """Redis-backed store for sessions and OTPs. Delegates customer lookup to optional PG/store."""

    def __init__(self, fallback_db=None):
        self._redis = None
        self._fallback_db = fallback_db
        self._connect()

    def _connect(self):
        redis_url = os.getenv("REDIS_URL") or os.getenv("REDIS_HOST")
        if not redis_url and os.getenv("REDIS_HOST"):
            redis_url = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', '6379')}"
        if not redis_url:
            raise ValueError("REDIS_URL or REDIS_HOST not set")
        try:
            import redis
            self._redis = redis.from_url(redis_url, decode_responses=True)
            self._redis.ping()
            logger.info("✅ Redis connected for session/OTP store")
        except ImportError:
            raise ImportError("redis package required. Install with: pip install redis")
        except Exception as e:
            raise RuntimeError(f"Redis connection failed: {e}")

    def initialize_tables(self):
        if self._fallback_db and hasattr(self._fallback_db, "initialize_tables"):
            self._fallback_db.initialize_tables()
        return True

    def get_session(self, whatsapp_user_id: str):
        from whatsapp.models import SessionInfo, AuthState
        key = SESSION_PREFIX + whatsapp_user_id
        raw = self._redis.get(key)
        if not raw:
            return None
        try:
            data = json.loads(raw)
            return SessionInfo(
                whatsapp_user_id=data["whatsapp_user_id"],
                customer_id=data.get("customer_id"),
                auth_state=AuthState(data["auth_state"]),
                auth_level=data.get("auth_level", "BASIC"),
                phone_number=data.get("phone_number"),
                created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
                last_activity=datetime.fromisoformat(data["last_activity"].replace("Z", "+00:00")),
                expires_at=datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00")) if data.get("expires_at") else None,
                metadata=data.get("metadata") or {},
            )
        except Exception as e:
            logger.warning(f"Redis get_session parse error: {e}")
            return None

    def create_or_update_session(self, whatsapp_user_id: str, auth_state, phone_number=None,
                                  customer_id=None, expires_at=None, metadata=None):
        from whatsapp.models import SessionInfo, AuthState
        key = SESSION_PREFIX + whatsapp_user_id
        now = datetime.utcnow()
        raw = self._redis.get(key)
        if raw:
            try:
                data = json.loads(raw)
                data["auth_state"] = auth_state.value if hasattr(auth_state, "value") else str(auth_state)
                if phone_number is not None:
                    data["phone_number"] = phone_number
                if customer_id is not None:
                    data["customer_id"] = customer_id
                if expires_at is not None:
                    data["expires_at"] = expires_at.isoformat() if hasattr(expires_at, "isoformat") else str(expires_at)
                if metadata is not None:
                    data["metadata"] = metadata
                data["last_activity"] = now.isoformat() + "Z"
            except Exception:
                data = {}
        else:
            data = {}
        data.setdefault("whatsapp_user_id", whatsapp_user_id)
        data.setdefault("customer_id", customer_id)
        data.setdefault("auth_state", auth_state.value if hasattr(auth_state, "value") else str(auth_state))
        data.setdefault("phone_number", phone_number)
        data.setdefault("created_at", now.isoformat() + "Z")
        data.setdefault("last_activity", now.isoformat() + "Z")
        data.setdefault("expires_at", expires_at.isoformat() + "Z" if expires_at and hasattr(expires_at, "isoformat") else None)
        data.setdefault("metadata", metadata or data.get("metadata") or {})
        meta = data.get("metadata") or {}
        data["auth_level"] = (metadata or {}).get("auth_level") or meta.get("auth_level", "BASIC")
        self._redis.setex(key, SESSION_TTL_SECONDS, json.dumps(data, default=str))
        return SessionInfo(
            whatsapp_user_id=data["whatsapp_user_id"],
            customer_id=data.get("customer_id"),
            auth_state=AuthState(data["auth_state"]),
            auth_level=data.get("auth_level", "BASIC"),
            phone_number=data.get("phone_number"),
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            last_activity=datetime.fromisoformat(data["last_activity"].replace("Z", "+00:00")),
            expires_at=datetime.fromisoformat(data["expires_at"].replace("Z", "+00:00")) if data.get("expires_at") else None,
            metadata=data.get("metadata") or {},
        )

    def store_otp(self, whatsapp_user_id: str, phone_number: str, otp_code: str, expiry_minutes: int = 10) -> str:
        key = OTP_PREFIX + whatsapp_user_id + ":" + phone_number
        attempts_key = OTP_ATTEMPTS_PREFIX + whatsapp_user_id + ":" + phone_number
        payload = json.dumps({"code": otp_code})
        ttl = expiry_minutes * 60
        self._redis.setex(key, ttl, payload)
        self._redis.setex(attempts_key, ttl, "0")
        return key

    def verify_otp(self, whatsapp_user_id: str, phone_number: str, otp_code: str) -> bool:
        key = OTP_PREFIX + whatsapp_user_id + ":" + phone_number
        attempts_key = OTP_ATTEMPTS_PREFIX + whatsapp_user_id + ":" + phone_number
        raw = self._redis.get(key)
        if not raw:
            return False
        try:
            attempts = int(self._redis.get(attempts_key) or 0)
            if attempts >= OTP_MAX_ATTEMPTS:
                self._redis.delete(key)
                self._redis.delete(attempts_key)
                return False
            data = json.loads(raw)
            if data.get("code") == otp_code:
                self._redis.delete(key)
                self._redis.delete(attempts_key)
                return True
            self._redis.incr(attempts_key)
            return False
        except Exception:
            return False

    def get_customer_by_phone(self, phone_number: str) -> Optional[str]:
        if self._fallback_db and hasattr(self._fallback_db, "get_customer_by_phone"):
            return self._fallback_db.get_customer_by_phone(phone_number)
        return None

    def cleanup_expired_otps(self):
        return 0

    def cleanup_expired_sessions(self, expiry_days: int = 30):
        return 0
