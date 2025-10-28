# agents.py
from crewai import Agent
from crewai import LLM
from tools import (
    OrderManagementTool,
    CarrierAPITool,
    InventoryTool,
    ReturnsManagementTool,
    PaymentTool,
    CustomerFeedbackTool
)

# Instantiate Tools
order_tool = OrderManagementTool()
carrier_tool = CarrierAPITool()
inventory_tool = InventoryTool()
returns_tool = ReturnsManagementTool()
payment_tool = PaymentTool()
feedback_tool = CustomerFeedbackTool()

# Define the LLM
llm = LLM(
    model="gpt-3.5-turbo",
    api_key="your-openai-api-key-here"  # Replace with actual API key
)

# Define the Agent
post_purchase_agent = Agent(
    role="Empathetic Customer Support Specialist",
    goal=(
        "Resolve post-purchase issues (tracking, returns, exchanges, feedback) "
        "efficiently, ensure the customer feels heard and valued, and make the "
        "support process as easy as possible."
    ),
    backstory=(
        "You are a seasoned support professional at a top retail brand, an expert "
        "in the company's policies, and skilled at de-escalating frustrated customers. "
        "You patiently listen to a customer's problem, apologize sincerely, and then "
        "use your available tools to find a complete solution on the first contact. "
        "You are not just a problem-solver; you are a brand ambassador."
    ),
    tools=[
        order_tool,
        carrier_tool,
        inventory_tool,
        returns_tool,
        payment_tool,
        feedback_tool
    ],
    llm=llm,
    verbose=True,
    allow_delegation=False
)