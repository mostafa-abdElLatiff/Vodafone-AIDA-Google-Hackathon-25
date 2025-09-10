"""
Test script to verify the deployment and connection
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_local_agent():
    """Test the local agent functionality"""
    print("🧪 Testing local agent functionality...")
    
    try:
        # Test imports
        from network_incident.agent import root_agent
        from network_incident.sub_agents.incident_ingestion.agent import incident_ingestion_agent
        from network_incident.sub_agents.resolution_suggestion.agent import resolution_suggestion_agent
        
        print("✅ All agent imports successful")
        
        # Test agent structure
        print(f"Root agent: {root_agent.name}")
        print(f"Ingestion agent: {incident_ingestion_agent.name}")
        print(f"Resolution agent: {resolution_suggestion_agent.name}")
        
        # Test with sample data
        sample_data = """incident_id,timestamp,severity,service_impact,incident_description,resolution_steps,root_cause
INC001,2024-01-01 10:00:00,High,4G Outage,4G network down in London,Restart base station,Hardware failure
INC002,2024-01-02 14:30:00,Medium,Packet Loss,High packet loss in Manchester,Check routing tables,Configuration error"""
        
        # Test ingestion
        from network_incident.sub_agents.incident_ingestion.agent import ingest_incident_data
        df = pd.read_csv(pd.io.common.StringIO(sample_data))
        
        print("✅ Sample data created and validated")
        print(f"Sample data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Test data validation
        from network_incident.sub_agents.incident_ingestion.file_handler import validate_dataframe
        is_valid = validate_dataframe(df)
        print(f"Data validation: {'✅ PASSED' if is_valid else '❌ FAILED'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Local agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frontend_client():
    """Test the frontend client"""
    print("\n🧪 Testing frontend client...")
    
    try:
        # Add frontend to path
        frontend_dir = Path(__file__).parent.parent / "frontend"
        sys.path.insert(0, str(frontend_dir))
        
        from agent_client import LocalAgentClient
        
        client = LocalAgentClient()
        print("✅ Agent client created successfully")
        
        # Test prediction
        response = client.predict("How to resolve 4G outage issues?")
        print(f"✅ Prediction test: {response['answer'][:100]}...")
        
        # Test ingestion
        sample_data = """incident_id,timestamp,severity,service_impact,incident_description,resolution_steps,root_cause
INC001,2024-01-01 10:00:00,High,4G Outage,4G network down in London,Restart base station,Hardware failure"""
        
        response = client.ingest_data(sample_data)
        print(f"✅ Ingestion test: {response['answer'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Frontend client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_deployment_script():
    """Test the deployment script"""
    print("\n🧪 Testing deployment script...")
    
    try:
        from deployment.deploy import create, list_agents, delete
        print("✅ Deployment functions imported successfully")
        
        # Test that we can access the root agent
        from network_incident.agent import root_agent
        print(f"✅ Root agent accessible: {root_agent.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment script test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Network Incident Agent - Deployment Test Suite")
    print("=" * 60)
    
    tests = [
        ("Local Agent", test_local_agent),
        ("Frontend Client", test_frontend_client),
        ("Deployment Script", test_deployment_script)
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
        print("\nNext steps:")
        print("1. Run: python deploy_agent.py deploy")
        print("2. Note the agent endpoint URL")
        print("3. Update frontend with the endpoint URL")
        print("4. Redeploy frontend to Cloud Run")
    else:
        print("⚠️  Some tests failed. Please fix issues before deploying.")

if __name__ == "__main__":
    main()
