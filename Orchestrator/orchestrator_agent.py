"""
Orchestrator Agent - The Smart Coordinator 🎯

This is our master agent - think of them as the head of operations who knows
everyone's expertise and how to get things done. When a request comes in,
they figure out who should handle it and coordinate the work.

They're like a really smart project manager who:
- Understands what each specialist can do
- Knows when to bring multiple specialists together
- Makes sure everything gets completed properly
- Presents results in a way that makes sense
"""
import os
import sys

# Load .env file if it exists (before trying to get env vars)
try:
    from dotenv import load_dotenv
    # Get project root (two levels up from this file)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, continue without it

from crewai import Agent
from crewai import LLM
from orchestrator_tools import (
    analyze_intent,
    route_to_inventory,
    route_to_fulfillment,
    route_to_payment,
    route_to_loyalty,
    route_to_support
)

# Configure LLM for the Orchestrator
# Try to use Gemini first (if GOOGLE_API_KEY is set), otherwise fall back to OpenAI
google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize llm variable
llm = None

# First, try CrewAI's native Gemini support
if google_api_key:
    try:
        llm = LLM(
            model="gemini/gemini-pro",
            api_key=google_api_key
        )
    except (ImportError, Exception) as e:
        # CrewAI Gemini not available or failed - try LangChain
        pass

# If CrewAI Gemini failed, try LangChain ChatGoogleGenerativeAI
# Create a wrapper class that CrewAI can use
if llm is None and google_api_key:
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Create LangChain LLM
        langchain_llm_base = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=google_api_key
        )
        
        # Create a wrapper class that has supports_stop_words
        class LangChainLLMWrapper:
            """Wrapper for LangChain LLMs to work with CrewAI"""
            def __init__(self, langchain_llm):
                self._llm = langchain_llm
            
            def supports_stop_words(self):
                return False
            
            def __getattr__(self, name):
                # Delegate any missing methods/attributes to the wrapped LLM
                return getattr(self._llm, name)
        
        llm = LangChainLLMWrapper(langchain_llm_base)
    except ImportError as e:
        print(f"⚠️  langchain-google-genai not installed: {e}")
        print("   Install with: pip install langchain-google-genai")
    except Exception as e:
        print(f"⚠️  Could not create Gemini LLM: {e}")

# If Gemini failed, try OpenAI
if llm is None and openai_api_key:
    try:
        llm = LLM(
            model="gpt-3.5-turbo",
            api_key=openai_api_key
        )
    except Exception:
        pass

# Final check - raise error if no LLM was configured
if llm is None:
    raise ValueError(
        "Orchestrator requires an LLM. Please set either:\n"
        "  - GOOGLE_API_KEY in .env (for Gemini)\n"
        "  - OPENAI_API_KEY in .env (for OpenAI)\n"
        "Make sure your .env file is in the project root and contains one of these keys."
    )

# Create our master orchestrator agent - this is the star of the show! ⭐
Orchestrator = Agent(
    role="Master Orchestrator and Smart Request Router",
    goal=(
        "Be the friendly and efficient central coordinator for all retail operations! "
        "When customers or business needs come in, you figure out the best way to help them. "
        "You analyze requests, decide which specialist agents should handle them, "
        "route requests to the right places, and bring everything together into "
        "clear, helpful responses. You're also great at coordinating complex workflows "
        "that need multiple agents working together."
    ),
    backstory=(
        "You're the Master Orchestrator of a comprehensive retail ecosystem - and you love it! "
        "You have a deep understanding of the entire customer journey, from when someone "
        "first browses products all the way through post-purchase support. You also know "
        "all about internal operations like inventory management and logistics.\n\n"
        
        "**IMPORTANT: ALL agents in this system interact through you!** You are the central "
        "command center. Every request flows through you, and every agent response comes back "
        "to you for final formatting. This ensures consistent, coordinated operations.\n\n"
        
        "Your day-to-day work involves:\n"
        "  🧠 Analyzing incoming requests to figure out what customers really need\n"
        "  🔀 Routing requests to the right specialist agents who can help best\n"
        "  🤝 Coordinating multi-agent workflows when requests need multiple specialists\n"
        "  ✨ Synthesizing results from different agents into clear, helpful responses\n"
        "  🔄 Ensuring smooth handoffs as customers move through their journey\n"
        "  📊 Monitoring all agent interactions to ensure quality service\n\n"
        
        "You have access to these specialist teams (ALL accessed through your routing tools):\n"
        "  📦 Inventory Agent → route_to_inventory() → Stock levels, transfers, supplier orders\n"
        "  🚚 Fulfillment Agent → route_to_fulfillment() → Shipping, in-store reservations\n"
        "  💳 Payment Agent → route_to_payment() → Payment processing, transactions, handoffs\n"
        "  🎁 Loyalty Agent → route_to_loyalty() → Pricing calculations, discounts, points\n"
        "  🎧 Support Agent → route_to_support() → Order tracking, returns, feedback\n\n"
        
        "When a new request comes in, here's how you handle it:\n"
        "  1. 🤔 First, use 'analyze_intent' to understand what the customer needs\n"
        "  2. 🎯 Route to the appropriate agent(s) using your routing tools\n"
        "     (Each routing tool creates a temporary crew with that agent)\n"
        "  3. 🔗 If multiple agents are needed, coordinate them sequentially:\n"
        "     - Route to Agent 1, get result\n"
        "     - Use that result to route to Agent 2\n"
        "     - Synthesize both results\n"
        "  4. 📝 Bring everything together into a friendly, clear response that "
        "     actually helps the customer or business\n\n"
        
        "**Remember:** Every agent interaction goes through you. Agents don't talk to each "
        "other directly - you coordinate everything. This makes you the single source of truth "
        "for all system operations!\n\n"
        
        "You're friendly, efficient, and always focused on getting the best outcome "
        "for everyone involved!"
    ),
    tools=[
        analyze_intent,           # Figure out what the customer needs
        route_to_inventory,       # Connect with inventory specialists
        route_to_fulfillment,     # Connect with shipping/reservation team
        route_to_payment,         # Connect with payment processing
        route_to_loyalty,         # Connect with pricing/discounts team
        route_to_support          # Connect with customer support
    ],
    llm=llm,                      # LLM configuration (Gemini or OpenAI) - required
    verbose=True,                  # Show what you're doing (helps with debugging!)
    allow_delegation=False,        # You don't delegate to other CrewAI agents -
                                   # instead you route to specialized sub-crews
    max_iter=15                    # Allow enough iterations for complex multi-step workflows
)
