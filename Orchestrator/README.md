# Master Orchestrator Agent

This orchestrator agent coordinates all retail agents in the system, routing requests to the appropriate specialized agents and managing multi-agent workflows.

## Architecture

The orchestrator acts as a central router that:
- **Analyzes** incoming requests to determine intent
- **Routes** requests to specialized agents
- **Coordinates** multi-step workflows across agents
- **Synthesizes** results into unified responses

## Agent Coordination

The orchestrator manages the following specialized agents:

1. **Inventory Agent** (`Inventory agent/`)
   - Stock level checks
   - Inter-store transfers
   - Supplier procurement orders

2. **Fulfillment Agent** (`Fullfillment_agent/`)
   - Ship-to-home orders
   - In-store reservations
   - Warehouse coordination

3. **Payment Agent** (`payment_agent/`)
   - Payment processing
   - Transaction management
   - Kiosk-to-mobile handoffs

4. **Loyalty and Offers Agent** (`loyalty and offers agent/`)
   - Pricing calculations
   - Loyalty points management
   - Coupon and promotion application

5. **Post Purchase Support Agent** (`post purchase support agent/`)
   - Order tracking
   - Returns and exchanges
   - Customer feedback collection

## Files Structure

```
orchestrator/
├── orchestrator_agent.py      # Main orchestrator agent definition
├── orchestrator_tools.py       # Routing tools for each sub-agent
├── orchestrator_tasks.py       # Example task definitions
├── main.py                     # Entry point for running the orchestrator
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

1. Install dependencies:
```bash
cd orchestrator
pip install -r requirements.txt
```

2. Set up your OpenAI API key (if not already set):
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Note: Some agents may use mock LLMs if API keys are not configured.

## Usage

### Running Example Scenarios

Run the main script to execute example scenarios:

```bash
python main.py
```

This will run pre-defined scenarios demonstrating:
- Inventory management workflows
- Order fulfillment
- Payment processing
- Customer support
- Checkout with loyalty points
- Return/exchange workflows

### Custom Requests

You can also handle custom requests programmatically:

```python
from main import handle_custom_request

# Example: Check inventory and fulfill order
result = handle_custom_request(
    description=(
        "A customer wants to order SKU RED-SHIRT-SML. "
        "First check if it's in stock, then process the fulfillment."
    )
)
```

### Programmatic Usage

```python
from crewai import Crew, Process
from orchestrator_agent import orchestrator_agent
from orchestrator_tasks import create_custom_task

# Create a custom task
task = create_custom_task(
    description="Your request here",
    expected_output="Expected output format"
)

# Create and run the crew
crew = Crew(
    agents=[orchestrator_agent],
    tasks=[task],
    process=Process.sequential,
    memory=True,
    verbose=2
)

result = crew.kickoff()
print(result)
```

## How It Works

1. **Request Analysis**: The orchestrator uses `analyze_intent` tool to determine which agent(s) should handle the request
2. **Routing**: Based on intent, requests are routed to appropriate agents using:
   - `route_to_inventory` - For stock/transfer requests
   - `route_to_fulfillment` - For shipping/reservation requests
   - `route_to_payment` - For payment/transaction requests
   - `route_to_loyalty` - For pricing/points/offers requests
   - `route_to_support` - For tracking/returns/support requests
3. **Coordination**: For multi-step workflows, the orchestrator can call multiple agents in sequence
4. **Synthesis**: Results from all agents are combined into a unified response

## Example Workflows

### Simple Workflow: Inventory Check
```
Request → Orchestrator → Inventory Agent → Result
```

### Complex Workflow: Order Processing
```
Request → Orchestrator 
  ├─→ Inventory Agent (check stock)
  ├─→ Payment Agent (process payment)
  └─→ Fulfillment Agent (ship order)
  → Synthesized Result
```

## Configuration

- **Verbosity**: Adjust `verbose` parameter in crew creation (0-2)
- **Memory**: Enable/disable memory for context across interactions
- **Max Iterations**: Configure `max_iter` in orchestrator agent if needed

## Troubleshooting

### Import Errors
If you encounter import errors, ensure:
- All sub-agent directories are accessible
- Python path includes parent directory
- All dependencies are installed

### Agent Not Responding
- Check that sub-agent directories exist
- Verify sub-agent dependencies are installed
- Check for API key configuration (if needed)

### Routing Issues
- Review request descriptions - be specific about what you need
- Check orchestrator logs for intent analysis results
- Verify the target agent is properly configured

## Next Steps

- Add more sophisticated intent analysis
- Implement caching for common requests
- Add monitoring and logging
- Create API wrapper for external access
- Add authentication and authorization


