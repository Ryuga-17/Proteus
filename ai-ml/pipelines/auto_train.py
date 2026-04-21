import os
import sys
import random
import time
from datetime import datetime

# Path resolutions for importing adjacent modules
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

try:
    from ai_ml.monitoring.metrics import metrics_tracker
    from ai_ml.model_registry_manager import registry_manager
except ImportError:
    # Alternative direct imports if pythonpath isn't strict
    import glob
    sys.path.append(os.path.join(base_dir, "ai-ml", "monitoring"))
    sys.path.append(os.path.join(base_dir, "ai-ml"))
    import metrics
    import model_registry_manager

class AutoTrainPipeline:
    """
    Antigravity trigger: Automated Training Pipeline.
    Evaluates historical data, "trains" a new model, and evaluates it against
    current production metrics. Handles auto-promotion or rejections.
    """
    
    def __init__(self):
        self.metrics_engine = metrics.metrics_tracker
        self.registry = model_registry_manager.registry_manager
        
    def _train_mock_model(self, model_type: str) -> dict:
        """
        Simulates Azure ML / Scikit-Learn training execution.
        Returns the freshly calculated metrics & metadata for the new candidate model.
        """
        print(f"   [Azure ML Hook] Triggering remote/local training for {model_type}...")
        time.sleep(2)  # Simulate training
        
        # We calculate the baseline from actual recent log data.
        # But we mock the new model's performance as slightly randomized around that baseline.
        current_metrics = self.metrics_engine.calculate_historical_metrics()
        
        # Simulate an outcome: sometimes better, sometimes worse
        fluctuation = random.uniform(-0.05, 0.08)
        
        timestamp_str = datetime.utcnow().strftime("%Y%m%d%H%M")
        new_version = f"v{timestamp_str}"
        
        return {
            "version": new_version,
            "path": f"ai-ml/models/{model_type}_v{timestamp_str}.pkl",
            "accuracy": current_metrics["intent_accuracy"] + (fluctuation if model_type == "intent_model" else 0.0),
            "ctr": current_metrics["ctr"] + (fluctuation if model_type == "recommendation_model" else 0.0),
            "conversion_rate": current_metrics["conversion_rate"] + fluctuation * 0.5,
            "created_at": datetime.utcnow().isoformat()
        }

    def evaluate_and_promote(self, model_type: str):
        """
        Main logic: Train -> Evaluate -> Promote/Reject
        """
        print(f"\n Starting Training Pipeline for {model_type}...")
        
        # 1. Train candidate
        candidate_model = self._train_mock_model(model_type)
        
        # 2. Extract active running model
        active_model = self.registry.get_active_model(model_type)
        
        if not active_model:
            print(f" No active {model_type} found in registry. Auto-promoting candidate as baseline.")
            self.registry.promote_model(model_type, candidate_model)
            return
            
        print(f" Evaluation Phase:")
        
        # 3. Compare Metrics (Accuracy if intent, CTR if recommendation)
        promote = False
        rejection_reason = ""
        
        if model_type == "intent_model":
            current_acc = active_model.get("accuracy", 0.0)
            new_acc = candidate_model["accuracy"]
            print(f"   Current Accuracy: {current_acc:.4f} | Candidate: {new_acc:.4f}")
            if new_acc > current_acc:
                promote = True
            else:
                rejection_reason = "Candidate accuracy did not exceed current."
                
        elif model_type == "recommendation_model":
            current_ctr = active_model.get("ctr", 0.0)
            new_ctr = candidate_model["ctr"]
            print(f"   Current CTR: {current_ctr:.4f} | Candidate: {new_ctr:.4f}")
            if new_ctr > current_ctr:
                promote = True
            else:
                rejection_reason = "Candidate CTR did not exceed current."
                
        # 4. Action
        if promote:
            print(f" Evaluation Passed! Promoting {candidate_model['version']} to active tier.")
            self.registry.promote_model(model_type, candidate_model)
        else:
            print(f" Evaluation Failed! Model rejected. Reason: {rejection_reason}")
            # The rollback is inherently "doing nothing" in this stage, but the registry 
            # provides a rollback function if the promoted model crashes the app entirely!
            
    def run_all(self):
        """Triggered daily by APScheduler."""
        self.evaluate_and_promote("recommendation_model")
        self.evaluate_and_promote("intent_model")

if __name__ == "__main__":
    pipeline = AutoTrainPipeline()
    pipeline.run_all()
