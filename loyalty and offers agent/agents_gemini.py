# FILENAME: agents.py (Gemini Version)

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from tools import pricing_tool

# Initialize the LLM with Gemini
# Make sure GOOGLE_API_KEY is set in environment
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",  # or "gemini-1.5-pro" for latest model
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)

# --- Worker Agent: Loyalty and Offers Agent [cite: 290] ---
loyalty_agent = Agent(
    role="Specialized Financial Assistant",
    goal=(
        "Calculate the final price for a customer's order by accurately "
        "applying all eligible loyalty points, promotions, and coupon codes."
    ),
    backstory=(
        "You are a precise, rule-based agent that handles all pricing calculations. "
        "You ONLY use your 'Pricing and Offers Calculation Tool' to get financial data. "
        "You do not talk to the customer directly, but provide a clean JSON "
        "summary of the transaction to the Sales Agent who requested it."
    ),
    # tools=[pricing_tool],  # Temporarily commented out to test basic functionality
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# --- Master Agent: Sales Agent [cite: 289] ---
sales_agent = Agent(
    role="Senior Conversational Sales Agent",
    goal=(
        "Guide the customer through their purchase and provide a seamless "
        "checkout experience. You are responsible for the final "
        "customer-facing communication."
    ),
    backstory=(
        "You are the primary point of contact for the customer. You are friendly, "
        "persuasive, and helpful. When it comes to complex calculations like "
        "pricing, you MUST delegate the task to the 'Specialized Financial Assistant' "
        "to ensure accuracy. You will then take the JSON data from that assistant "
        "and present it to the customer in a friendly, easy-to-understand way."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=True # Can delegate tasks to the loyalty_agent
)

