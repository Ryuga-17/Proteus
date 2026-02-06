from crewai import Agent
import sys
import os

# Add Orchestrator to path for inter-agent communication
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, 'Orchestrator'))

from inventory_tools import InventoryTools

# Import inter-agent communication tools
try:
    from inter_agent_communication import (
        request_fulfillment_help,
        request_payment_help,
        request_loyalty_help,
        request_agent_help
    )
    INTER_AGENT_COMMS_AVAILABLE = True
except ImportError:
    # If orchestrator not available, continue without inter-agent comms
    INTER_AGENT_COMMS_AVAILABLE = False
    request_fulfillment_help = None
    request_payment_help = None
    request_loyalty_help = None
    request_agent_help = None

# Build tools list for inventory orchestrator
inventory_orchestrator_tools = [
    InventoryTools.check_stock_tool,
    InventoryTools.get_sales_velocity_tool
]

# Add inter-agent communication tools if available
if INTER_AGENT_COMMS_AVAILABLE:
    inventory_orchestrator_tools.extend([
        request_fulfillment_help,  # Can check fulfillment status
        request_payment_help,      # Can verify payment before ordering
        request_loyalty_help,      # Can get pricing info
        request_agent_help         # Generic interface for any agent
    ])

# ----------------------------------------------------------------------------
# AGENT 1: The Orchestrator / Analyst
# ----------------------------------------------------------------------------
inventory_orchestrator_agent = Agent(
    role="Inventory & Logistics Orchestrator",
    goal="Analyze stock levels, sales trends, and locations to ensure optimal "
         "inventory distribution and identify replenishment needs.",
    backstory=(
        "You are the digital 'Supply Chain Head.' Your job is not just to "
        "report numbers, but to think one step ahead. You analyze data "
        "to find problems (like low stock at a key store) and opportunities "
        "(like high sales velocity for a new product) and then create a "
        "clear plan for other agents to execute.\n\n"
        
        "**Inter-Agent Communication:** When you need information from other "
        "specialists, you can request help through the Orchestrator:\n"
        "  - Use request_fulfillment_help() to check fulfillment status\n"
        "  - Use request_payment_help() to verify payment before ordering\n"
        "  - Use request_loyalty_help() to get pricing information\n"
        "  - All communication flows through Orchestrator - centralized and managed"
    ),
    tools=inventory_orchestrator_tools,
    verbose=True,
    allow_delegation=True  # Can delegate tasks to other agents in crew AND request help from other agent crews
)

# ----------------------------------------------------------------------------
# AGENT 2: The Logistics Executor
# ----------------------------------------------------------------------------
logistics_agent = Agent(
    role="Logistics Coordinator",
    goal="Execute physical stock transfers between different godowns and stores "
         "safely and efficiently.",
    backstory=(
        "You are the hands-on operations manager. You follow instructions "
        "from the Orchestrator to move stock. Your primary concern is "
        "executing these transfers correctly and respecting all safety "
        "and cost guardrails. You use the 'execute_safe_transfer_tool' "
        "for all movements."
    ),
    tools=[InventoryTools.execute_safe_transfer_tool],
    verbose=True
)

# ----------------------------------------------------------------------------
# AGENT 3: The Procurement Executor
# ----------------------------------------------------------------------------
procurement_agent = Agent(
    role="Procurement Specialist",
    goal="Place replenishment orders with external suppliers.",
    backstory=(
        "You are the purchasing specialist. When the Orchestrator "
        "identifies a need to re-stock, you are given the SKU and "
        "quantity, and you execute the purchase order."
    ),
    tools=[InventoryTools.order_from_supplier_tool],
    verbose=True
)