"""
Payment Agent Main Script - Processing Payments Like a Pro! 💳

This script demonstrates how the Payment Agent handles various payment scenarios:
1. Payment failures - Handling declined cards gracefully
2. Kiosk-to-mobile handoffs - Moving payment from in-store kiosks to mobile devices
3. Loyalty point payments - Processing payments using customer loyalty points

The payment crew uses a hierarchical structure where the Sales Agent orchestrates
the conversation, while Payment and Loyalty agents handle the technical work.
"""
from crewai import Crew, Process

# Import our payment crew members
from agents import sales_agent, payment_agent, loyalty_agent

# Import the example payment scenarios
from tasks import task_fail_scenario, task_kiosk_scenario, task_points_scenario

# Welcome message
print("=" * 60)
print("💳 PAYMENT AGENT CREW - Demo Script")
print("=" * 60)
print("This demonstrates the payment processing workflow with multiple agents")
print("working together to handle various payment scenarios.")
print("=" * 60)
print()

# ============================================================================
# CONFIGURE WHICH SCENARIOS TO RUN
# ============================================================================
# You can easily customize which scenarios to test by commenting/uncommenting
# Just uncomment the ones you want to see in action!

tasks_to_run = [
    task_fail_scenario,      # See how we handle payment failures gracefully
    task_kiosk_scenario     # See how kiosk-to-mobile handoff works
    # task_points_scenario   # See how loyalty point payments work
]

# ============================================================================
# ASSEMBLE THE PAYMENT CREW
# ============================================================================
# We use hierarchical processing - the Sales Agent manages the conversation
# and delegates technical work (payments, loyalty) to specialist agents
crew = Crew(
    agents=[
        sales_agent,     # The conversation coordinator - talks to customers
        payment_agent,   # The payment processor - handles transactions
        loyalty_agent    # The loyalty manager - handles points and rewards
    ],
    tasks=tasks_to_run,
    process=Process.hierarchical,  # Sales agent coordinates the others
    manager_llm=None,               # Use the default LLM for the manager
    verbose=2                       # Show what's happening (great for learning!)
)

# ============================================================================
# RUN THE CREW
# ============================================================================
if __name__ == "__main__":
    print("\n🚀 Starting the Payment Crew...")
    print("-" * 60)
    print()
    
    # Run all the configured scenarios
    result = crew.kickoff()
    
    # Show the final results
    print("\n" + "=" * 60)
    print("✅ PAYMENT CREW EXECUTION COMPLETE!")
    print("=" * 60)
    print("\n📋 Final Result:")
    print(result)
    print("\n💡 Check the output above to see how each payment scenario was handled!")