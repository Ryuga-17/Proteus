from typing import Any, Dict, List, Tuple
from .storage import utc_now_iso


class CustomerIdentityResolver:
    def __init__(self, store):
        self.store = store

    def _normalize(self, profile: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        warnings = []
        normalized = dict(profile)
        if not normalized.get("email") and not normalized.get("phone"):
            warnings.append("missing_contact")
        if not normalized.get("name"):
            normalized["name"] = "Guest Customer"
            warnings.append("name_defaulted")
        normalized.setdefault("loyalty_tier", "bronze")
        return normalized, warnings

    def resolve(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        normalized, warnings = self._normalize(profile)

        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            customers = data.setdefault("customers", {})
            match_id = None
            for customer_id, existing in customers.items():
                if normalized.get("email") and existing.get("email") == normalized.get("email"):
                    match_id = customer_id
                    break
                if normalized.get("phone") and existing.get("phone") == normalized.get("phone"):
                    match_id = customer_id
                    break
            if match_id:
                existing = customers[match_id]
                if normalized.get("email") and existing.get("email") and normalized.get("email") != existing.get("email"):
                    warnings.append("email_conflict")
                if normalized.get("phone") and existing.get("phone") and normalized.get("phone") != existing.get("phone"):
                    warnings.append("phone_conflict")
                existing.update({k: v for k, v in normalized.items() if v})
                existing["updated_at"] = utc_now_iso()
                customers[match_id] = existing
            else:
                match_id = normalized.get("customer_id") or f"CUST-{len(customers)+1:04d}"
                normalized["customer_id"] = match_id
                normalized["created_at"] = utc_now_iso()
                normalized["updated_at"] = utc_now_iso()
                customers[match_id] = normalized
            data["customers"] = customers
            data["last_customer_warnings"] = warnings
            data["last_customer_id"] = match_id
            return data

        updated = self.store.update(_update)
        return {
            "profile": updated.get("customers", {}).get(updated.get("last_customer_id", "")),
            "warnings": updated.get("last_customer_warnings", []),
        }

    def merge_profiles(self, primary_id: str, secondary_id: str) -> Dict[str, Any]:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            customers = data.setdefault("customers", {})
            primary = customers.get(primary_id)
            secondary = customers.get(secondary_id)
            if not primary or not secondary:
                data["last_merge_error"] = "profile_missing"
                return data
            for key, value in secondary.items():
                if not primary.get(key) and value:
                    primary[key] = value
            primary["updated_at"] = utc_now_iso()
            customers[primary_id] = primary
            customers.pop(secondary_id, None)
            data["customers"] = customers
            data.pop("last_merge_error", None)
            return data

        updated = self.store.update(_update)
        if updated.get("last_merge_error"):
            return {"success": False, "message": "Profile missing"}
        return {"success": True, "profile": updated.get("customers", {}).get(primary_id)}
