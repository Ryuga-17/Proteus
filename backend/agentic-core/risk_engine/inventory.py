import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple
from .storage import utc_now_iso


class InventoryManager:
    def __init__(self, store):
        self.store = store

    def _purge_expired_reservations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        reservations = data.get("reservations", {})
        active = {}
        now_ts = utc_now_iso()
        for res_id, res in reservations.items():
            if res.get("expires_at", "") > now_ts:
                active[res_id] = res
        data["reservations"] = active
        return data

    def _reserved_by_sku(self, data: Dict[str, Any], location_id: str) -> Dict[str, int]:
        reserved = {}
        for res in data.get("reservations", {}).values():
            if res.get("location_id") != location_id:
                continue
            for item in res.get("items", []):
                sku = item["sku"]
                reserved[sku] = reserved.get(sku, 0) + item["quantity"]
        return reserved

    def get_stock_snapshot(self) -> Dict[str, Any]:
        return self.store.get().get("stock", {})

    def reserve_items(
        self,
        location_id: str,
        items: List[Dict[str, Any]],
        ttl_seconds: int = 600,
    ) -> Tuple[bool, str, List[str]]:
        reservation_id = f"RSV-{uuid.uuid4().hex[:10].upper()}"

        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data = self._purge_expired_reservations(data)
            stock = data.get("stock", {})
            reserved_map = self._reserved_by_sku(data, location_id)
            conflicts = []
            for item in items:
                sku = item["sku"]
                qty = item["quantity"]
                available = stock.get(location_id, {}).get(sku, 0) - reserved_map.get(sku, 0)
                if available < qty:
                    conflicts.append(f"{sku}: available {available}, requested {qty}")
            if conflicts:
                data["last_reservation_error"] = {
                    "reservation_id": reservation_id,
                    "conflicts": conflicts,
                }
                return data

            expires_at = (datetime.utcnow() + timedelta(seconds=ttl_seconds)).isoformat() + "Z"
            data.setdefault("reservations", {})[reservation_id] = {
                "reservation_id": reservation_id,
                "location_id": location_id,
                "items": items,
                "expires_at": expires_at,
                "created_at": utc_now_iso(),
                "baseline_stock": stock.get(location_id, {}),
            }
            data.pop("last_reservation_error", None)
            return data

        updated = self.store.update(_update)
        error = updated.get("last_reservation_error")
        if error and error.get("reservation_id") == reservation_id:
            return False, reservation_id, error.get("conflicts", [])
        return True, reservation_id, []

    def confirm_reservation(self, reservation_id: str) -> Tuple[bool, str]:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data = self._purge_expired_reservations(data)
            reservations = data.get("reservations", {})
            reservation = reservations.get(reservation_id)
            if not reservation:
                data["last_confirmation_error"] = "Reservation missing or expired"
                return data

            stock = data.get("stock", {})
            location_id = reservation["location_id"]
            for item in reservation.get("items", []):
                sku = item["sku"]
                qty = item["quantity"]
                if stock.get(location_id, {}).get(sku, 0) < qty:
                    data["last_confirmation_error"] = f"Insufficient stock for {sku}"
                    return data
            for item in reservation.get("items", []):
                sku = item["sku"]
                qty = item["quantity"]
                stock.setdefault(location_id, {})[sku] = stock.get(location_id, {}).get(sku, 0) - qty

            reservations.pop(reservation_id, None)
            data["stock"] = stock
            data["reservations"] = reservations
            data.pop("last_confirmation_error", None)
            return data

        updated = self.store.update(_update)
        error = updated.get("last_confirmation_error")
        if error:
            return False, error
        return True, "confirmed"

    def release_reservation(self, reservation_id: str) -> None:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data = self._purge_expired_reservations(data)
            data.get("reservations", {}).pop(reservation_id, None)
            return data

        self.store.update(_update)

    def revalidate_reservation(self, reservation_id: str) -> Tuple[bool, str]:
        data = self.store.get()
        data = self._purge_expired_reservations(data)
        reservation = data.get("reservations", {}).get(reservation_id)
        if not reservation:
            return False, "Reservation expired"
        location_id = reservation["location_id"]
        stock = data.get("stock", {})
        baseline = reservation.get("baseline_stock", {})
        reserved_map = self._reserved_by_sku(data, location_id)
        for item in reservation.get("items", []):
            sku = item["sku"]
            qty = item["quantity"]
            if stock.get(location_id, {}).get(sku, 0) < baseline.get(sku, 0):
                return False, f"Stock changed after reservation for {sku}"
            available = stock.get(location_id, {}).get(sku, 0) - reserved_map.get(sku, 0) + qty
            if available < qty:
                return False, f"Stock changed for {sku}"
        return True, "valid"

    def adjust_stock(self, location_id: str, sku: str, delta: int) -> None:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            stock = data.setdefault("stock", {})
            stock.setdefault(location_id, {})
            stock[location_id][sku] = max(0, stock[location_id].get(sku, 0) + delta)
            return data

        self.store.update(_update)
