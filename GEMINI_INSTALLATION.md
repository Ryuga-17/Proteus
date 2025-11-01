# Installing Gemini Support for CrewAI

## Issue

If you get this error:
```
ImportError: Google Gen AI native provider not available, to install: uv add "crewai[google-genai]"
```

You need to install Gemini support for CrewAI.

## Solutions

### Option 1: Install CrewAI with Google GenAI support (Recommended)

```bash
pip install 'crewai[google-genai]'
```

### Option 2: Use LangChain Google GenAI directly

```bash
pip install langchain-google-genai
```

Then update `Orchestrator/orchestrator_agent.py` to use:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm_instance = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

And pass it to CrewAI Agent appropriately.

### Option 3: Use OpenAI instead

If you prefer to use OpenAI:

1. Get OpenAI API key: https://platform.openai.com/api-keys
2. Add to `.env` file:
   ```
   OPENAI_API_KEY=your-openai-key-here
   ```
3. Remove or comment out `GOOGLE_API_KEY` in `.env`

The system will automatically use OpenAI instead.

---

## Quick Fix

```bash
# Install Gemini support
pip install 'crewai[google-genai]'

# OR use LangChain
pip install langchain-google-genai

# Then test again
python test_quick.py
```

