"""
Tools for Recommendation Agent 2
Uses real Ollama and Qdrant services
"""
from langchain_community.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import asyncio
from voice_processor_v2 import process_voice_query_v2
from app import OllamaClient


class VoiceQueryToolSchemaV2(BaseModel):
    """Input schema for Voice Query Tool V2"""
    query_text: str = Field(..., description="Natural language product query (e.g., 'looking for a shirt for date')")
    user_id: str = Field(..., description="Unique identifier for the user")


class VoiceQueryToolV2(BaseTool):
    """
    Tool for processing voice-based product queries using real services
    Uses Ollama for embeddings and Qdrant for vector search
    """
    name: str = "Advanced Voice Query Recommendation Tool"
    description: str = (
        "Process a natural language product query using real vector embeddings and Qdrant database "
        "to find highly accurate, personalized recommendations. Takes query_text and user_id, "
        "returns a list of recommended products with scores and reasoning. "
        "Uses real product data and customer profiles for superior personalization."
    )
    args_schema: Type[BaseModel] = VoiceQueryToolSchemaV2
    
    def _run(self, query_text: str, user_id: str) -> str:
        """
        Synchronous wrapper for async voice query processing with real services
        """
        # Run async function in event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            results = loop.run_until_complete(
                process_voice_query_v2(query_text, user_id)
            )
        except Exception as e:
            return f"Error processing query: {str(e)}"
        
        # Format results as a readable string
        if not results:
            return "No recommendations found for your query."
        
        formatted_results = []
        formatted_results.append(f"Found {len(results)} personalized recommendations:\n")
        
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. Product ID: {result.get('product_id', 'N/A')}\n"
                f"   Title: {result.get('title', 'N/A')}\n"
                f"   Price: ${result.get('price', 0):.2f}\n"
                f"   Score: {result.get('score', 0):.3f}\n"
                f"   Reasoning: {result.get('reasoning', 'N/A')}\n"
            )
        
        return "\n".join(formatted_results)


# Instantiate the tool
voice_query_tool_v2 = VoiceQueryToolV2()




