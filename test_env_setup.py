"""
Environment Variables Test Script
Quickly check if all required environment variables are set
"""
import os

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    project_root = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

def test_environment():
    """Test that required environment variables are set"""
    print("\n" + "=" * 60)
    print("🔍 TESTING ENVIRONMENT VARIABLES")
    print("=" * 60 + "\n")
    
    # Required variables - need at least one LLM provider
    # Check if either OpenAI or Gemini key is set
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")
    
    required_vars = {}
    if openai_key:
        required_vars["OPENAI_API_KEY"] = "OpenAI API key for LLM access ✅ SET"
    if gemini_key:
        required_vars["GOOGLE_API_KEY"] = "Google Gemini API key for LLM access ✅ SET"
    
    # If neither is set, show both as required
    if not required_vars:
        required_vars = {
            "OPENAI_API_KEY": "OpenAI API key for LLM access (OR use GOOGLE_API_KEY for Gemini)",
            "GOOGLE_API_KEY": "Google Gemini API key for LLM access (OR use OPENAI_API_KEY)"
        }
    
    all_set = True
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            # Show partial value for verification (first 8 chars + last 4 chars)
            if len(value) > 12:
                masked_value = value[:8] + "..." + value[-4:]
            else:
                masked_value = "***"
            print(f"✅ {var_name}")
            print(f"   Value: {masked_value}")
            print(f"   Purpose: {description}")
        else:
            print(f"❌ {var_name}: NOT SET")
            print(f"   Purpose: {description}")
            print(f"   Fix: export {var_name}='your-key-here'")
            print(f"   Or: Add to .env file and load with python-dotenv")
            all_set = False
        print()
    
    # Optional/Additional variables
    optional_vars = {
        # Add any optional variables here
    }
    
    if optional_vars:
        print("\n📋 Optional Environment Variables:")
        for var_name, description in optional_vars.items():
            value = os.getenv(var_name)
            status = "✅ Set" if value else "⚪ Not set (optional)"
            print(f"  {status}: {var_name}")
            print(f"    Purpose: {description}")
        print()
    
    # Summary
    print("=" * 60)
    
    # Check if at least one LLM provider is configured
    has_openai = os.getenv("OPENAI_API_KEY")
    has_gemini = os.getenv("GOOGLE_API_KEY")
    has_llm = has_openai or has_gemini
    
    if has_llm:
        print("✅ LLM provider configured!")
        if has_openai:
            print("   Using: OpenAI (OPENAI_API_KEY)")
        if has_gemini:
            print("   Using: Google Gemini (GOOGLE_API_KEY)")
        print("\n🚀 You're ready to run the system!")
        print("\nNext steps:")
        print("  1. Run: python test_quick.py")
        print("  2. Or: cd orchestrator && python main.py")
    else:
        print("⚠️  No LLM provider configured.")
        print("📝 Please set at least one API key:")
        print("\n  Option 1 (OpenAI):")
        print("    export OPENAI_API_KEY='your-openai-key-here'")
        print("\n  Option 2 (Gemini):")
        print("    export GOOGLE_API_KEY='your-gemini-key-here'")
        print("    See GEMINI_SETUP.md for Gemini setup")
        print("\n  Then run: python test_env_setup.py  # Verify again")
    print("=" * 60 + "\n")
    
    return all_set

if __name__ == "__main__":
    test_environment()

