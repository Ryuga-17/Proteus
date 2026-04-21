import json
import os
import glob
from typing import Dict, Any

class MetricsTracker:
    """
    Calculates ML system metrics explicitly from historical log data.
    """
    
    def __init__(self, log_dir: str = None):
        if log_dir is None:
            self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "backend", "data", "logs")
        else:
            self.log_dir = log_dir

    def calculate_historical_metrics(self) -> Dict[str, float]:
        """
        Parses all log files to calculate aggregate metrics.
        Returns CTR and Conversion Rate.
        """
        total_sessions = 0
        total_purchases = 0
        total_recommendations = 0
        total_clicks = 0
        correct_intents = 0
        total_intent_predictions = 0
        
        if not os.path.exists(self.log_dir):
            return {"ctr": 0.0, "conversion_rate": 0.0, "intent_accuracy": 0.0}

        # Parse all partition files
        log_files = glob.glob(os.path.join(self.log_dir, "events_*.json"))
        
        for filepath in log_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        event = json.loads(line)
                        
                        # Conversion logic
                        total_sessions += 1
                        if event.get("purchase_flag"):
                            total_purchases += 1
                            
                        # CTR logic
                        recs = event.get("recommendation", [])
                        clicks = event.get("click", [])
                        
                        if recs:
                            # If they got recommendations, we increment the pool
                            # A simple CTR formulation: ratio of interaction events that resulted in a click
                            total_recommendations += 1
                            if clicks:
                                total_clicks += 1
                                
                        # Intent accuracy (Mock logic: if purchase happened after intent, intent was accurate)
                        # In reality, this requires explicit user feedback or a human-in-the-loop audit data structure
                        if event.get("intent"):
                            total_intent_predictions += 1
                            if event.get("purchase_flag") or len(clicks) > 0:
                                correct_intents += 1
                                
            except Exception as e:
                print(f"Error parsing log file {filepath}: {e}")
                
        # Calculate final formulas
        # CTR = clicks (sessions with a click) / recommendations (sessions with a recommendation presented)
        ctr = total_clicks / total_recommendations if total_recommendations > 0 else 0.0
        
        # Conversion Rate = purchases / sessions
        conversion_rate = total_purchases / total_sessions if total_sessions > 0 else 0.0
        
        # Intent Accuracy
        intent_accuracy = correct_intents / total_intent_predictions if total_intent_predictions > 0 else 0.0
        
        return {
            "ctr": round(ctr, 4),
            "conversion_rate": round(conversion_rate, 4),
            "intent_accuracy": round(intent_accuracy, 4)
        }

metrics_tracker = MetricsTracker()
