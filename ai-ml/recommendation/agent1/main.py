"""
Main entry point for Recommendation Agent
Can be used for testing the agent independently
"""
import asyncio
from voice_processor import process_voice_query
from models import RecommendationResult
import json


async def test_voice_query():
    """Test the voice query processing pipeline"""
    print("=" * 70)
    print("  Testing Voice Query Processing Pipeline")
    print("=" * 70)
    print()
    
    # Simulate audio input (in production, this would be actual audio bytes)
    audio_input = b"mock_audio_data"
    user_id = "USER-123"
    
    print(f"📝 Processing voice query for user: {user_id}")
    print(f"🎤 Audio input: {len(audio_input)} bytes")
    print()
    
    try:
        results = await process_voice_query(audio_input, user_id)
        
        print("=" * 70)
        print("  RESULTS")
        print("=" * 70)
        print()
        
        if not results:
            print("❌ No recommendations found")
            return
        
        print(f"✅ Found {len(results)} recommendations:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. Item ID: {result.item_id}")
            print(f"   Score: {result.score:.3f}")
            print(f"   Reasoning: {result.reasoning}")
            print()
        
        # Also show as JSON
        print("=" * 70)
        print("  JSON Output")
        print("=" * 70)
        print()
        results_json = [r.dict() for r in results]
        print(json.dumps(results_json, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_voice_query())




