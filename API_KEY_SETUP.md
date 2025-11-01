# Where to Paste Your API Key 🔑

## Quick Answer

**Best Way (Recommended):** Set it as an environment variable - NO code changes needed!

```bash
export GOOGLE_API_KEY="paste-your-key-here"
```

OR for OpenAI:

```bash
export OPENAI_API_KEY="paste-your-key-here"
```

---

## Method 1: Environment Variable (Recommended ✅)

### For Gemini (GOOGLE_API_KEY)

**Terminal/Command Line:**

```bash
# macOS/Linux - Paste your key here
export GOOGLE_API_KEY="paste-your-gemini-key-here"

# Verify it's set
echo $GOOGLE_API_KEY
```

**Windows (PowerShell):**

```powershell
$env:GOOGLE_API_KEY="paste-your-gemini-key-here"

# Verify
echo $env:GOOGLE_API_KEY
```

**Windows (Command Prompt):**

```cmd
set GOOGLE_API_KEY=paste-your-gemini-key-here

# Verify
echo %GOOGLE_API_KEY%
```

---

### For OpenAI (OPENAI_API_KEY)

**Terminal/Command Line:**

```bash
# macOS/Linux
export OPENAI_API_KEY="paste-your-openai-key-here"

# Verify
echo $OPENAI_API_KEY
```

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="paste-your-openai-key-here"
echo $env:OPENAI_API_KEY
```

---

### Using .env File (Easiest for Development)

**Step 1:** Create a file named `.env` in your project root:

```
/Users/viveksawant/Desktop/Sales Agent/.env
```

**Step 2:** Paste your key in the `.env` file:

```
GOOGLE_API_KEY=paste-your-gemini-key-here
```

OR

```
OPENAI_API_KEY=paste-your-openai-key-here
```

**Step 3:** Make sure `.env` is in `.gitignore` (don't commit secrets!):

```bash
echo ".env" >> .gitignore
```

**Step 4:** Install python-dotenv (if not already installed):

```bash
pip install python-dotenv
```

**Step 5:** Load in your Python scripts:

```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file automatically

import os
api_key = os.getenv("GOOGLE_API_KEY")  # Now works!
```

---

## Method 2: Paste Directly in Code Files (Quick Testing Only)

⚠️ **Warning:** Only for testing! Remove before committing to Git!

### Option A: Support Agent

**File:** `post purchase support agent/agents.py`

**Find this line (around line 70):**
```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")  # ← PASTE HERE
)
```

**Replace with:**
```python
llm = LLM(
    model="gemini/gemini-pro",  # For Gemini
    api_key="paste-your-gemini-key-here"  # ← PASTE YOUR KEY HERE
)
```

OR for OpenAI:
```python
llm = LLM(
    model="gpt-3.5-turbo",
    api_key="paste-your-openai-key-here"  # ← PASTE YOUR KEY HERE
)
```

---

### Option B: Loyalty Agent

**File:** `loyalty and offers agent/agents.py`

**Find this line (around line 8):**
```python
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
```

**Replace with (for Gemini):**
```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key="paste-your-gemini-key-here",  # ← PASTE YOUR KEY HERE
    temperature=0.1
)
```

**OR keep OpenAI:**
```python
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "paste-your-openai-key-here"  # ← PASTE YOUR KEY HERE
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
```

---

### Option C: Orchestrator

The orchestrator uses CrewAI's LLM which automatically picks up environment variables. Just set:

```bash
export GOOGLE_API_KEY="paste-your-key-here"
```

Or for OpenAI:
```bash
export OPENAI_API_KEY="paste-your-key-here"
```

No code changes needed!

---

## Quick Setup Checklist

### For Gemini:

```bash
# Step 1: Install package
pip install langchain-google-genai

# Step 2: Set environment variable
export GOOGLE_API_KEY="paste-your-gemini-key-here"

# Step 3: Verify
python test_gemini_setup.py

# Step 4: Test system
python test_quick.py
```

### For OpenAI:

```bash
# Step 1: Set environment variable
export OPENAI_API_KEY="paste-your-openai-key-here"

# Step 2: Verify
python test_env_setup.py

# Step 3: Test system
python test_quick.py
```

---

## Visual Guide: Where to Paste

### Using .env File (Recommended)

```
Sales Agent/                    ← Project root
├── .env                       ← CREATE THIS FILE
│   └── GOOGLE_API_KEY=your-key-here  ← PASTE KEY HERE
├── orchestrator/
├── Inventory agent/
└── ...
```

### Using Environment Variable

```bash
# In your terminal, type:
export GOOGLE_API_KEY="paste-key-between-these-quotes"
```

---

## Which Method Should I Use?

### ✅ Use Environment Variable (.env file or export) if:
- You want to keep keys out of code
- You're working on a shared project
- You plan to commit code to Git
- You want the best practice

### ⚠️ Use Direct Paste in Code if:
- Just testing quickly
- You won't commit the code
- You're learning and want it simple
- Remember to remove before sharing!

---

## Verify Your Key is Set

```bash
# Quick test script
python -c "import os; print('Key set!' if os.getenv('GOOGLE_API_KEY') else 'Key NOT set')"
```

OR run the test script:

```bash
python test_env_setup.py
```

---

## Troubleshooting

### "Key not found" error?

1. **Check you pasted it correctly:**
   - No extra spaces
   - Include quotes if using export: `export KEY="value"`
   - No line breaks

2. **Check the variable name:**
   - Gemini: `GOOGLE_API_KEY`
   - OpenAI: `OPENAI_API_KEY`

3. **Check you're in the right terminal:**
   - If you set it in Terminal 1, run script in Terminal 1
   - Or add to shell profile for permanent set

4. **Try .env file method:**
   - Create `.env` file
   - Paste key there
   - Use `python-dotenv` to load

---

## Example: Complete Setup with .env

**1. Create `.env` file:**
```bash
cd "/Users/viveksawant/Desktop/Sales Agent"
touch .env
```

**2. Open `.env` in editor and paste:**
```
GOOGLE_API_KEY=your-actual-gemini-key-pasted-here
```

**3. Test:**
```bash
python test_gemini_setup.py
```

That's it! 🎉

---

## Summary

**Best Practice:** Use environment variable or `.env` file

**Quick Test:** Paste directly in code (remove before Git!)

**Where to paste:**
- ✅ Environment variable: `export GOOGLE_API_KEY="key"`
- ✅ .env file: `GOOGLE_API_KEY=key`
- ⚠️ Code file: `api_key="key"` (temporary only)

**Verify:** Run `python test_env_setup.py`

