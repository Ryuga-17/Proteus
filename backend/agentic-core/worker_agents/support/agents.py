# agents.py
from crewai import Agent
from crewai import LLM
import sys
import os

# Add Orchestrator to path for inter-agent communication
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, 'Orchestrator'))

from tools import (
    OrderManagementTool,
    CarrierAPITool,
    InventoryTool,
    ReturnsManagementTool,
    PaymentTool,
    CustomerFeedbackTool
)

# Import inter-agent communication tools
try:
    from inter_agent_communication import (
        request_inventory_help,
        request_fulfillment_help,
        request_payment_help,
        request_loyalty_help,
        request_agent_help
    )
    INTER_AGENT_COMMS_AVAILABLE = True
except ImportError:
    # If orchestrator not available, continue without inter-agent comms
    INTER_AGENT_COMMS_AVAILABLE = False
    request_inventory_help = None
    request_fulfillment_help = None
    request_payment_help = None
    request_loyalty_help = None
    request_agent_help = None

# Instantiate Tools
order_tool = OrderManagementTool()
carrier_tool = CarrierAPITool()
inventory_tool = InventoryTool()
returns_tool = ReturnsManagementTool()
payment_tool = PaymentTool()
feedback_tool = CustomerFeedbackTool()

# Build tools list - include inter-agent communication if available
support_tools = [
    order_tool,
    carrier_tool,
    inventory_tool,
    returns_tool,
    payment_tool,
    feedback_tool
]

# Add inter-agent communication tools if available
if INTER_AGENT_COMMS_AVAILABLE:
    support_tools.extend([
        request_inventory_help,   # Can request inventory checks for exchanges
        request_fulfillment_help,  # Can request fulfillment status
        request_payment_help,     # Can request payment/refund help
        request_loyalty_help,      # Can get pricing information
        request_agent_help        # Generic interface for any agent
    ])

# Define the LLM
# Use environment variable for API key (recommended)
# Fallback to hardcoded value only if env var not set (for development)
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")  # Use env var, fallback for dev
)

# Define the Agent
post_purchase_agent = Agent(
    role="Empathetic Customer Support Specialist",
    goal=(
        "Resolve post-purchase issues (tracking, returns, exchanges, feedback) "
        "efficiently, ensure the customer feels heard and valued, and make the "
        "support process as easy as possible. You can request help from other agents "
        "through the Orchestrator when needed."
    ),
    backstory=(
        "You are a seasoned support professional at a top retail brand, an expert "
        "in the company's policies, and skilled at de-escalating frustrated customers. "
        "You patiently listen to a customer's problem, apologize sincerely, and then "
        "use your available tools to find a complete solution on the first contact. "
        "You are not just a problem-solver; you are a brand ambassador.\n\n"
        
        "**Inter-Agent Communication:** When you need information from other agents "
        "(like checking inventory for an exchange or verifying fulfillment status), "
        "you can use the inter-agent communication tools which route requests through "
        "the Orchestrator to get help from specialist agents:\n"
        "  - Use request_inventory_help() to check stock for exchanges\n"
        "  - Use request_fulfillment_help() to get fulfillment/shipping status\n"
        "  - Use request_payment_help() to process refunds\n"
        "  - Use request_loyalty_help() to get pricing information\n"
        "  - All communication flows through Orchestrator - centralized and managed"
    ),
    tools=support_tools,
    llm=llm,
    verbose=True,
    allow_delegation=False  # Doesn't delegate within crew, but can request help from other agents
)
