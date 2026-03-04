"""
Recommendation Agent - Voice Search and Product Recommendations
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
    # Fallback - will need to be set
    llm = None

from tools import voice_query_tool

# Recommendation Agent
recommendation_agent = Agent(
    role="Product Recommendation Specialist",
    goal=(
        "Process voice-based product queries and provide personalized product recommendations. "
        "Understand natural language queries, extract product preferences, and return "
        "structured, ranked recommendations based on user context and query intent."
    ),
    backstory=(
        "You are an expert at understanding what customers really want when they search for products. "
        "You excel at interpreting natural language queries like 'looking for a shirt for date' and "
        "extracting the underlying intent - product type, occasion, style preferences. "
        "You use advanced AI to match products to user needs, considering their past purchases, "
        "preferences, and the specific context of their query. You provide clear, personalized "
        "recommendations with explanations of why each product was suggested."
    ),
    tools=[voice_query_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)




