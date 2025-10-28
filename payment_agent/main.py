# main.py
from crewai import Crew, Process

# Import the agents and tasks
from agents import sales_agent, payment_agent, loyalty_agent
from tasks import task_fail_scenario, task_kiosk_scenario, task_points_scenario

print("--- Payment Agent CrewAI Setup ---")
print("This script simulates the Retail Challenge (Challenge V) agent orchestration.")

# --- Define the tasks to run ---
# You can easily swap which tasks to run
tasks_to_run = [
    task_fail_scenario, 
    task_kiosk_scenario
    # task_points_scenario 
]

# --- Assemble the Crew ---
crew = Crew(
    agents=[sales_agent, payment_agent, loyalty_agent],
    tasks=tasks_to_run,
    process=Process.hierarchical,
    manager_llm=None, # Use the default LLM
    verbose=2
)

# --- Run the Crew ---
if __name__ == "__main__":
    print("\n--- KICKING OFF CREW ---")
    result = crew.kickoff()
    
    print("\n\n--- CREW EXECUTION FINISHED ---")
    print("\nFinal Result:")
    print(result)