# main.py
from crewai import Crew, Process
from agents import fulfillment_agent
from tasks import task_ship_to_home, task_reserve_in_store

# --- SCENARIO 1: SHIP-TO-HOME ---
print("=============================================================")
print("--- KICKING OFF CREW (SCENARIO 1: SHIP-TO-HOME) ---")
print("=============================================================")

ship_to_home_crew = Crew(
    agents=[fulfillment_agent],
    tasks=[task_ship_to_home],
    process=Process.sequential,
    verbose=2
)

ship_result = ship_to_home_crew.kickoff()

print("\n--- SCENARIO 1 COMPLETE ---")
print("Final Result (Ship-to-Home):")
print(ship_result)


# --- SCENARIO 2: RESERVE IN-STORE ---
print("\n\n=============================================================")
print("--- KICKING OFF CREW (SCENARIO 2: RESERVE IN-STORE) ---")
print("=============================================================")

reserve_crew = Crew(
    agents=[fulfillment_agent],
    tasks=[task_reserve_in_store],
    process=Process.sequential,
    verbose=2
)

reserve_result = reserve_crew.kickoff()

print("\n--- SCENARIO 2 COMPLETE ---")
print("Final Result (Reserve In-Store):")
print(reserve_result)