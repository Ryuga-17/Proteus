# Environment Variables Guide 🔐

## Required Environment Variables

### ✅ Option 1: OPENAI_API_KEY (Default)

**Required for:** All agents that use LLM (Language Models) with OpenAI

**Description:** Your OpenAI API key for accessing GPT models used by CrewAI agents.

---

### ✅ Option 2: GOOGLE_API_KEY (For Gemini)

**Required for:** All agents that use LLM (Language Models) with Google Gemini

**Description:** Your Google Gemini API key for accessing Gemini models.

**Note:** You can use either OpenAI or Gemini - just set the appropriate key!

**How to set:**

```bash
# macOS/Linux
export OPENAI_API_KEY="your-openai-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=your-openai-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-openai-api-key-here"
```

**Verify it's set:**
```bash
# macOS/Linux
echo $OPENAI_API_KEY

# Windows (PowerShell)
echo $env:OPENAI_API_KEY
```

**Get your OpenAI API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and set it as shown above

**OR Get your Gemini API key:**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and set: `export GOOGLE_API_KEY="your-key"`
5. See `GEMINI_SETUP.md` for full Gemini setup instructions

---

## Optional Environment Variables

### Using `.env` File (Recommended for Development)

Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=your-openai-api-key-here
```

**Note:** Make sure to add `.env` to your `.gitignore` to avoid committing secrets!

```bash
# Add to .gitignore
echo ".env" >> .gitignore
```

---

## Agent-Specific Requirements

### 1. Orchestrator Agent

**Required:**
- `OPENAI_API_KEY` - For orchestrator agent LLM

**Status Check:**
```python
# The orchestrator checks for this on startup
import os
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  Warning: OPENAI_API_KEY not found")
```

---

### 2. Inventory Agent

**Required:**
- `OPENAI_API_KEY` - For inventory orchestrator agent

**Note:** Uses its own internal tools, no additional env vars needed

---

### 3. Fulfillment Agent

**Required:**
- None (uses MockLLM for testing)

**Optional:**
- `OPENAI_API_KEY` - If you want to use a real LLM instead of MockLLM

**How to enable real LLM:**
Edit `Fullfillment_agent/agents.py`:
```python
# Replace MockLLM with real LLM
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4-turbo")  # or gpt-3.5-turbo
```

---

### 4. Payment Agent

**Required:**
- `OPENAI_API_KEY` - For payment crew agents

**Note:** Payment tools work without API key (simulated), but agents need it for reasoning

---

### 5. Loyalty & Offers Agent

**Required:**
- `OPENAI_API_KEY` - For sales_agent and loyalty_agent

**Status:** Checks for API key on startup and exits if not found

---

### 6. Support Agent

**Required:**
- `OPENAI_API_KEY` - For post_purchase_agent

**Note:** Currently hardcoded in `post purchase support agent/agents.py`:
```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key="your-openai-api-key-here"  # Replace this!
)
```

**Better approach:** Use environment variable:
```python
import os
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY", "your-fallback-key")
)
```

---

## Setting Up Environment Variables

### Method 1: Terminal Session (Temporary)

```bash
# Set for current terminal session only
export OPENAI_API_KEY="your-key-here"

# Verify
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

**Note:** This only lasts for the current terminal session. Close terminal = gone.

---

### Method 2: Shell Profile (Permanent)

Add to your shell configuration file:

**For zsh (macOS default):**
```bash
# Add to ~/.zshrc
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
# Add to ~/.bashrc or ~/.bash_profile
echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**For fish shell:**
```bash
# Add to ~/.config/fish/config.fish
set -gx OPENAI_API_KEY "your-key-here"
```

---

### Method 3: Using python-dotenv

Install:
```bash
pip install python-dotenv
```

Create `.env` file in project root:
```
OPENAI_API_KEY=your-openai-api-key-here
```

Load in Python:
```python
from dotenv import load_dotenv
load_dotenv()

# Now os.getenv('OPENAI_API_KEY') will work
import os
api_key = os.getenv('OPENAI_API_KEY')
```

---

### Method 4: IDE/Editor Settings

**VS Code:**
1. Install "Python Environment Manager" extension
2. Or add to `.vscode/settings.json`:
```json
{
    "python.envFile": "${workspaceFolder}/.env"
}
```

**PyCharm:**
1. Go to Run → Edit Configurations
2. Add environment variable: `OPENAI_API_KEY=your-key`

---

## Testing Your Environment Setup

### Quick Test Script

Create `test_env_setup.py`:

```python
import os

