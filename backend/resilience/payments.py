import uuid
from typing import Any, Dict, Optional
from .storage import utc_now_iso


class PaymentGateway:
    def __init__(self, store):
        self.store = store

    def _get_idempotency(self, key: str) -> Optional[Dict[str, Any]]:
        return self.store.get().get("idempotency", {}).get(key)

    def _get_group_success(self, group_key: str) -> Optional[Dict[str, Any]]:
        return self.store.get().get("group_success", {}).get(group_key)

    def _set_idempotency(self, key: str, value: Dict[str, Any]) -> None:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data.setdefault("idempotency", {})[key] = value
            return data

        self.store.update(_update)

    def _set_group_success(self, group_key: str, value: Dict[str, Any]) -> None:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data.setdefault("group_success", {})[group_key] = value
            return data

        self.store.update(_update)

    def process_payment(
        self,
        amount: float,
        currency: str,
        channel: str,
        idempotency_key: str,
        group_key: str,
        simulate_timeout: bool = False,
        simulate_failure: bool = False,
        attempt: int = 1,
    ) -> Dict[str, Any]:
        group_success = self._get_group_success(group_key)
        if group_success:
            return group_success

        existing = self._get_idempotency(idempotency_key)
        if existing:
            return existing

        if simulate_timeout:
            result = {
                "status": "timeout",
                "transaction_id": None,
                "channel": channel,
                "amount": amount,
                "currency": currency,
                "attempt": attempt,
                "created_at": utc_now_iso(),
            }
            return result

        if simulate_failure:
            result = {
                "status": "failed",
                "transaction_id": None,
                "channel": channel,
                "amount": amount,
                "currency": currency,
                "attempt": attempt,
                "created_at": utc_now_iso(),
            }
            self._set_idempotency(idempotency_key, result)
            return result

        result = {
            "status": "success",
            "transaction_id": f"PAY-{uuid.uuid4().hex[:12].upper()}",
            "channel": channel,
            "amount": amount,
            "currency": currency,
            "attempt": attempt,
            "created_at": utc_now_iso(),
        }
        self._set_idempotency(idempotency_key, result)
        self._set_group_success(group_key, result)
        return result
