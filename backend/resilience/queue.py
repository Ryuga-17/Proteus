import uuid
from typing import Any, Dict, List
from .storage import utc_now_iso


class OperationQueue:
    def __init__(self, store):
        self.store = store

    def enqueue(self, operation_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        job_id = f"JOB-{uuid.uuid4().hex[:10].upper()}"

        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            data.setdefault("queue", {})[job_id] = {
                "job_id": job_id,
                "operation_type": operation_type,
                "payload": payload,
                "status": "queued",
                "attempts": 0,
                "created_at": utc_now_iso(),
                "updated_at": utc_now_iso(),
            }
            return data

        self.store.update(_update)
        return {"job_id": job_id, "status": "queued"}

    def list_jobs(self) -> List[Dict[str, Any]]:
        return list(self.store.get().get("queue", {}).values())

    def mark_done(self, job_id: str, status: str = "completed") -> None:
        def _update(data: Dict[str, Any]) -> Dict[str, Any]:
            job = data.setdefault("queue", {}).get(job_id)
            if job:
                job["status"] = status
                job["attempts"] = job.get("attempts", 0) + 1
                job["updated_at"] = utc_now_iso()
            return data

        self.store.update(_update)
