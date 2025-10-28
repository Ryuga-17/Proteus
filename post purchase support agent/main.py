# main.py
from crewai import Crew, Process
from agents import post_purchase_agent
from tasks import task_track_order, task_damaged_item, task_get_feedback

def run_task(task, task_name):
    """Helper function to create and run a crew for a single task."""
    print("##################################################")
    print(f"##           Running Task: {task_name}     ##")
    print("##################################################\n")

    crew = Crew(
        agents=[post_purchase_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=2
    )
    
    result = crew.kickoff()
    print(f"\n--- {task_name} Final Result ---")
    print(result)
    print("\n\n")

if __name__ == "__main__":
    # Run each task separately to see the results
    run_task(task_track_order, "Order Tracking")
    run_task(task_damaged_item, "Damaged Item Exchange")
    run_task(task_get_feedback, "Solicit Feedback")