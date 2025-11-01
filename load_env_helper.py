"""
Environment Variable Loader Helper
Use this at the start of your scripts to automatically load .env file
"""
import os

def load_environment():
    """Load environment variables from .env file if it exists"""
    try:
        from dotenv import load_dotenv
        # Load .env file from project root
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"✅ Loaded .env file from: {env_path}")
            return True
        else:
            print(f"⚠️  .env file not found at: {env_path}")
            return False
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        print("   Continuing without .env file loading...")
        return False

# Auto-load when imported
if __name__ != "__main__":
    load_environment()