def test_environment():
    """Test that required environment variables are set"""
    print("🔍 Testing Environment Variables\n")
    
    # Required variables
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for LLM access"
    }
    
    all_set = True
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            # Show partial value for verification
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"✅ {var_name}: Set ({masked_value})")
            print(f"   Purpose: {description}")
        else:
            print(f"❌ {var_name}: NOT SET")
            print(f"   Purpose: {description}")
            print(f"   Fix: export {var_name}='your-key-here'")
            all_set = False
        print()
    
    # Optional variables
    optional_vars = {}
    if optional_vars:
        print("\n📋 Optional Environment Variables:")
        for var_name, description in optional_vars.items():
            value = os.getenv(var_name)
            status = "✅ Set" if value else "⚪ Not set (optional)"
            print(f"  {status}: {var_name} - {description}")
        print()
    
    # Summary
    print("=" * 60)
    if all_set:
        print("✅ All required environment variables are set!")
        print("🚀 You're ready to run the system!")
    else:
        print("⚠️  Some required environment variables are missing.")
        print("📝 Please set them before running the system.")
    print("=" * 60)
    
    return all_set

if __name__ == "__main__":
    test_environment()
```

Run it:
```bash
python test_env_setup.py
```

---

## Environment Variables by Component

### Orchestrator System
```
OPENAI_API_KEY  (Required)
```

### Individual Agents
```
OPENAI_API_KEY  (Required for all except Fulfillment with MockLLM)
```

### Future Extensions
If you add integrations, you might need:
```
# Payment Gateway (if integrated)
PAYMENT_API_KEY=
PAYMENT_API_SECRET=

# Shipping Carrier APIs
CARRIER_API_KEY=
CARRIER_API_SECRET=

# Database Connections
DATABASE_URL=
DATABASE_USER=
DATABASE_PASSWORD=
```

---

## Security Best Practices

### ✅ DO:

1. **Use `.env` files for development**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Never commit API keys**
   - Don't put keys in code
   - Don't commit `.env` files
   - Don't share keys in chat/email

3. **Use environment variables in production**
   - Set via deployment platform (AWS, Heroku, etc.)
   - Use secrets management (AWS Secrets Manager, etc.)

4. **Rotate keys regularly**
   - Update keys periodically
   - Revoke old keys when rotating

### ❌ DON'T:

1. **Don't hardcode keys in source files**
   ```python
   # ❌ BAD
   api_key = "sk-1234567890abcdef"
   
   # ✅ GOOD
   api_key = os.getenv("OPENAI_API_KEY")
   ```

2. **Don't log API keys**
   ```python
   # ❌ BAD
   print(f"API Key: {api_key}")
   
   # ✅ GOOD
   print(f"API Key: {'*' * len(api_key)}")  # Mask it
   ```

3. **Don't share keys in documentation**
   - Use placeholders in examples
   - Keep keys secret

---

## Troubleshooting

### Problem: "OPENAI_API_KEY not found"

**Solution:**
```bash
# Check if it's set
echo $OPENAI_API_KEY

# If empty, set it
export OPENAI_API_KEY="your-key-here"

# Verify
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

---

### Problem: "Key works in terminal but not in script"

**Solution:**
- Make sure you're setting it in the same terminal where you run the script
- Or use `.env` file with `python-dotenv`
- Or set it in your shell profile

---

### Problem: "API key invalid" or "Authentication failed"

**Solution:**
1. Verify key is correct (no extra spaces)
2. Check key hasn't expired
3. Verify key has credits/quota
4. Check key format: should start with `sk-`

---

### Problem: "Environment variable not persisting"

**Solution:**
- Add to shell profile (`~/.zshrc`, `~/.bashrc`)
- Or use `.env` file
- Or set in IDE run configuration

---

## Quick Setup Checklist

- [ ] Get OpenAI API key from https://platform.openai.com/api-keys
- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Verify with `test_env_setup.py`
- [ ] Add `.env` to `.gitignore` (if using .env file)
- [ ] Update Support Agent to use env var instead of hardcoded key
- [ ] Test with `python test_quick.py`

---

## Summary

**Required:**
- ✅ `OPENAI_API_KEY` - For all agents using LLMs

**Optional:**
- `.env` file with `python-dotenv` for easier management
- Future API keys for integrations

**Security:**
- Never commit keys
- Use environment variables
- Mask keys in logs

**Quick Start:**
```bash
export OPENAI_API_KEY="your-key-here"
python test_env_setup.py  # Verify setup
python test_quick.py      # Test system
```

That's it! Once you have `OPENAI_API_KEY` set, you're ready to go! 🚀

