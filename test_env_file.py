"""
Test .env File Setup
Verify that your .env file is configured correctly
"""
import os

def test_env_file_exists():
    """Check if .env file exists"""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_file):
        print("✅ .env file found!")
        print(f"   Location: {env_file}")
        return True
    else:
        print("❌ .env file NOT found")
        print(f"   Expected location: {env_file}")
        print("\n   To create it:")
        print(f"   1. Create a file named '.env' in: {os.path.dirname(__file__)}")
        print("   2. Add your key: GOOGLE_API_KEY=your-key-here")
        return False

def test_dotenv_package():
    """Check if python-dotenv is installed"""
    try:
        import dotenv
        print("✅ python-dotenv package is installed")
        return True
    except ImportError:
        print("⚠️  python-dotenv package NOT installed")
        print("   Install with: pip install python-dotenv")
        print("\n   Note: You can still use .env file, but you'll need to load it manually")
        return False

def test_load_env_file():
    """Try to load .env file and check keys"""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file):
        print("⚠️  Cannot test - .env file not found")
        return False
    
    # Try loading with python-dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env file loaded successfully!")
        
        # Check what keys are in the file
        google_key = os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if google_key:
            masked = google_key[:8] + "..." + google_key[-4:] if len(google_key) > 12 else "***"
            print(f"   ✅ GOOGLE_API_KEY found ({masked})")
        else:
            print("   ⚪ GOOGLE_API_KEY not found in .env")
        
        if openai_key:
            masked = openai_key[:8] + "..." + openai_key[-4:] if len(openai_key) > 12 else "***"
            print(f"   ✅ OPENAI_API_KEY found ({masked})")
        else:
            print("   ⚪ OPENAI_API_KEY not found in .env")
        
        if not google_key and not openai_key:
            print("\n   ⚠️  No API keys found in .env file!")
            print("   Make sure your .env file contains:")
            print("   GOOGLE_API_KEY=your-key-here")
            print("   OR")
            print("   OPENAI_API_KEY=your-key-here")
            return False
        
        return True
        
    except ImportError:
        print("⚠️  python-dotenv not installed - cannot auto-load .env")
        print("   But you can manually read the file or install python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")
        return False

def show_env_file_content():
    """Show .env file content (masked for security)"""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file):
        return
    
    try:
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        print("\n📄 .env file contents (masked):")
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    if value and len(value) > 12:
                        masked_value = value[:8] + "..." + value[-4:]
                    else:
                        masked_value = "***" if value else "(empty)"
                    print(f"   {key}={masked_value}")
                else:
                    print(f"   {line}")
    except Exception as e:
        print(f"   Could not read file: {e}")

def main():
    print("\n" + "=" * 60)
    print("🧪 TESTING .env FILE SETUP")
    print("=" * 60 + "\n")
    
    # Test 1: File exists
    print("1. Checking if .env file exists...")
    file_exists = test_env_file_exists()
    print()
    
    # Test 2: Package installed
    print("2. Checking python-dotenv package...")
    package_installed = test_dotenv_package()
    print()
    
    # Test 3: Load and check keys
    if file_exists:
        print("3. Testing .env file loading...")
        loaded = test_load_env_file()
        print()
        
        # Show content
        show_env_file_content()
        print()
    else:
        loaded = False
        print("\n⚠️  Skipping load test - .env file not found")
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if file_exists and loaded:
        print("✅ .env file is set up correctly!")
        print("\n🚀 Next steps:")
        print("   1. Make sure you load .env in your scripts:")
        print("      from dotenv import load_dotenv")
        print("      load_dotenv()")
        print("   2. Test the system:")
        print("      python test_quick.py")
    elif file_exists:
        if not package_installed:
            print("⚠️  .env file exists but python-dotenv not installed")
            print("\n   Fix:")
            print("   pip install python-dotenv")
            print("   python test_env_file.py  # Run again")
        else:
            print("⚠️  .env file exists but keys might be missing")
            print("\n   Check your .env file contains:")
            print("   GOOGLE_API_KEY=your-key-here")
    else:
        print("❌ .env file not found")
        print("\n   Create it:")
        print("   1. Create file named '.env' in project root")
        print("   2. Add: GOOGLE_API_KEY=your-key-here")
        print("   3. Run this test again")
    
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

