from typing import Any, Dict, Optional
from .storage import utc_now_iso


class SessionManager:
    def __init__(self, store):
        self.store = store

    def register_device(self, user_id: str, device_id: str, session_id: str) -> Dict[str, Any]:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            sessions = data.setdefault("sessions", {})
            user_sessions = sessions.setdefault(user_id, {})
            user_sessions[device_id] = {
                "device_id": device_id,
                "session_id": session_id,
                "last_seen": utc_now_iso(),
            }
            sessions[user_id] = user_sessions
            data["sessions"] = sessions
            return data

        updated = self.store.update(_update)
        return updated.get("sessions", {}).get(user_id, {})

    def detect_conflict(self, user_id: str, device_id: str) -> Optional[Dict[str, Any]]:
        sessions = self.store.get().get("sessions", {}).get(user_id, {})
        other_devices = [s for d, s in sessions.items() if d != device_id]
        if other_devices:
            return {"conflict": True, "active_devices": other_devices}
        return None

    def sync_cart(self, user_id: str, cart: Dict[str, Any], action_ts: str) -> Dict[str, Any]:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            carts = data.setdefault("carts", {})
            existing = carts.get(user_id)
            if existing and existing.get("last_action_ts", "") > action_ts:
                data["last_cart_conflict"] = {
                    "user_id": user_id,
                    "reason": "stale_update",
                    "existing_ts": existing.get("last_action_ts"),
                    "incoming_ts": action_ts,
                }
                return data
            carts[user_id] = {
                "user_id": user_id,
                "cart": cart,
                "last_action_ts": action_ts,
                "updated_at": utc_now_iso(),
            }
            data["carts"] = carts
            data.pop("last_cart_conflict", None)
            return data

        updated = self.store.update(_update)
        conflict = updated.get("last_cart_conflict")
        return {"cart": updated.get("carts", {}).get(user_id), "conflict": conflict}
