# FILENAME: main.py

import os
from crewai import Crew, Process
from langchain_openai import ChatOpenAI

# Import the agents and tasks from their respective files
from agents import sales_agent, loyalty_agent
from tasks import sales_task

# --- Set Up Your API Key ---
# Make sure you have OPENAI_API_KEY set in your environment variables
# For testing purposes, you can set it here (not recommended for production)
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Check if API key is available
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables.")
    print("   Please set your OpenAI API key to test the agents.")
    print("   You can set it by running: export OPENAI_API_KEY='your-key-here'")
    print("   Or uncomment and set the line in main.py")
    exit(1)


# Form the crew with the two agents
retail_crew = Crew(
    agents=[sales_agent, loyalty_agent],
    tasks=[sales_task],
    process=Process.sequential,
    verbose=2
)

# Kick off the crew's work
if __name__ == "__main__":
    print("==================================================")
    print("Retail Crew is starting the checkout process...")
    print("==================================================")

    result = retail_crew.kickoff()

    print("\n==================================================")
    print("Retail Crew has finished the checkout process.")
    print("================================S==================")
    print("\nFinal Customer-Facing Message:\n")
    print(result)