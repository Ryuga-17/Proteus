"""
Test Gemini API Setup
Quick script to verify your Gemini API key works
"""
import os

def test_gemini_import():
    """Test if langchain-google-genai is installed"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain-google-genai package installed")
        return True
    except ImportError:
        print("❌ langchain-google-genai not installed")
        print("   Install with: pip install langchain-google-genai")
        return False

def test_gemini_key():
    """Test if GOOGLE_API_KEY is set"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        print("   Set it with: export GOOGLE_API_KEY='your-key-here'")
        print("   Get key from: https://makersuite.google.com/app/apikey")
        return False
    
    # Show partial key
    masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    print(f"✅ GOOGLE_API_KEY is set ({masked})")
    return True

def test_gemini_connection():
    """Test actual connection to Gemini API"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️  Skipping connection test - no API key")
            return False
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0.1
        )
        
        # Simple test
        response = llm.invoke("Say 'Hello' if you can hear me.")
        print(f"✅ Gemini API connection successful!")
        print(f"   Response: {response.content[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API connection failed: {e}")
        print("   Check your API key and internet connection")
        return False

def main():
    print("\n" + "=" * 60)
    print("🧪 TESTING GEMINI SETUP")
    print("=" * 60 + "\n")
    
    results = []
    
    # Test 1: Package installation
    print("1. Checking package installation...")
    results.append(("Package", test_gemini_import()))
    print()
    
    # Test 2: API key
    print("2. Checking API key...")
    results.append(("API Key", test_gemini_key()))
    print()
    
    # Test 3: Connection
    if results[-1][1]:  # If API key is set
        print("3. Testing Gemini API connection...")
        results.append(("Connection", test_gemini_connection()))
    else:
        print("3. Skipping connection test (no API key)")
        results.append(("Connection", False))
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Gemini is ready to use!")
        print("   You can now use Gemini instead of OpenAI")
        print("   Run: python test_quick.py")
    else:
        print("\n⚠️  Please fix the issues above")
        print("\nQuick setup:")
        print("  1. pip install langchain-google-genai")
        print("  2. export GOOGLE_API_KEY='your-key-here'")
        print("  3. python test_gemini_setup.py")
    
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

