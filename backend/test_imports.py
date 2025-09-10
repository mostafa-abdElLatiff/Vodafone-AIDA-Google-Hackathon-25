"""
Test script to verify imports work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly."""
    try:
        print("Testing imports...")
        
        # Test config import
        from configs.config import (
            ELASTICSEARCH_HOST,
            ELASTICSEARCH_USERNAME,
            ELASTICSEARCH_PASSWORD,
            INDEX_NAME,
            GCP_PROJECT_ID,
            GCP_LOCATION,
            EMBEDDINGS_MODEL_NAME,
            KEYWORD_FIELDS_TO_SEARCH,
            VECTOR_FIELDS_TO_SEARCH
        )
        print("✅ Config imports successful")
        
        # Test retrieval import
        from network_incident.retrieval import get_search_context, search_network_incidents
        print("✅ Retrieval imports successful")
        
        # Test agent imports
        from network_incident.agent import network_incident, root_agent
        print("✅ Main agent imports successful")
        
        # Test sub-agent imports
        from network_incident.sub_agents.incident_ingestion.agent import incident_ingestion_agent
        from network_incident.sub_agents.resolution_suggestion.agent import resolution_suggestion_agent
        print("✅ Sub-agent imports successful")
        
        # Test tool imports
        from network_incident.sub_agents.resolution_suggestion.retrieval_tool import incident_retrieval_tool
        print("✅ Tool imports successful")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()
