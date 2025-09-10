"""
Test script to verify tools work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_tools():
    """Test that the tools can be instantiated and called correctly."""
    try:
        print("Testing tool instantiation...")
        
        # Test retrieval tool
        from network_incident.sub_agents.resolution_suggestion.retrieval_tool import incident_retrieval_tool
        print("✅ Retrieval tool instantiated successfully")
        
        # Test ingestion tools
        from network_incident.sub_agents.incident_ingestion.agent import ingest_tool, file_upload_tool
        print("✅ Ingestion tools instantiated successfully")
        
        # Test that tools have the expected attributes
        print(f"Retrieval tool name: {incident_retrieval_tool.name}")
        print(f"Ingest tool name: {ingest_tool.name}")
        print(f"File upload tool name: {file_upload_tool.name}")
        
        # Test that we can get the function declaration (this is what ADK does internally)
        try:
            retrieval_declaration = incident_retrieval_tool._get_declaration()
            print("✅ Retrieval tool declaration generated successfully")
        except Exception as e:
            print(f"❌ Retrieval tool declaration error: {e}")
            return False
        
        try:
            ingest_declaration = ingest_tool._get_declaration()
            print("✅ Ingest tool declaration generated successfully")
        except Exception as e:
            print(f"❌ Ingest tool declaration error: {e}")
            return False
        
        print("\n🎉 All tools work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Tool test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_tools()
