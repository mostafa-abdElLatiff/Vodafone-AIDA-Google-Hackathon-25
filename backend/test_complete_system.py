"""
Complete system test to verify everything works together.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_complete_system():
    """Test the complete system integration."""
    try:
        print("Testing complete system integration...")
        
        # Test 1: Import all components
        print("\n1. Testing imports...")
        from network_incident.agent import network_incident, root_agent
        from network_incident.sub_agents.incident_ingestion.agent import incident_ingestion_agent
        from network_incident.sub_agents.resolution_suggestion.agent import resolution_suggestion_agent
        from network_incident.sub_agents.resolution_suggestion.retrieval_tool import incident_retrieval_tool
        print("✅ All imports successful")
        
        # Test 2: Verify agent structure
        print("\n2. Testing agent structure...")
        print(f"Main agent: {network_incident.name}")
        print(f"  - Model: {network_incident.model}")
        print(f"  - Tools: {len(network_incident.tools)}")
        
        print(f"Ingestion agent: {incident_ingestion_agent.name}")
        print(f"  - Tools: {len(incident_ingestion_agent.tools)}")
        
        print(f"Resolution agent: {resolution_suggestion_agent.name}")
        print(f"  - Tools: {len(resolution_suggestion_agent.tools)}")
        print("✅ Agent structure verified")
        
        # Test 3: Test tool declarations
        print("\n3. Testing tool declarations...")
        try:
            for tool in incident_ingestion_agent.tools:
                declaration = tool._get_declaration()
                print(f"  - {tool.name}: ✅")
        except Exception as e:
            print(f"  - Ingestion tools error: {e}")
            return False
        
        try:
            for tool in resolution_suggestion_agent.tools:
                declaration = tool._get_declaration()
                print(f"  - {tool.name}: ✅")
        except Exception as e:
            print(f"  - Resolution tools error: {e}")
            return False
        
        print("✅ All tool declarations successful")
        
        # Test 4: Test configuration
        print("\n4. Testing configuration...")
        from configs.config import (
            ELASTICSEARCH_HOST,
            ELASTICSEARCH_USERNAME,
            ELASTICSEARCH_PASSWORD,
            INDEX_NAME,
            GCP_PROJECT_ID,
            GCP_LOCATION,
            EMBEDDINGS_MODEL_NAME
        )
        print(f"  - Elasticsearch: {ELASTICSEARCH_HOST}")
        print(f"  - Index: {INDEX_NAME}")
        print(f"  - GCP Project: {GCP_PROJECT_ID}")
        print(f"  - Embeddings Model: {EMBEDDINGS_MODEL_NAME}")
        print("✅ Configuration loaded successfully")
        
        print("\n🎉 Complete system test passed!")
        print("\nThe system is ready to use. You can now run:")
        print("  adk run backend.network_incident.agent:root_agent")
        return True
        
    except Exception as e:
        print(f"❌ System test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_complete_system()
