"""
Voice Query Processing System V2 - Production Ready
Uses real Ollama embeddings and Qdrant vector database
"""
import json
import asyncio
import os
from typing import List, Dict, Any, Optional
from app import OllamaClient

# Try to import Qdrant client
try:
    from qdrant_client import QdrantClient as Qdrant
    from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    print("⚠️  Qdrant client not installed. Install with: pip install qdrant-client")

# Load product and profile data
def load_product_data():
    """Load product data from JSON file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        product_file = os.path.join(current_dir, 'product.json')
        with open(product_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading product data: {e}")
        return []

def load_profile_data():
    """Load customer profile data from JSON file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        profile_file = os.path.join(current_dir, 'profile.json')
        with open(profile_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading profile data: {e}")
        return []

# Global data
PRODUCTS = load_product_data()
PROFILES = load_profile_data()

# Initialize Ollama client
ollama_client = OllamaClient()

# Initialize Qdrant client (if available)
qdrant_client = None
if QDRANT_AVAILABLE:
    try:
        qdrant_client = Qdrant(host="localhost", port=6333)
        print("✅ Connected to Qdrant at localhost:6333")
    except Exception as e:
        print(f"⚠️  Could not connect to Qdrant: {e}")
        print("   Using fallback search method")


async def generate_embedding(text: str) -> List[float]:
    """Generate embedding using Ollama"""
    try:
        embedding = ollama_client.get_embedding(text)
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []


async def search_qdrant(query_vector: List[float], query_text: str = "", filters: Optional[Dict] = None, limit: int = 10) -> List[Dict]:
    """Search Qdrant vector database"""
    if not QDRANT_AVAILABLE or qdrant_client is None:
        # Fallback: simple keyword search
        return fallback_search(query_text if query_text else "product", limit)
    
    try:
        # Build filter if provided
        query_filter = None
        if filters:
            conditions = []
            if filters.get('gender'):
                conditions.append(
                    FieldCondition(key="gender", match=MatchValue(value=filters['gender']))
                )
            if filters.get('category'):
                conditions.append(
                    FieldCondition(key="category", match=MatchValue(value=filters['category']))
                )
            if filters.get('tags'):
                conditions.append(
                    FieldCondition(key="tags", match=MatchAny(any=filters['tags']))
                )
            
            if conditions:
                query_filter = Filter(must=conditions)
        
        # Search Qdrant
        results = qdrant_client.query_points(
            collection_name="products",
            query=query_vector,
            query_filter=query_filter,
            with_payload=True,
            limit=limit
        )
        
        # Format results
        formatted_results = []
        for point in results.points:
            formatted_results.append({
                'product_id': point.id,
                'score': point.score,
                'payload': point.payload
            })
        
        return formatted_results
        
    except Exception as e:
        print(f"Error searching Qdrant: {e}")
        return fallback_search(query_text if query_text else "product", limit)


def fallback_search(query_text: str, limit: int = 10) -> List[Dict]:
    """Fallback search using keyword matching"""
    query_lower = query_text.lower()
    query_terms = query_lower.split()
    
    scored_products = []
    for product in PRODUCTS:
        score = 0.0
        
        # Match in title
        if any(term in product.get('title', '').lower() for term in query_terms):
            score += 2.0
        
        # Match in description
        if any(term in product.get('description', '').lower() for term in query_terms):
            score += 1.0
        
        # Match in tags
        tags = product.get('tags', [])
        if any(term in ' '.join(tags).lower() for term in query_terms):
            score += 1.5
        
        if score > 0:
            scored_products.append({
                'product_id': product.get('product_id'),
                'score': score,
                'payload': product
            })
    
    # Sort and return top results
    scored_products.sort(key=lambda x: x['score'], reverse=True)
    return scored_products[:limit]


def get_user_profile(user_id: str) -> Optional[Dict]:
    """Get user profile from loaded data"""
    for profile in PROFILES:
        if profile.get('customer_id') == user_id:
            return profile
    return None


def rank_results(results: List[Dict], user_id: str, query_text: str) -> List[Dict]:
    """Rank results based on user profile and query"""
    user_profile = get_user_profile(user_id)
    
    if not user_profile:
        # No profile, return results as-is
        return results
    
    # Get past purchases
    past_purchases = set(user_profile.get('past_purchases', []))
    
    # Rank each result
    ranked_results = []
    for result in results:
        product = result.get('payload', {})
        product_id = result.get('product_id')
        
        # Base score from vector similarity
        base_score = result.get('score', 0.0)
        
        # Boost if not previously purchased
        if product_id not in past_purchases:
            base_score += 0.1
        
        # Check for preferred categories/brands from past purchases
        past_product_categories = set()
        past_product_brands = set()
        for pid in past_purchases:
            for p in PRODUCTS:
                if p.get('product_id') == pid:
                    past_product_categories.add(p.get('category', ''))
                    past_product_brands.add(p.get('brand', ''))
                    break
        
        if product.get('category') in past_product_categories:
            base_score += 0.15
        
        if product.get('brand') in past_product_brands:
            base_score += 0.1
        
        # Generate reasoning
        reasoning_parts = []
        if product_id not in past_purchases:
            reasoning_parts.append("new to you")
        if product.get('category') in past_product_categories:
            reasoning_parts.append("matches your preferred category")
        if product.get('brand') in past_product_brands:
            reasoning_parts.append("from a brand you've purchased before")
        
        reasoning = ", ".join(reasoning_parts) if reasoning_parts else "recommended based on query"
        
        ranked_results.append({
            'product_id': product_id,
            'title': product.get('title'),
            'price': product.get('price', 0),
            'score': min(1.0, base_score),
            'reasoning': reasoning,
            **product
        })
    
    # Sort by score
    ranked_results.sort(key=lambda x: x['score'], reverse=True)
    
    return ranked_results[:10]


async def process_voice_query_v2(query_text: str, user_id: str) -> List[Dict]:
    """
    Main orchestration function for voice query processing V2
    Uses real Ollama and Qdrant services
    """
    # Step 1: Generate query embedding
    query_embedding = await generate_embedding(query_text)
    
    if not query_embedding:
        # Fallback to keyword search
        results = fallback_search(query_text, limit=50)
    else:
        # Step 2: Search Qdrant
        # Extract basic filters from query (simple extraction)
        filters = {}
        query_lower = query_text.lower()
        
        # Try to extract gender
        if any(word in query_lower for word in ['men', 'male', 'man', "men's"]):
            filters['gender'] = 'Male'
        elif any(word in query_lower for word in ['women', 'female', 'woman', "women's"]):
            filters['gender'] = 'Female'
        
        # Try to extract category
        category_keywords = {
            'dress': 'Dresses',
            'shoe': 'Footwear',
            'shirt': 'Tops',
            'pant': 'Bottoms',
            'suit': 'Suits',
            'jacket': 'Outerwear'
        }
        for keyword, category in category_keywords.items():
            if keyword in query_lower:
                filters['category'] = category
                break
        
        # Search Qdrant
        results = await search_qdrant(query_embedding, query_text=query_text, filters=filters if filters else None, limit=50)
    
    # Step 3: Rank results based on user profile
    ranked_results = rank_results(results, user_id, query_text)
    
    return ranked_results

