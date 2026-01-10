# Recommendation Agent - Voice Search Feature

## Overview

The Recommendation Agent processes voice-based, natural language product queries and returns structured, personalized recommendations. It implements a complete pipeline from speech-to-text to personalized ranking.

## Architecture

```
User Voice Input
    ↓
[STT Service] → Raw Text
    ↓
[NLU Agent] → Structured Query (product_type, occasion, attributes)
    ↓
[Vector Retrieval] → Candidate Items (50 items from Qdrant)
    ↓
[DeepFM Ranking] → Top 10 Personalized Recommendations
    ↓
User receives ranked results with scores and reasoning
```

## Components

### 1. Models (`models.py`)
- `VoiceQueryInput`: Input model for voice queries
- `StructuredQuery`: NLU output with product_type, occasion_tag, implied_attributes
- `RecommendationResult`: Final recommendation with item_id, score, reasoning
- `UserContext`: User preferences from Redis (simulated)

### 2. Voice Processor (`voice_processor.py`)
- `STTService`: Simulated speech-to-text service
- `LLMClient`: Simulated LLM for NLU extraction
- `QdrantClient`: Simulated vector database for retrieval
- `DeepFMRanker`: Simulated ranking model
- `process_voice_query()`: Main orchestration function

### 3. Agent (`agents.py`)
- `recommendation_agent`: CrewAI agent for handling recommendation requests

### 4. Tools (`tools.py`)
- `VoiceQueryTool`: Tool that wraps the voice query processing

## Usage

### Direct Usage (Testing)

```python
import asyncio
from voice_processor import process_voice_query, stt_service

# Set query text (simulates STT output)
stt_service.set_override_text("looking for a shirt for date")

# Process query
results = await process_voice_query(
    audio_input=b"mock_audio",
    user_id="USER-123"
)

# Results is a list of RecommendationResult objects
for result in results:
    print(f"{result.item_id}: {result.score} - {result.reasoning}")
```

### Through Orchestrator (Production)

```python
from Orchestrator.main import handle_custom_request

# The orchestrator will route recommendation requests automatically
result = handle_custom_request(
    "looking for a shirt for date",
    user_id="USER-123"
)
```

## Testing

### Run Demo
```bash
cd "Recommendation agent"
python demo.py
```

### Run Tests
```bash
python test_voice_query.py
```

### Run Main Test
```bash
python main.py
```

## Pipeline Details

### Step 1: Speech-to-Text (STT)
- Simulated STT service converts audio bytes to text
- In production: Would call actual STT API (e.g., Google Speech-to-Text)

### Step 2: Natural Language Understanding (NLU)
- Extracts structured information from raw text:
  - `product_type`: Main product category
  - `occasion_tag`: Use case/occasion
  - `implied_attributes`: Style/attribute tags
- In production: Would use actual LLM API with structured output

### Step 3: Vector Retrieval
- Combines product_type and attributes into search query
- Queries Qdrant vector database
- Returns top 50 candidate item IDs
- In production: Would use actual Qdrant instance with product embeddings

### Step 4: DeepFM Ranking
- Combines user context and structured query
- Scores candidates based on:
  - Product type match
  - Attribute overlap
  - User preferences (size, color, price range)
  - Past purchase similarity
  - Occasion matching
- Returns top 10 ranked recommendations
- In production: Would use actual trained DeepFM model

## Integration with Orchestrator

The Recommendation Agent is integrated into the Orchestrator system:

1. **Routing Tool**: `route_to_recommendation()` in `Orchestrator/orchestrator_tools.py`
2. **Intent Detection**: Orchestrator recognizes recommendation keywords
3. **Agent Access**: Available through Orchestrator's routing system

## Example Queries

- "looking for a shirt for date"
- "I need formal pants for office"
- "show me workout shoes"
- "find a casual dress"
- "recommend a jacket for winter"

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- `crewai`: Agent framework
- `langchain-openai`: LLM integration
- `pydantic`: Data validation
- `asyncio`: Async processing

## Future Enhancements

1. **Real STT Integration**: Connect to actual STT API
2. **Real LLM Integration**: Use actual LLM for better NLU
3. **Qdrant Integration**: Connect to actual Qdrant instance
4. **DeepFM Model**: Deploy actual trained ranking model
5. **Redis Integration**: Fetch real user context from Redis
6. **Multi-modal Search**: Support image + text queries
7. **Conversational Recommendations**: Multi-turn recommendation dialogs




