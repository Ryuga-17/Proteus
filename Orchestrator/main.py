"""
Main Orchestrator - Your Friendly Central Command Center 🎛️

This is where all the magic happens! Think of this file as the main control room
that coordinates all your retail agents. Whether it's checking inventory, processing
payments, or helping customers track their orders - everything flows through here.

When you run a request, the orchestrator figures out which specialist agent
needs to handle it, sends it their way, and brings back a helpful response.
It's like having a super-smart assistant who knows exactly who to talk to!
"""
import os
import sys

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    # Get project root (one level up from orchestrator folder)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed - continue without it
    pass

from crewai import Crew, Process

# Our star player - the orchestrator agent who knows how to route everything
from orchestrator_agent import Orchestrator

# Import all the pre-built example tasks we can run
from orchestrator_tasks import (
    task_inventory_management,
    task_order_fulfillment,
    task_payment_processing,
    task_customer_support,
    task_checkout_with_loyalty,
    task_return_exchange,
    create_custom_task
)


def run_orchestrator(task, task_name: str = "Orchestrator Task"):
    """
    Run a single task through our orchestrator - the friendly way! 😊
    
    This function takes any task and runs it through our orchestrator agent,
    which will figure out the best way to handle it. It's like sending a request
    to a smart assistant who knows all the right people to contact.
    
    Args:
        task: The task object that describes what needs to be done
        task_name: A friendly name to show in the output (so we know what's running)
    
    Returns:
        The result from the orchestrator - usually a helpful response or status update
    
    Example:
        >>> from orchestrator_tasks import task_inventory_management
        >>> result = run_orchestrator(task_inventory_management, "Check Stock")
        >>> print(result)  # See what happened!
    """
    # Let's make it pretty with a nice header
    print("=" * 60)
    print(f"  🎯 {task_name}")
    print("=" * 60)
    print()
    
    # Create our orchestrator crew - this is the team that will handle the task
    # We're using sequential processing so tasks happen one at a time
    # Memory is enabled so our agent remembers context from earlier in the conversation
    orchestrator_crew = Crew(
        agents=[Orchestrator],  # Our one agent who coordinates everything
        tasks=[task],                 # The task we want to complete
        process=Process.sequential,   # One step at a time (nice and organized)
        memory=True,                   # Remember what we talked about earlier
        verbose=True                      # Show us what's happening (good for debugging)
    )
    
    print(f"🚀 Starting orchestrator crew for: {task_name}")
    print("-" * 60)
    
    # Try to run the task and catch any issues that come up
    try:
        # Kick off the crew and let them do their thing!
        result = orchestrator_crew.kickoff()
        
        # Show a nice success message with the results
        print("\n" + "=" * 60)
        print(f"✅ {task_name} - COMPLETED")
        print("=" * 60)
        print("\n📋 Final Result:")
        print(result)
        print("\n" + "=" * 60)
        
        return result
        
    except Exception as e:
        # Oops, something went wrong. Let's tell the user in a friendly way
        print(f"\n❌ Oops! We ran into an issue with '{task_name}': {str(e)}")
        print("   Don't worry, check the error message above for clues on what happened.")
        raise


