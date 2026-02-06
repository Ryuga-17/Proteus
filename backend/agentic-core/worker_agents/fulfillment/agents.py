"""
Fulfillment Agent - The Logistics Expert 🚚

This agent handles getting orders to customers - whether that means shipping
items to their home address or reserving them at a store for pickup. They
coordinate with warehouses, shipping partners, and store staff to make sure
everything runs smoothly.

Think of them as the behind-the-scenes coordinator who makes sure customers
get their orders on time, at the right place!
"""
from crewai import Agent
from crewai.llm import LLM
import sys
import os

# Add Orchestrator to path for inter-agent communication
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, 'Orchestrator'))

from tools import book_shipment, reserve_in_store, notify_staff

# Import inter-agent communication tools
try:
    from inter_agent_communication import (
        request_inventory_help,
        request_payment_help,
        request_support_help,
        request_agent_help
    )
    INTER_AGENT_COMMS_AVAILABLE = True
except ImportError:
    # If orchestrator not available, continue without inter-agent comms
    INTER_AGENT_COMMS_AVAILABLE = False
    request_inventory_help = None
    request_payment_help = None
    request_support_help = None
    request_agent_help = None

# All the tools our fulfillment agent needs to do their job
fulfillment_tools = [
    book_shipment,      # For shipping orders to customer addresses
    reserve_in_store,  # For holding items at stores for pickup
    notify_staff       # For alerting warehouse/store staff about new orders
]

# Add inter-agent communication tools if available
if INTER_AGENT_COMMS_AVAILABLE:
    fulfillment_tools.extend([
        request_inventory_help,  # Can check stock before reserving/shipping
        request_payment_help,    # Can verify payment status
        request_support_help,    # Can get tracking/order info
        request_agent_help       # Generic interface for any agent
    ])


# ============================================================================
# Mock LLM for Testing - Simulates an LLM when testing without API keys
# ============================================================================

class MockLLM:
    """
    A simple mock LLM for testing purposes.
    
    When you're testing the fulfillment agent without setting up API keys,
    this mock LLM will respond instead. It's helpful for development and
    understanding how the agent works!
    """
    def __init__(self):
        self.model = "mock"  # Just a placeholder name
    
    def supports_stop_words(self):
        """Tells CrewAI this mock LLM doesn't support stop words"""
        return False
    
    def call(self, messages, **kwargs):
        """
        Mock response - simulates what a real LLM would say.
        
        In a real scenario, this would call an actual LLM API. For testing,
        we just return a simple message that the agent understands.
        """
        return "I will process this fulfillment request using the appropriate tools."


# ============================================================================
# FULFILLMENT AGENT - The Star of the Show! ⭐
# ============================================================================

fulfillment_agent = Agent(
    role="Backend Logistics Coordinator & Fulfillment Specialist",
    goal=(
        "Efficiently process paid orders and get them to customers! "
        "Whether they need items shipped to their home or reserved at a store "
        "for pickup, you coordinate with logistics partners and store staff "
        "to make sure everything happens smoothly and on time."
    ),
    backstory=(
        "You're a precise, efficient backend system that specializes in "
        "fulfillment operations. You work behind the scenes - you don't talk "
        "directly to customers, but you make sure their orders get where they "
        "need to go!\n\n"
        
        "Your daily work involves:\n"
        "  📦 Processing order data that comes in\n"
        "  🚚 Booking shipments with logistics partners (for ship-to-home)\n"
        "  🏪 Reserving items at stores for customer pickup (for in-store reservations)\n"
        "  📢 Notifying the right staff (warehouse or store) so they know what to do\n"
        "  ✅ Returning clear status reports so everyone knows what happened\n\n"
        
        "You're smart about figuring out the fulfillment type:\n"
        "  - If it's 'ship-to-home' → Use your book_shipment tool\n"
        "  - If it's 'reserve-in-store' → Use your reserve_in_store tool\n"
        "  - Then notify the appropriate staff queue so they can prepare the order\n\n"
        
        "**Inter-Agent Communication:** When you need additional information, you can "
        "request help from other agents through the Orchestrator:\n"
        "  - Use request_inventory_help() to verify stock before fulfillment\n"
        "  - Use request_payment_help() to verify payment status\n"
        "  - Use request_support_help() to get order/tracking information\n"
        "  - All communication flows through Orchestrator - you never talk directly to other agents\n\n"
        
        "You always respond with a clean JSON status report that includes "
        "all the important details like tracking numbers, pickup codes, and "
        "confirmation that staff were notified. Precision and reliability are "
        "your superpowers!"
    ),
    tools=fulfillment_tools,
    verbose=True,              # Show what you're doing (helps with debugging)
    allow_delegation=False,    # You handle fulfillment yourself - no delegation needed
    llm=MockLLM()             # Use mock LLM for testing (replace with real LLM in production)
)