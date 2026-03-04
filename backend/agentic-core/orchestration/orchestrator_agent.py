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
    # Get project root (one level up from Orchestrator folder)
    # __file__ is Orchestrator/orchestrator_agent.py
    # dirname(__file__) is Orchestrator/
    # dirname(dirname(__file__)) is project root (Sales Agent/)
    orchestrator_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(orchestrator_dir)
    env_path = os.path.join(project_root, '.env')
    
    # Try loading from multiple locations
    locations = [env_path, os.path.join(os.getcwd(), '.env'), '.env']
    for loc in locations:
        if os.path.exists(loc):
            load_dotenv(loc, override=True)
            break
    # Final fallback
    load_dotenv(override=True)
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
    route_to_support,
    route_to_recommendation,
    route_to_recommendation_v2
)

# Get API keys - try multiple sources
# Force reload .env one more time to ensure it's loaded
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except:
    pass

google_api_key = os.getenv("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

# Initialize llm variable
llm = None

# Use OpenAI as primary LLM (Google API key is invalid)
# Initialize LLM with OpenAI
if openai_api_key:
    try:
        llm = LLM(
            model="gpt-3.5-turbo",
            api_key=openai_api_key
        )
        # Verify it was created
        if llm is None:
            import sys
            print("ERROR: LLM object is None after creation!", file=sys.stderr)
    except Exception as e:
        # OpenAI initialization failed - log it
        import sys
        print(f"ERROR: OpenAI LLM initialization failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        llm = None
else:
    import sys
    print("ERROR: openai_api_key is None!", file=sys.stderr)

# Final check - ensure we have an LLM before creating Agent
if llm is None:
    # One final attempt with explicit key retrieval
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        final_openai_key = os.getenv("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if final_openai_key:
            llm = LLM(model="gpt-3.5-turbo", api_key=final_openai_key)
    except Exception as e:
        import sys
        print(f"Final OpenAI attempt failed: {e}", file=sys.stderr)
    
    if llm is None:
        raise ValueError(
            "Orchestrator requires an LLM. Please set OPENAI_API_KEY in .env file.\n"
            f"Current status: OpenAI key is {'SET' if openai_api_key else 'NOT SET'}"
        )

# Debug: Print llm status before Agent creation
import sys
print(f"DEBUG: About to create Agent. llm is {'SET' if llm is not None else 'None'}", file=sys.stderr)
if llm is None:
    print("ERROR: llm is None! Cannot create Agent!", file=sys.stderr)
    raise RuntimeError("llm is None - this should not happen!")

# Create our master orchestrator agent - this is the star of the show! ⭐
Orchestrator = Agent(
    role="Master Orchestrator and Smart Request Router",
    goal=(
        "Be the friendly and efficient central coordinator for all retail operations! "
        "When customers or business needs come in, you figure out the best way to help them. "
        "You analyze requests, decide which specialist agents should handle them, "
        "route requests to the right places, and bring everything together into "
        "clear, helpful responses. You're also great at coordinating complex workflows "
        "that need multiple agents working together.\n\n"
        "You must handle errors deterministically: detect error types from structured "
        "tool responses, decide retry vs rollback vs human handoff, and respond to "
        "customers with clear, non-technical messaging."
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
        "  🎧 Support Agent → route_to_support() → Order tracking, returns, feedback\n"
        "  🎯 Recommendation Agent → route_to_recommendation() → Voice search, product recommendations\n"
        "  🚀 Recommendation Agent 2 → route_to_recommendation_v2() → Advanced recommendations with real data\n\n"
        
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
        "for everyone involved!\n\n"
        "IMPORTANT ERROR HANDLING RULES:\n"
        "  - Every tool returns a JSON object with success/result/error.\n"
        "  - Never expose internal error details or stack traces to the user.\n"
        "  - If error.retryable is true, you may retry once; otherwise, hand off.\n"
        "  - If a payment succeeds but order confirmation fails, trigger reconciliation."
    ),
    tools=[
        analyze_intent,           # Figure out what the customer needs
        route_to_inventory,       # Connect with inventory specialists
        route_to_fulfillment,     # Connect with shipping/reservation team
        route_to_payment,         # Connect with payment processing
        route_to_loyalty,         # Connect with pricing/discounts team
        route_to_support,         # Connect with customer support
        route_to_recommendation,  # Connect with recommendation system
        route_to_recommendation_v2 # Connect with advanced recommendation system (production-ready)
    ],
    llm=llm,                      # LLM configuration (Gemini or OpenAI) - required
    verbose=True,                  # Show what you're doing (helps with debugging!)
    allow_delegation=False,        # You don't delegate to other CrewAI agents -
                                   # instead you route to specialized sub-crews
    max_iter=15                    # Allow enough iterations for complex multi-step workflows
)
