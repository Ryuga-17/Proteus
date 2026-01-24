import uuid
from enum import Enum
from typing import Any, Dict, Optional
from .storage import utc_now_iso


class TransactionState(str, Enum):
    INITIATED = "INITIATED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    INVENTORY_CONFIRMED = "INVENTORY_CONFIRMED"
    ORDER_CONFIRMED = "ORDER_CONFIRMED"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


ALLOWED_TRANSITIONS = {
    TransactionState.INITIATED: [TransactionState.PAYMENT_PENDING, TransactionState.CANCELLED],
    TransactionState.PAYMENT_PENDING: [TransactionState.PAYMENT_SUCCESS, TransactionState.FAILED],
    TransactionState.PAYMENT_SUCCESS: [TransactionState.INVENTORY_CONFIRMED, TransactionState.FAILED],
    TransactionState.INVENTORY_CONFIRMED: [TransactionState.ORDER_CONFIRMED, TransactionState.FAILED],
    TransactionState.ORDER_CONFIRMED: [TransactionState.FULFILLED, TransactionState.CANCELLED],
    TransactionState.FULFILLED: [],
    TransactionState.CANCELLED: [],
    TransactionState.FAILED: [],
}


class TransactionManager:
    def __init__(self, store):
        self.store = store

    def create(self, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        record = {
            "transaction_id": transaction_id,
            "state": TransactionState.INITIATED.value,
            "user_id": user_id,
            "payload": payload,
            "version": 1,
            "created_at": utc_now_iso(),
            "updated_at": utc_now_iso(),
            "payment": {},
            "inventory": {},
            "order": {},
            "errors": [],
        }

        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data.setdefault("transactions", {})[transaction_id] = record
            return data

        self.store.update(_update)
        return record

    def get(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        return self.store.get().get("transactions", {}).get(transaction_id)

    def transition(self, transaction_id: str, target_state: TransactionState) -> Dict[str, Any]:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            transactions = data.setdefault("transactions", {})
            record = transactions.get(transaction_id)
            if not record:
                return data
            current_state = TransactionState(record["state"])
            if current_state == target_state:
                return data
            if target_state not in ALLOWED_TRANSITIONS.get(current_state, []):
                record.setdefault("errors", []).append(
                    {
                        "error": "invalid_transition",
                        "from": current_state.value,
                        "to": target_state.value,
                        "ts": utc_now_iso(),
                    }
                )
                transactions[transaction_id] = record
                data["transactions"] = transactions
                return data

            record["state"] = target_state.value
            record["version"] = record.get("version", 0) + 1
            record["updated_at"] = utc_now_iso()
            transactions[transaction_id] = record
            data["transactions"] = transactions
            return data

        updated = self.store.update(_update)
        return updated.get("transactions", {}).get(transaction_id)

    def update_payment(self, transaction_id: str, payment: Dict[str, Any]) -> None:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            record = data.setdefault("transactions", {}).get(transaction_id)
            if record:
                record["payment"] = payment
                record["updated_at"] = utc_now_iso()
            return data

        self.store.update(_update)

    def update_inventory(self, transaction_id: str, inventory: Dict[str, Any]) -> None:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            record = data.setdefault("transactions", {}).get(transaction_id)
            if record:
                record["inventory"] = inventory
                record["updated_at"] = utc_now_iso()
            return data

        self.store.update(_update)

    def update_order(self, transaction_id: str, order: Dict[str, Any]) -> None:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            record = data.setdefault("transactions", {}).get(transaction_id)
            if record:
                record["order"] = order
                record["updated_at"] = utc_now_iso()
            return data

        self.store.update(_update)
