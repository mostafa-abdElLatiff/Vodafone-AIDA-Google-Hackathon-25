"""
Test script to verify deployment works correctly
"""

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def test_deployment_imports():
    """Test that all deployment imports work"""
    try:
        print("🧪 Testing deployment imports...")
        
        # Test main deployment script
        from deploy import create, list_agents, delete
        print("✅ Deployment functions imported successfully")
        
        # Test agent imports
        from backend.network_incident.agent import root_agent
        print("✅ Network incident agent imported successfully")
        
        # Test configs
        from configs.config import GCP_PROJECT_ID, GCP_LOCATION, DATASET_ID, TABLE_ID
        print("✅ Configs imported successfully")
        print(f"  Project ID: {GCP_PROJECT_ID}")
        print(f"  Location: {GCP_LOCATION}")
        print(f"  Dataset: {DATASET_ID}")
        print(f"  Table: {TABLE_ID}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_structure():
    """Test that the agent structure is correct"""
    try:
        print("\n🧪 Testing agent structure...")
        
        from backend.network_incident.agent import root_agent
        from backend.network_incident.sub_agents.incident_ingestion.agent import incident_ingestion_agent
        from backend.network_incident.sub_agents.resolution_suggestion.agent import resolution_suggestion_agent
        
        print(f"✅ Root agent: {root_agent.name}")
        print(f"✅ Ingestion agent: {incident_ingestion_agent.name}")
        print(f"✅ Resolution agent: {resolution_suggestion_agent.name}")
        print(f"✅ Root agent tools: {len(root_agent.tools)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Network Incident Agent - Deployment Test")
    print("=" * 60)
    
    tests = [
        ("Deployment Imports", test_deployment_imports),
        ("Agent Structure", test_agent_structure)
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
        print("🎉 All tests passed! Ready for deployment.")
        print("\nTo deploy, run:")
        print("  python deploy.py --create --project_id=vodaf-aida25lcpm-205 --location=europe-west1 --bucket=aida-hackathon-team-5")
    else:
        print("⚠️  Some tests failed. Please fix issues before deploying.")

if __name__ == "__main__":
    main()
