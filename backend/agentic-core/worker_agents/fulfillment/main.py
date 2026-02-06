"""
Fulfillment Agent Main Script - Getting Orders to Customers! 🚚

This script demonstrates how the Fulfillment Agent handles two main scenarios:
1. Ship-to-Home: Shipping products directly to customer addresses
2. Reserve In-Store: Holding items at a store for customer pickup

The fulfillment agent coordinates with warehouses and stores to make sure
customers get their orders smoothly, whether it's delivered to their door
or waiting for them at a store location.
"""
from crewai import Crew, Process
from agents import fulfillment_agent
from tasks import task_ship_to_home, task_reserve_in_store

# ============================================================================
# SCENARIO 1: SHIP-TO-HOME - Delivering orders to customer addresses
# ============================================================================
print("=" * 60)
print("🚚 SCENARIO 1: SHIP-TO-HOME")
print("=" * 60)
print("Processing an order that needs to be shipped directly to the customer...")
print()

# Set up the fulfillment crew for shipping
ship_to_home_crew = Crew(
    agents=[fulfillment_agent],      # Our fulfillment specialist
    tasks=[task_ship_to_home],        # The shipping task
    process=Process.sequential,       # One step at a time
    verbose=2                         # Show what's happening
)

# Let's ship that order! 📦
print("🚀 Starting fulfillment process...")
ship_result = ship_to_home_crew.kickoff()

# Show the results
print("\n" + "=" * 60)
print("✅ SHIP-TO-HOME COMPLETE!")
print("=" * 60)
print("\n📋 Final Result:")
print(ship_result)
print()


# ============================================================================
# SCENARIO 2: RESERVE IN-STORE - Holding items for store pickup
# ============================================================================
print("\n\n" + "=" * 60)
print("🏪 SCENARIO 2: RESERVE IN-STORE")
print("=" * 60)
print("Processing an order that will be held at a store for customer pickup...")
print()

# Set up the fulfillment crew for in-store reservation
reserve_crew = Crew(
    agents=[fulfillment_agent],       # Same agent, different task
    tasks=[task_reserve_in_store],    # The reservation task
    process=Process.sequential,       # Sequential processing
    verbose=2                         # Show the workflow
)

# Reserve those items! 🏪
print("🚀 Starting reservation process...")
reserve_result = reserve_crew.kickoff()

# Show the results
print("\n" + "=" * 60)
print("✅ RESERVE IN-STORE COMPLETE!")
print("=" * 60)
print("\n📋 Final Result:")
print(reserve_result)
print("\n💡 The customer can now pick up their order using the pickup code!")