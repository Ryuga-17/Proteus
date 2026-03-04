"""
Recommendation Agent 2 - Production-Ready Voice Search
Uses real Ollama embeddings and Qdrant vector database
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from langchain_openai import ChatOpenAI

# Initialize the LLM
try:
    from dotenv import load_dotenv
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

openai_api_key = os.getenv("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

if openai_api_key:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
else:
    llm = None

from tools import voice_query_tool_v2

# Recommendation Agent 2 - Production Ready
recommendation_agent_2 = Agent(
    role="Advanced Product Recommendation Specialist",
    goal=(
        "Process voice-based and natural language product queries using real vector embeddings "
        "and Qdrant database to provide highly accurate, personalized product recommendations. "
        "Leverage real customer profiles and product data for superior personalization."
    ),
    backstory=(
        "You are an advanced AI agent powered by real vector embeddings and semantic search. "
        "You use Ollama for generating embeddings and Qdrant vector database for fast, accurate "
        "product retrieval. You have access to real product catalogs and customer profiles, "
        "allowing you to provide highly personalized recommendations based on actual purchase "
        "history, preferences, and behavioral patterns. You excel at understanding natural language "
        "queries and matching them to products using semantic similarity, then refining results "
        "with metadata filtering and personalized ranking."
    ),
    tools=[voice_query_tool_v2],
    llm=llm,
    verbose=True,
    allow_delegation=False
)




