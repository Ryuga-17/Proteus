# Verify Your .env File Setup ✅

Great! You've created a `.env` file. Now let's verify it's set up correctly.

## Quick Verification

Run this command:

```bash
python test_env_file.py
```

This will check:
- ✅ If `.env` file exists
- ✅ If `python-dotenv` package is installed
- ✅ If your API keys are loaded correctly
- ✅ Shows what keys are found (masked for security)

---

## What Should Be In Your .env File

Your `.env` file should look like this:

```
GOOGLE_API_KEY=your-actual-gemini-key-here
```

OR for OpenAI:

```
OPENAI_API_KEY=your-actual-openai-key-here
```

**Important:**
- No spaces around the `=` sign
- No quotes needed (but won't hurt if you have them)
- One key per line
- No trailing spaces

---

## If You Get "python-dotenv not installed"

Install it:

```bash
pip install python-dotenv
```

Then run the test again:

```bash
python test_env_file.py
```

---

## After Verification

Once your `.env` file is verified:

1. **Test the system:**
   ```bash
   python test_quick.py
   ```

2. **Or test through orchestrator:**
   ```bash
   cd orchestrator
   python main.py
   ```

---

## Troubleshooting

### "Key not found" error?

1. Check your `.env` file is in the project root:
   ```
   /Users/viveksawant/Desktop/Sales Agent/.env
   ```

2. Check the key name is correct:
   - For Gemini: `GOOGLE_API_KEY`
   - For OpenAI: `OPENAI_API_KEY`

3. Check no extra spaces:
   ```
   ✅ GOOGLE_API_KEY=your-key
   ❌ GOOGLE_API_KEY = your-key  (has spaces)
   ```

4. Make sure the key value is after the `=` sign

---

## Example .env File

Here's what a correct `.env` file looks like:

```
# This is a comment - ignored by the system
GOOGLE_API_KEY=AIzaSyExample123456789YourActualKeyHere

# You can have multiple keys
# OPENAI_API_KEY=sk-example123456789
```

**Note:** The `#` lines are comments and are ignored.

---

## Need Help?

Run:

```bash
python test_env_file.py
```

It will tell you exactly what's wrong and how to fix it! 🔧

