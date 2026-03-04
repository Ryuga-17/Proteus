"""
Tools for Recommendation Agent
"""
from langchain_community.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
import asyncio
from voice_processor import process_voice_query, stt_service
from models import RecommendationResult


class VoiceQueryToolSchema(BaseModel):
    """Input schema for Voice Query Tool"""
    query_text: str = Field(..., description="Natural language product query (e.g., 'looking for a shirt for date')")
    user_id: str = Field(..., description="Unique identifier for the user")


class VoiceQueryTool(BaseTool):
    """
    Tool for processing voice-based product queries and returning recommendations
    """
    name: str = "Voice Query Recommendation Tool"
    description: str = (
        "Process a natural language product query to find personalized recommendations. "
        "Takes query_text (natural language like 'looking for a shirt for date') and user_id, "
        "returns a list of recommended products with scores and reasoning. "
        "Use this when a user asks for product recommendations using natural language."
    )
    args_schema: Type[BaseModel] = VoiceQueryToolSchema
    
    def _run(self, query_text: str, user_id: str) -> str:
        """
        Synchronous wrapper for async voice query processing
        """
        # Set override text for STT (since we're passing text directly)
        stt_service.set_override_text(query_text)
        
        # Run async function in event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Use mock audio bytes since we're passing text directly
        mock_audio = b"mock_audio_data"
        
        try:
            results = loop.run_until_complete(
                process_voice_query(mock_audio, user_id)
            )
        finally:
            # Clear override after processing
            stt_service.clear_override()
        
        # Format results as a readable string
        if not results:
            return "No recommendations found for your query."
        
        formatted_results = []
        formatted_results.append(f"Found {len(results)} personalized recommendations:\n")
        
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. Item ID: {result.item_id}\n"
                f"   Relevance Score: {result.score:.3f}\n"
                f"   Why Recommended: {result.reasoning}\n"
            )
        
        return "\n".join(formatted_results)


# Instantiate the tool
voice_query_tool = VoiceQueryTool()

