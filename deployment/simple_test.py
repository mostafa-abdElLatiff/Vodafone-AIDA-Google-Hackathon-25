"""
Simple test script that doesn't require ADK installation
"""

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def test_basic_imports():
    """Test basic imports without ADK dependencies"""
    try:
        print("🧪 Testing basic imports...")
        
        # Test configs
        from configs.config import GCP_PROJECT_ID, GCP_LOCATION, DATASET_ID, TABLE_ID
        print("✅ Configs imported successfully")
        print(f"  Project ID: {GCP_PROJECT_ID}")
        print(f"  Location: {GCP_LOCATION}")
        print(f"  Dataset: {DATASET_ID}")
        print(f"  Table: {TABLE_ID}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic import test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    try:
        print("\n🧪 Testing file structure...")
        
        # Check required files exist
        required_files = [
            "backend/network_incident/agent.py",
            "backend/network_incident/__init__.py",
            "configs/config.py",
            "deployment/deploy.py"
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path} exists")
            else:
                print(f"❌ {file_path} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ File structure test failed: {e}")
        return False

def test_dependencies():
    """Test that basic dependencies are available"""
    try:
        print("\n🧪 Testing dependencies...")
        
        # Test basic Python modules
        try:
            import pandas
            print("✅ pandas available")
        except Exception as e:
            print(f"⚠️  pandas issue: {e}")
        
        import json
        print("✅ json available")
        
        import os
        print("✅ os available")
        
        import sys
        print("✅ sys available")
        
        return True
        
    except Exception as e:
        print(f"❌ Dependencies test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Network Incident Agent - Simple Deployment Test")
    print("=" * 60)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("File Structure", test_file_structure),
        ("Dependencies", test_dependencies)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"  Test failed: {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 Basic tests passed! Project structure is ready.")
        print("\nNote: For full deployment, you need to install Google ADK:")
        print("  pip install google-adk")
        print("  pip install google-cloud-aiplatform")
        print("  pip install google-genai")
    else:
        print("⚠️  Some tests failed. Please fix issues before deploying.")

if __name__ == "__main__":
    main()
