import uuid
from typing import Any, Dict, Optional
from .storage import utc_now_iso


class OrderManager:
    def __init__(self, store, grace_minutes: int = 30):
        self.store = store
        self.grace_minutes = grace_minutes

    def create_order(self, user_id: str, items: Dict[str, Any], total_amount: float, channel: str = "online") -> Dict[str, Any]:
        order_id = f"ORD-{uuid.uuid4().hex[:10].upper()}"
        record = {
            "order_id": order_id,
            "user_id": user_id,
            "items": items,
            "total_amount": total_amount,
            "status": "confirmed",
            "fulfillment_status": "pending",
            "delivery_method": "standard",
            "channel": channel,
            "created_at": utc_now_iso(),
            "updated_at": utc_now_iso(),
        }

        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data.setdefault("orders", {})[order_id] = record
            return data

        self.store.update(_update)
        return record

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        return self.store.get().get("orders", {}).get(order_id)

    def update_order(self, order_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            order = data.setdefault("orders", {}).get(order_id)
            if not order:
                return data
            order.update(updates)
            order["updated_at"] = utc_now_iso()
            data["orders"][order_id] = order
            return data

        updated = self.store.update(_update)
        return updated.get("orders", {}).get(order_id)

    def request_return(self, order_id: str, reason: str, return_type: str = "refund") -> Dict[str, Any]:
        return_id = f"RET-{uuid.uuid4().hex[:10].upper()}"

        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data.setdefault("returns", {})[return_id] = {
                "return_id": return_id,
                "order_id": order_id,
                "reason": reason,
                "type": return_type,
                "status": "requested",
                "created_at": utc_now_iso(),
                "updated_at": utc_now_iso(),
            }
            return data

        self.store.update(_update)
        return {"return_id": return_id, "status": "requested"}
