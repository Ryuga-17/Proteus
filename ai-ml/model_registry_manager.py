import json
import os
import shutil
from typing import Dict, Any, Optional

class ModelRegistryManager:
    """
    Manages the model_registry.json file.
    Provides safe reading, updating, and rollbacks for the MLOps pipeline.
    """
    
    def __init__(self, registry_path: str = None):
        if registry_path is None:
            self.registry_path = os.path.join(os.path.dirname(__file__), "model_registry.json")
        else:
            self.registry_path = registry_path
            
    def _load_registry(self) -> Dict[str, Any]:
        """Loads the registry safely."""
        try:
            with open(self.registry_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading model registry: {e}")
            return {}

    def _save_registry(self, data: Dict[str, Any]) -> bool:
        """Saves the registry safely."""
        try:
            # Create a backup before saving
            if os.path.exists(self.registry_path):
                shutil.copy2(self.registry_path, f"{self.registry_path}.bak")
                
            with open(self.registry_path, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving model registry: {e}")
            return False

    def get_active_model(self, model_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the currently active (promoted) model config.
        e.g. model_type = 'recommendation_model'
        """
        registry = self._load_registry()
        model_group = registry.get(model_type, {})
        return model_group.get("current")

    def promote_model(self, model_type: str, new_model_metadata: Dict[str, Any]) -> bool:
        """
        Promote a new model. The existing 'current' model moves to 'previous'.
        """
        registry = self._load_registry()
        
        if model_type not in registry:
            registry[model_type] = {"current": None, "previous": None}
            
        # Shift current to previous
        current_model = registry[model_type].get("current")
        registry[model_type]["previous"] = current_model
        
        # Set new model as current
        registry[model_type]["current"] = new_model_metadata
        
        print(f" MLOPS: Promoted new {model_type} version {new_model_metadata.get('version')}")
        return self._save_registry(registry)

    def rollback_to_previous_model(self, model_type: str) -> bool:
        """
        Rollback the model_type to its previous version if the new model fails.
        """
        registry = self._load_registry()
        model_group = registry.get(model_type)
        
        if not model_group:
            print(f" MLOPS: Cannot rollback {model_type}. Not found in registry.")
            return False
            
        previous_model = model_group.get("previous")
        
        if not previous_model:
            print(f" MLOPS: Cannot rollback {model_type}. No previous model exists.")
            return False
            
        # Perform rollback
        current_model = model_group.get("current")
        print(f" MLOPS: Rolling back {model_type} from {current_model.get('version')} to {previous_model.get('version')}")
        
        # We restore previous to current. We can keep previous as it is or nullify it.
        # Nullifying it prevents double-rollbacks.
        registry[model_type]["current"] = previous_model
        registry[model_type]["previous"] = None
        
        return self._save_registry(registry)

# Global Instance
registry_manager = ModelRegistryManager()
