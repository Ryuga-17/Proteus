import json
import os
import time
from typing import Dict, Any, Optional

class FeatureStore:
    """
    Lightweight Feature Store for AI Agent Models.
    Handles caching, lazy loading, and separation of raw data vs computed features.
    """
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Point to the recommendation agent's data by default for this project structure
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                         "backend", "agentic-core", "worker_agents", "recommendation_agent2")
        else:
            self.data_dir = data_dir
            
        # Raw Data Caches
        self._raw_products: Optional[Dict[str, Any]] = None
        self._raw_profiles: Optional[Dict[str, Any]] = None
        
        # Computed Feature Caches
        self._product_features: Dict[str, Any] = {}
        self._user_features: Dict[str, Any] = {}
        
        # Track load times for TTL invalidation if needed
        self._last_loaded = {}

    def _load_raw_data(self, filename: str) -> list:
        """Helper to load JSON data."""
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: Data file {filepath} not found.")
            return []
        with open(filepath, 'r') as f:
            return json.load(f)

    @property
    def raw_products(self) -> Dict[str, Any]:
        """Lazy load raw products data."""
        if self._raw_products is None:
            data = self._load_raw_data('product.json')
            self._raw_products = {p['product_id']: p for p in data if 'product_id' in p}
            self._last_loaded['products'] = time.time()
        return self._raw_products

    @property
    def raw_profiles(self) -> Dict[str, Any]:
        """Lazy load raw profiles data."""
        if self._raw_profiles is None:
            data = self._load_raw_data('profile.json')
            self._raw_profiles = {p['customer_id']: p for p in data if 'customer_id' in p}
            self._last_loaded['profiles'] = time.time()
        return self._raw_profiles

    def get_product_features(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get computed product features. 
        Separates raw product metadata from computed behavioral/embedding features.
        """
        if product_id in self._product_features:
            return self._product_features[product_id]
            
        raw_product = self.raw_products.get(product_id)
        if not raw_product:
            return None
            
        # Compute features
        features = {
            "product_id": raw_product["product_id"],
            "base_price": raw_product.get("price", 0.0),
            "category_encoded": raw_product.get("category", "unknown"),
            "tags_count": len(raw_product.get("tags", [])),
            # Placeholders for future Azure ML/Ollama computed embeddings
            "embedding_mock": [0.1, 0.2, 0.3] 
        }
        
        self._product_features[product_id] = features
        return features

    def get_user_features(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get computed user features based on profile and history.
        """
        if user_id in self._user_features:
            return self._user_features[user_id]
            
        raw_profile = self.raw_profiles.get(user_id)
        if not raw_profile:
            return None
            
        # Compute features
        past_purchases = raw_profile.get("past_purchases", [])
        features = {
            "user_id": raw_profile["customer_id"],
            "purchase_count": len(past_purchases),
            "loyalty_tier": raw_profile.get("loyalty_points", 0),
            "has_purchased": len(past_purchases) > 0,
            # Represents the behavioral vector representing user interests
            "behavioral_embedding_mock": [0.3, 0.1, 0.4]
        }
        
        self._user_features[user_id] = features
        return features

    def invalidate_cache(self):
        """Clear the cache to force reloading from disk."""
        self._raw_products = None
        self._raw_profiles = None
        self._product_features = {}
        self._user_features = {}

# Global feature store instance
feature_store = FeatureStore()
