from crewai import Crew, Process, Task
from inventory_agents import (
    inventory_orchestrator_agent, 
    logistics_agent, 
    procurement_agent
)
from inventory_tools import db  


analysis_task = Task(
    description=(
        "Run the nightly inventory optimization plan. "
        "1. Check sales velocity for 'sku_123' (in-demand) and 'sku_456'. "
        "2. Check current stock levels for both SKUs at all locations. "
        "3. Identify replenishment needs: 'sku_123' is 'in-demand' (velocity > 10), "
        "   so we need to order more. Order 100 units. "
        "4. Identify transfer needs: 'store_main_street' is low on 'sku_123' (stock < 10) "
        "   and 'godown_central' has plenty. Plan a transfer of 50 units."
    ),
    expected_output=(
        "A JSON object with two keys: "
        "'replenishments': A list of {sku, quantity} to order. "
        "'transfers': A list of {from, to, sku, quantity} to move."
    ),
    agent=inventory_orchestrator_agent
)


procurement_task = Task(
    description="Process all replenishment orders identified in the analysis.",
    expected_output="A confirmation list of all purchase orders placed.",
    agent=procurement_agent,
    context=[analysis_task]  # This task depends on the output of the first
)


logistics_task = Task(
    description="Process all inter-store transfers identified in the analysis.",
    expected_output="A confirmation list of all transfers completed or rejected.",
    agent=logistics_agent,
    context=[analysis_task]  # This task also depends on the output of the first
)


def run_crew():
    print("--- Initial Database State ---")
    print(db.inventory)
    print("---------------------------------")
    
    # Define the crew with all agents
    inventory_crew = Crew(
        agents=[
            inventory_orchestrator_agent, 
            logistics_agent, 
            procurement_agent
        ],
        tasks=[
            analysis_task, 
            procurement_task, 
            logistics_task
        ],
        process=Process.sequential,  # Tasks run one after another
        memory=True,  # this will enable "Memory" for the crew
        verbose=2
    )
    

    print("🚀 Kicking off the Inventory Crew...")
    result = inventory_crew.kickoff()
    
    print("\n✅ Crew run finished!")
    print("\n--- Final Result ---")
    print(result)
    
    print("\n--- Final Database State ---")
    print(db.inventory)
    print("---------------------------------")

if __name__ == "__main__":
    run_crew()