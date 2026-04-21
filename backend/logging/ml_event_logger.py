import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

class MLEventLogger:
    """
    Structured Logging System for MLOps Pipeline data collection.
    Logs interactions in partitioned JSON files by month (events_YYYY_MM.json).
    """
    
    def __init__(self, log_dir: str = None):
        # Default to a generic logs directory under backend if not provided
        if log_dir is None:
            self.log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs")
        else:
            self.log_dir = log_dir
            
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
    def _get_log_filepath(self) -> str:
        """Get the current month's log file path (events_YYYY_MM.json)"""
        current_date = datetime.utcnow()
        filename = f"events_{current_date.strftime('%Y_%m')}.json"
        return os.path.join(self.log_dir, filename)

    def log_event(self, 
                  user_id: str, 
                  channel: str, 
                  query: Optional[str] = None, 
                  intent: Optional[str] = None, 
                  recommendation: Optional[List[str]] = None, 
                  click: Optional[List[str]] = None, 
                  purchase_flag: bool = False, 
                  agent_used: Optional[str] = None,
                  extra_metadata: Optional[Dict[str, Any]] = None):
        """
        Log an ML event.
        
        Args:
            user_id: Identifier for the user.
            channel: Channel used (e.g., 'whatsapp', 'web', 'kiosk').
            query: The text query performed.
            intent: The intent predicted by the classifier.
            recommendation: List of product IDs recommended.
            click: List of product IDs clicked.
            purchase_flag: Boolean indicating if a purchase resulted.
            agent_used: The agent which handled the event.
            extra_metadata: Any other custom metadata to store.
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "channel": channel,
            "query": query,
            "intent": intent,
            "recommendation": recommendation if recommendation else [],
            "click": click if click else [],
            "purchase_flag": purchase_flag,
            "agent_used": agent_used,
            "metadata": extra_metadata if extra_metadata else {}
        }
        
        filepath = self._get_log_filepath()
        
        # Append as a single JSON line per event (JSONL format for data processing)
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            print(f"Failed to log ML event: {e}")

# Global instance for usage across app
ml_logger = MLEventLogger()