def run_example_scenarios():
    """
    Run through example scenarios to show off what our orchestrator can do! 🎬
    
    This function runs a collection of example scenarios that demonstrate
    different capabilities of the orchestrator. It's great for:
    - Testing that everything works
    - Understanding how the orchestrator handles different request types
    - Seeing the orchestrator coordinate multiple agents together
    
    You can easily customize which scenarios to run by editing the
    scenarios_to_run list below. Just uncomment the ones you want!
    """
    # Welcome message - let's be friendly!
    print("\n" + "=" * 60)
    print("  🤖 MASTER ORCHESTRATOR - Retail Agent Coordination")
    print("=" * 60)
    print("\nThis orchestrator coordinates all your retail agents:")
    print("  📦 Inventory Agent      → Stock checks, transfers, procurement")
    print("  🚚 Fulfillment Agent    → Shipping, in-store reservations")
    print("  💳 Payment Agent        → Transactions, payments, kiosk handoffs")
    print("  🎁 Loyalty Agent        → Points, offers, pricing calculations")
    print("  🎧 Support Agent        → Order tracking, returns, feedback")
    print("\n" + "=" * 60)
    print()
    
    # All available example scenarios - think of these as demo scripts
    # Each one shows off a different capability
    available_scenarios = [
        ("Inventory Management", task_inventory_management),
        ("Order Fulfillment", task_order_fulfillment),
        ("Payment Processing", task_payment_processing),
        ("Customer Support", task_customer_support),
        ("Checkout with Loyalty", task_checkout_with_loyalty),
        ("Return/Exchange", task_return_exchange),
    ]
    
    # Which scenarios do we actually want to run?
    # Just uncomment the ones you're interested in!
    # Pro tip: Start with one scenario at a time to see how it works
    scenarios_to_run = [
        available_scenarios[0],  # Inventory Management - great starting point!
        # available_scenarios[1],  # Order Fulfillment - see how orders flow
        # available_scenarios[2],  # Payment Processing - watch payments happen
        # available_scenarios[3],  # Customer Support - help customers track orders
        # available_scenarios[4],  # Checkout with Loyalty - full checkout flow
        # available_scenarios[5],  # Return/Exchange - handle returns gracefully
    ]
    
    # Track results so we can see what happened
    scenario_results = {}
    
    # Run each scenario and collect the results
    for scenario_name, scenario_task in scenarios_to_run:
        try:
            print(f"\n🔄 Running scenario: {scenario_name}...")
            result = run_orchestrator(scenario_task, scenario_name)
            scenario_results[scenario_name] = result
            print(f"✨ Successfully completed: {scenario_name}")
            
        except Exception as e:
            # Something went wrong with this scenario, but let's continue with others
            print(f"⚠️  Couldn't complete '{scenario_name}': {e}")
            scenario_results[scenario_name] = None
            print("   Moving on to the next scenario...")
        
        # Give some breathing room between scenarios
        print("\n\n")
    
    # Summary of what we ran
    print("=" * 60)
    print("📊 Scenario Summary:")
    for name, result in scenario_results.items():
        status = "✅ Success" if result else "❌ Failed"
        print(f"   {status} - {name}")
    print("=" * 60)
    
    return scenario_results


def handle_custom_request(customer_request: str, expected_output: str = None):
    """
    Handle any custom request - the easy way! 🎯
    
    This is your go-to function when you have a specific customer request
    that doesn't fit into the pre-built scenarios. Just describe what you
    need, and the orchestrator will figure out the best way to handle it!
    
    Args:
        customer_request: What the customer needs (describe it in plain English!)
                         Examples:
                         - "Check if SKU-123 is in stock"
                         - "Track order ORD-456 for customer C-789"
                         - "Process a return for damaged item from order ORD-123"
        
        expected_output: What format you'd like the response in (optional)
                        If you don't specify, we'll give you a helpful response
    
    Returns:
        The orchestrator's response to your request
    
    Example:
        >>> result = handle_custom_request(
        ...     "Check stock for red shirt size small at all stores"
        ... )
        >>> print(result)  # See what we found!
    """
    # Create a custom task from the description
    # This is flexible - you can ask for anything!
    custom_task = create_custom_task(customer_request, expected_output)
    
    # Run it through our orchestrator - easy peasy!
    return run_orchestrator(custom_task, "Custom Request")


if __name__ == "__main__":
    """
    Main entry point - this runs when you execute the file directly
    
    When you run: python main.py
    This is what gets executed!
    """
    
    # First, let's check if the user has set up their API key
    # Some agents need this to work properly (though some have mock LLMs)
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Hey there! 👋")
        print("   I noticed you don't have OPENAI_API_KEY set up yet.")
        print("   To get the full experience, you can set it by running:")
        print()
        print("   export OPENAI_API_KEY='your-key-here'")
        print()
        print("   Don't worry though - we'll continue anyway!")
        print("   (Some agents have mock LLMs that work without the key)")
        print()
    
    # Run our example scenarios - these are great for learning how it all works!
    # This will demonstrate various capabilities of the orchestrator
    run_example_scenarios()
    
    # ========================================================================
    # 🎨 CUSTOM REQUEST EXAMPLES (Uncomment to try them!)
    # ========================================================================
    # Want to try something specific? Just uncomment one of these:
    #
    # Example 1: Check inventory
    # handle_custom_request(
    #     "A customer wants to check stock for SKU ABC123 and if available, "
    #     "reserve it in store S-102"
    # )
    #
    # Example 2: Track an order
    # handle_custom_request(
    #     "Customer is asking where their order ORD-78901 is. "
    #     "Please track it and give them an update!"
    # )
    #
    # Example 3: Process a return
    # handle_custom_request(
    #     "A customer received a damaged item (SKU: TSHIRT-BLU-M) from order ORD56789. "
    #     "They want to exchange it for a new one if available, "
    #     "or get a refund if not in stock."
    # )

