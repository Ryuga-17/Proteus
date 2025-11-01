# Using Google Gemini Instead of OpenAI 🚀

Yes, you can absolutely use Google Gemini! This guide shows you how to switch from OpenAI to Gemini.

---

## Quick Setup

### Step 1: Install Gemini Package

```bash
pip install langchain-google-genai
```

### Step 2: Get Your Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 3: Set Environment Variable

```bash
# Set Gemini API key
export GOOGLE_API_KEY="your-gemini-api-key-here"

# Or for CrewAI LLM (alternative)
export GEMINI_API_KEY="your-gemini-api-key-here"
```

---

## Configuration Options

### Option 1: Using CrewAI's LLM Class (Recommended)

CrewAI's `LLM` class supports Gemini automatically when you set the API key:

```python
from crewai import LLM
import os

# Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "your-key-here"

# CrewAI will automatically use Gemini if GOOGLE_API_KEY is set
llm = LLM(
    model="gemini/gemini-pro",  # or "gemini/gemini-1.5-pro"
    api_key=os.getenv("GOOGLE_API_KEY")
)
```

### Option 2: Using LangChain ChatGoogleGenerativeAI

```python
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",  # or "gemini-1.5-pro"
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)
```

---

## Updating Your Agents

### For Agents Using CrewAI LLM

These agents already support Gemini - just set the environment variable!

**Agents that use `LLM` from CrewAI:**
- ✅ Support Agent (`post purchase support agent/agents.py`)
- ✅ Fulfillment Agent (if using real LLM)
- ✅ Any agent using `from crewai import LLM`

**Update:**
```python
from crewai import LLM
import os

llm = LLM(
    model="gemini/gemini-pro",  # Use Gemini model
    api_key=os.getenv("GOOGLE_API_KEY")  # Use Gemini key
)
```

### For Agents Using LangChain ChatOpenAI

**Agents that need updating:**
- Loyalty Agent (`loyalty and offers agent/agents.py`)
- Payment Agent (if configured)
- Any agent using `from langchain_openai import ChatOpenAI`

**Replace:**
```python
# Old (OpenAI)
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
```

**With:**
```python
# New (Gemini)
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)
```

---

## Step-by-Step Migration

### 1. Install Required Package

```bash
pip install langchain-google-genai
```

### 2. Set Environment Variable

```bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

### 3. Update Agent Files

I'll update the key files for you, but here's what changes:

**File: `loyalty and offers agent/agents.py`**
```python
# Change from:
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

# To:
from langchain_google_genai import ChatGoogleGenerativeAI
import os
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)
```

**File: `post purchase support agent/agents.py`**
```python
# Change from:
llm = LLM(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY", "...")
)

# To:
llm = LLM(
    model="gemini/gemini-pro",  # Gemini model
    api_key=os.getenv("GOOGLE_API_KEY", "...")  # Gemini key
)
```

---

## Available Gemini Models

- `gemini-pro` - Standard model
- `gemini-1.5-pro` - Latest and most capable
- `gemini-1.5-flash` - Faster, lighter model

For CrewAI LLM format: `gemini/gemini-pro` or `gemini/gemini-1.5-pro`

---

## Environment Variables

### For Gemini

```bash
# Primary (recommended)
export GOOGLE_API_KEY="your-gemini-api-key"

# Alternative (some systems)
export GEMINI_API_KEY="your-gemini-api-key"
```

### Supporting Both Providers

You can support both OpenAI and Gemini:

```python
import os

# Check which provider to use
use_gemini = os.getenv("USE_GEMINI", "false").lower() == "true"

if use_gemini:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
else:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
```

Then set:
```bash
export USE_GEMINI=true
export GOOGLE_API_KEY="your-key"
```

---

## Quick Switch Helper Script

Create `switch_to_gemini.py`:

```python
"""Helper script to update agent files for Gemini"""
import os
import re

def update_file(filepath, old_pattern, new_pattern):
    """Update a file with new LLM configuration"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        updated = content.replace(old_pattern, new_pattern)
        
        with open(filepath, 'w') as f:
            f.write(updated)
        
        print(f"✅ Updated {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

# Update loyalty agent
update_file(
    "loyalty and offers agent/agents.py",
    "from langchain_openai import ChatOpenAI",
    "from langchain_google_genai import ChatGoogleGenerativeAI"
)
update_file(
    "loyalty and offers agent/agents.py",
    'llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)',
    'llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.1)'
)

print("\n✅ Migration complete!")
print("Don't forget to: export GOOGLE_API_KEY='your-key-here'")
```

---

## Testing Gemini Setup

```python
# test_gemini_setup.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

def test_gemini():
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return False
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key
        )
        response = llm.invoke("Say hello in one word")
        print(f"✅ Gemini working! Response: {response.content}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini()
```

---

## Summary

**To use Gemini:**

1. **Install:** `pip install langchain-google-genai`
2. **Get Key:** https://makersuite.google.com/app/apikey
3. **Set:** `export GOOGLE_API_KEY="your-key"`
4. **Update agents:** Replace `ChatOpenAI` with `ChatGoogleGenerativeAI`
5. **Test:** Run `python test_gemini_setup.py`

**Quick Command:**
```bash
pip install langchain-google-genai
export GOOGLE_API_KEY="your-key"
python test_quick.py  # Test the system
```

That's it! 🎉

