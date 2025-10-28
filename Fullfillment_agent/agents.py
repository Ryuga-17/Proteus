# agents.py
from crewai import Agent
from crewai.llm import LLM
from tools import book_shipment, reserve_in_store, notify_staff

# Collate all tools for the agent
fulfillment_tools = [book_shipment, reserve_in_store, notify_staff]

# Create a simple LLM for testing
class MockLLM:
    def __init__(self):
        self.model = "mock"
    
    def supports_stop_words(self):
        return False
    
    def call(self, messages, **kwargs):
        # Mock response for testing
        return "I will process this fulfillment request using the appropriate tools."

# Define the Fulfillment Agent
fulfillment_agent = Agent(
    role="Backend Logistics Coordinator",
    goal="Efficiently process paid orders for either shipment or in-store reservation by coordinating with logistics and store APIs.",
    backstory=(
        "You are a precise and autonomous backend system. You do not interact with customers. "
        "You receive order data, execute fulfillment tasks using your tools, notify the correct staff, "
        "and return a final JSON status report. You must validate the fulfillment type "
        "('ship-to-home' or 'reserve-in-store') and use the correct tool for the job. "
        "You MUST respond with only the final JSON status report."
    ),
    tools=fulfillment_tools,
    verbose=True,
    allow_delegation=False,
    llm=MockLLM()
)