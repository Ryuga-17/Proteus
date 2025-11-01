# How to Test Your System 🧪

## Quick Start Testing

### Step 1: Verify Environment Setup

First, make sure your `.env` file is configured:

```bash
python test_env_file.py
```

You should see:
- ✅ `.env` file found
- ✅ `GOOGLE_API_KEY` or `OPENAI_API_KEY` found

### Step 2: Run Quick Test (All Agents)

Test all agents quickly:

```bash
python test_quick.py
```

This will test:
- 📦 Inventory Agent
- 🚚 Fulfillment Agent
- 💳 Payment Agent
- 🎁 Loyalty Agent
- 🎧 Support Agent

### Step 3: Run Individual Agent Tests

Test specific agents:

```bash
python test_basic_functionality.py
```

### Step 4: Test Inter-Agent Communication

Test that agents can request help from each other:

```bash
python test_inter_agent_communication.py
```

---

## Alternative: Run the Orchestrator Directly

### Option A: Use the Main Menu

```bash
cd Orchestrator
python main.py
```

This will run example scenarios and show you a menu.

### Option B: Use Python Scripts

```python
from Orchestrator.main import handle_custom_request

# Test inventory
result = handle_custom_request("Check stock for SKU-123 at all locations")
print(result)

# Test fulfillment
result = handle_custom_request("Ship order ORD-456 to customer address 123 Main St")
print(result)

# Test payment
result = handle_custom_request("Process $150 payment for customer C-789")
print(result)

# Test loyalty
result = handle_custom_request("Calculate price for cart with coupon SAVE20")
print(result)

# Test support
result = handle_custom_request("Track order ORD-12345 for customer C-999")
print(result)
```

---

## Common Issues & Solutions

### Issue 1: "No module named 'orchestrator_agent'"

**Solution:** Make sure you're running from the project root:
```bash
cd "/Users/viveksawant/Desktop/Sales Agent"
python test_quick.py
```

### Issue 2: "AttributeError: 'NoneType' object has no attribute 'supports_stop_words'"

**Solution:** This means the LLM wasn't initialized properly. Try:

1. **Install CrewAI with Gemini support:**
   ```bash
   pip install 'crewai[google-genai]'
   ```

2. **OR use OpenAI instead:**
   - Add `OPENAI_API_KEY=your-key` to your `.env` file
   - The system will automatically use OpenAI

### Issue 3: "Orchestrator requires an LLM"

**Solution:** Make sure your `.env` file contains:
```
GOOGLE_API_KEY=your-gemini-key
```
OR
```
OPENAI_API_KEY=your-openai-key
```

Then verify:
```bash
python test_env_file.py
```

---

## Test Scenarios

### Scenario 1: Inventory Check
```python
from Orchestrator.main import handle_custom_request

result = handle_custom_request(
    "Check stock levels for SKU-123 across all store locations"
)
```

### Scenario 2: Complete Order Flow
```python
result = handle_custom_request(
    "A customer wants to order item SKU-456. "
    "First check if it's in stock, then calculate price with coupon SAVE20, "
    "process payment of $75, and ship to 123 Main St, City, State 12345"
)
```

### Scenario 3: Return Request
```python
result = handle_custom_request(
    "Customer wants to return order ORD-789 because item was damaged. "
    "Check if we have replacement stock, and if not, process refund"
)
```

---

## Expected Output

When tests run successfully, you should see:
- ✅ Agent names and requests
- ✅ Responses from each agent
- ✅ Success messages
- ✅ No error messages

---

## Advanced Testing

### Test Specific Agent Functions

See `TESTING_GUIDE.md` for detailed testing instructions.

### Test Individual Agent Files

Each agent folder has its own `main.py`:
```bash
cd "Inventory agent"
python main.py

cd "../Fullfillment_agent"
python main.py

cd "../payment_agent"
python main.py
```

---

## Need Help?

1. Check `.env` file setup: `python test_env_file.py`
2. Check environment variables: `python test_env_setup.py`
3. See full testing guide: `TESTING_GUIDE.md`
4. See system explanation: `SYSTEM_EXPLANATION.md`

