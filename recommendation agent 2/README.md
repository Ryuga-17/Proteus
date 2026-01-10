# Recommendation Agent 2 - Production Ready

## Overview

Recommendation Agent 2 is a production-ready product recommendation system that uses:
- **Real Ollama** for generating embeddings
- **Real Qdrant** vector database for semantic search
- **Real product data** (100 products from `product.json`)
- **Real customer profiles** (50 customers from `profile.json`)

## Key Differences from Recommendation Agent

| Feature | Recommendation Agent | Recommendation Agent 2 |
|---------|---------------------|----------------------|
| Embeddings | Simulated | Real Ollama |
| Vector DB | Simulated | Real Qdrant |
| Product Data | 1000 mock products | 100 real products |
| Customer Data | Simulated profiles | 50 real customer profiles |
| Production Ready | No | Yes |

## Architecture

```
User Query → Ollama Embedding → Qdrant Vector Search 
→ Metadata Filtering → User Profile Ranking → Recommendations
```

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Ollama Server
Ensure Ollama is running at `http://192.168.0.160:11434` (or update in `app.py`)

### 3. Start Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. Load Products into Qdrant
You'll need to create embeddings and load products. See `description.md` for details.

## Usage

### Through Orchestrator
```python
from Orchestrator.main import handle_custom_request

result = handle_custom_request(
    "looking for a shirt for date",
    user_id="CUST001"
)
```

### Direct Usage
```python
from voice_processor_v2 import process_voice_query_v2

results = await process_voice_query_v2(
    "looking for a shirt for date",
    "CUST001"
)
```

## Files

- `agents.py` - CrewAI agent definition
- `tools.py` - Agent tools
- `voice_processor_v2.py` - Core processing pipeline
- `app.py` - Ollama client
- `product.json` - Product catalog (100 products)
- `profile.json` - Customer profiles (50 customers)
- `description.md` - Technical documentation

## Integration

This agent is fully integrated with the Orchestrator system:
- Routing tool: `route_to_recommendation_v2()`
- Intent detection recognizes recommendation keywords
- Accessible through `handle_custom_request()`

## Features

✅ Real vector embeddings via Ollama
✅ Real Qdrant vector database
✅ Real product catalog
✅ Real customer profiles
✅ Personalized recommendations
✅ Metadata filtering
✅ User profile-based ranking




