import os
import json
import glob
from datetime import datetime
from typing import List, Dict, Any

class AutoDataPipeline:
    """
    MLOps pipeline trigger: Automated Data Pipeline
    Parses logs, cleans data, and generates training datasets.
    """
    
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.log_dir = os.path.join(base_dir, "backend", "data", "logs")
        self.dataset_dir = os.path.join(base_dir, "ai-ml", "data", "datasets")
        
        # Ensure dataset directory exists
        os.makedirs(self.dataset_dir, exist_ok=True)
        
    def collect_and_clean_data(self) -> List[Dict[str, Any]]:
        """
        Gathers all log partitions, filters out corrupted data.
        """
        if not os.path.exists(self.log_dir):
            print("No log directory found for data pipeline.")
            return []
            
        log_files = glob.glob(os.path.join(self.log_dir, "events_*.json"))
        clean_data = []
        
        for filepath in log_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            event = json.loads(line)
                            # Basic cleaning: Must have a user_id and a timestamp
                            if event.get("user_id") and event.get("timestamp"):
                                clean_data.append(event)
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
                
        return clean_data

    def generate_training_datasets(self, data: List[Dict[str, Any]]):
        """
        Transforms clean log data into structured ML datasets.
        """
        if not data:
            print("No data available to generate datasets.")
            return
            
        # Example struct for an Intent Classification Dataset
        intent_dataset = []
        # Example struct for a Recommendation Dataset (Collaborative filtering tuples)
        recommender_dataset = []
        
        for event in data:
            query = event.get("query")
            intent = event.get("intent")
            
            if query and intent:
                intent_dataset.append({"text": query, "label": intent})
                
            user_id = event.get("user_id")
            clicks = event.get("click", [])
            purchase = int(event.get("purchase_flag", False))
            
            for item_id in clicks:
                # Interaction score: 1 for click, 5 for purchase
                score = 5 if purchase else 1
                recommender_dataset.append({
                    "user_id": user_id,
                    "item_id": item_id,
                    "interaction_score": score
                })
                
        # Save datasets locally (can be synced to Azure Blob Storage via hooks)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        intent_path = os.path.join(self.dataset_dir, f"intent_dataset_{timestamp}.json")
        rec_path = os.path.join(self.dataset_dir, f"recommender_dataset_{timestamp}.json")
        
        try:
            with open(intent_path, "w", encoding="utf-8") as f:
                json.dump(intent_dataset, f, indent=2)
            with open(rec_path, "w", encoding="utf-8") as f:
                json.dump(recommender_dataset, f, indent=2)
            print(f" Data Pipeline: Successfully generated datasets at {self.dataset_dir}")
        except Exception as e:
            print(f" Data Pipeline Error: Failed to save datasets -> {e}")

    def run_pipeline(self):
        """Executes the full pipeline manually or via APScheduler."""
        print(" Starting Automated Data Pipeline...")
        clean_data = self.collect_and_clean_data()
        print(f"   Gathered {len(clean_data)} valid interaction records.")
        self.generate_training_datasets(clean_data)
        print(" Data Pipeline execution complete.")

if __name__ == "__main__":
    pipeline = AutoDataPipeline()
    pipeline.run_pipeline()
