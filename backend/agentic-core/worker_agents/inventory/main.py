"""
Inventory Agent Main Script - Managing Stock Like a Pro! 📦

This script demonstrates how the Inventory Agent handles stock management,
transfers between locations, and ordering from suppliers. It runs through
a complete inventory optimization workflow.
"""
from crewai import Crew, Process, Task
from inventory_agents import (
    inventory_orchestrator_agent,  # The planner who analyzes and decides what to do
    logistics_agent,               # The mover who handles transfers
    procurement_agent              # The buyer who places orders with suppliers
)
from inventory_tools import db  

# ============================================================================
# TASK DEFINITIONS - These describe what we want the agents to do
# ============================================================================

# Task 1: Analyze inventory and figure out what needs to happen
analysis_task = Task(
    description=(
        "Run our nightly inventory optimization check! "
        "\n\n"
        "Here's what I need you to do:\n"
        "  1. Check how fast 'sku_123' and 'sku_456' are selling (sales velocity)\n"
        "     Note: 'sku_123' is currently in high demand\n"
        "  2. Check current stock levels for both SKUs at all our locations\n"
        "  3. Figure out what we need to replenish:\n"
        "     - If 'sku_123' is selling fast (velocity > 10), order 100 more units\n"
        "  4. Figure out what transfers we need:\n"
        "     - If 'store_main_street' is running low on 'sku_123' (less than 10 units)\n"
        "       and 'godown_central' has plenty, plan to transfer 50 units over"
    ),
    expected_output=(
        "A clear plan in JSON format with two main sections:\n"
        "  📝 'replenishments': List of what we need to order from suppliers "
        "(each item should have the SKU and quantity)\n"
        "  🔄 'transfers': List of what needs to move between locations "
        "(each transfer should show: from where, to where, which SKU, how many)\n"
        "\n"
        "Make it structured so the next agents can easily execute the plan!"
    ),
    agent=inventory_orchestrator_agent  # The orchestrator plans everything
)


# Task 2: Place orders with suppliers (depends on analysis being done first)
procurement_task = Task(
    description=(
        "Great! The analysis is done and we know what we need to order. "
        "Now please process all the replenishment orders that were identified. "
        "Place purchase orders with our suppliers for all the items that need restocking."
    ),
    expected_output=(
        "A confirmation list showing all the purchase orders you placed. "
        "For each order, include: which SKU, how many units, supplier details, "
        "and order confirmation numbers if available."
    ),
    agent=procurement_agent,
    context=[analysis_task]  # This task waits for the analysis to finish first
)


# Task 3: Move stock between locations (also depends on analysis)
logistics_task = Task(
    description=(
        "The analysis has identified some transfers we need to make. "
        "Please process all the inter-store and inter-godown transfers that were planned. "
        "Move the items from where we have plenty to where we're running low."
    ),
    expected_output=(
        "A confirmation list showing all the transfers you completed. "
        "For each transfer, include: what was moved, from where, to where, "
        "and whether it was successful. If any transfers were rejected (maybe "
        "due to safety rules or cost limits), explain why."
    ),
    agent=logistics_agent,
    context=[analysis_task]  # This also waits for the analysis to finish
)


def run_crew():
    """
    Run the inventory crew through their workflow! 🚀
    
    This function:
    1. Shows what's in inventory before we start
    2. Runs the agents through their tasks (analysis → procurement → logistics)
    3. Shows the results
    4. Shows what's in inventory after (so you can see what changed!)
    """
    # Show what we're starting with
    print("=" * 60)
    print("📦 INITIAL INVENTORY STATE")
    print("=" * 60)
    print(db.inventory)
    print("=" * 60)
    print()
    
    # Assemble our inventory management crew
    # These agents work together: the orchestrator plans, procurement buys, logistics moves
    inventory_crew = Crew(
        agents=[
            inventory_orchestrator_agent,  # The brain - plans what needs to happen
            logistics_agent,               # The mover - executes transfers
            procurement_agent              # The buyer - places orders
        ],
        tasks=[
            analysis_task,      # First: analyze and plan
            procurement_task,   # Second: place orders (waits for analysis)
            logistics_task      # Third: move stock (also waits for analysis)
        ],
        process=Process.sequential,  # Tasks happen one at a time, in order
        memory=True,                  # Remember what we did earlier in the conversation
        verbose=2                    # Show us what's happening (helpful for understanding!)
    )
    
    # Let's go! 🚀
    print("🚀 Starting the Inventory Management Crew...")
    print("   They'll analyze, order, and transfer as needed!")
    print("-" * 60)
    print()
    
    # Run the crew and see what happens!
    result = inventory_crew.kickoff()
    
    # Show the results
    print("\n" + "=" * 60)
    print("✅ CREW WORK COMPLETE!")
    print("=" * 60)
    print("\n📋 Final Result:")
    print(result)
    print()
    
    # Show what changed in inventory
    print("=" * 60)
    print("📦 FINAL INVENTORY STATE")
    print("=" * 60)
    print(db.inventory)
    print("=" * 60)
    print("\n💡 Compare this with the initial state to see what changed!")


if __name__ == "__main__":
    """
    Main entry point - run this file directly to see the inventory crew in action!
    
    Just run: python main.py
    """
    run_crew()