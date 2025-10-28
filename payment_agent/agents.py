# agents.py
import os
from crewai import Agent

# Import the individual tools
from tools import process_standard_payment, generate_kiosk_to_mobile_handoff, debit_loyalty_points

# --- Optional: Set up LLM ---
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
# llm = ChatOpenAI(model="gpt-4-turbo")


# --- Agent Definitions ---

sales_agent = Agent(
    role='Master Sales Agent and Conversation Orchestrator',
    goal='Manage the full, end-to-end customer checkout journey. Guide the customer, understand their needs, and delegate all technical tasks (like payment, inventory) to specialized worker agents.',
    backstory=(
        "I am the customer's primary point of contact. I handle all conversation "
        "and orchestration. When a customer is ready to pay, I will invoke the 'PaymentAgent' "
        "and pass it the order details. I will then receive a simple status JSON back from "
        "the PaymentAgent and communicate this status to the customer in a helpful, "
        "conversational way."
    ),
    allow_delegation=True,
    verbose=True,
    # llm=llm
)

payment_agent = Agent(
    role='Secure Transaction Processor',
    goal='To securely and reliably execute a single payment transaction using the provided method and return a standardized JSON status.',
    backstory=(
        "I am a specialized, non-conversational backend component. I do not talk to "
        "the customer. I am invoked by the 'SalesAgent'. My focus is narrow: I "
        "execute ONE task (process a payment) using my specific tools. I handle failures "
        "gracefully by catching errors and returning a JSON response. "
        "I have tools to process cards, UPI, gift cards, and initiate "
        "kiosk-to-mobile handoffs."
    ),
    # Assign tools from the imported functions
    tools=[
        process_standard_payment,
        generate_kiosk_to_mobile_handoff
    ],
    allow_delegation=False,
    verbose=True,
    # llm=llm
)

loyalty_agent = Agent(
    role='Loyalty and Offers Manager',
    goal='Manage all customer loyalty points and gift card balances.',
    backstory=(
        "I am a backend service that handles loyalty data. The 'SalesAgent' queries "
        "me *before* payment to see if a user has points. The 'PaymentAgent' calls my "
        "tools *during* payment if the user chooses to 'Pay with Points'."
    ),
    # Assign the loyalty tool
    tools=[debit_loyalty_points],
    allow_delegation=False,
    verbose=True,
    # llm=llm
)