"""
Test script to verify ADK agent instantiation works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_agent_instantiation():
    """Test that the ADK agent can be instantiated without errors."""
    try:
        print("Testing ADK agent instantiation...")
        
        # Test main agent
        from network_incident.agent import network_incident, root_agent
        print("✅ Main agent instantiated successfully")
        
        # Test sub-agents
        from network_incident.sub_agents.incident_ingestion.agent import incident_ingestion_agent
        from network_incident.sub_agents.resolution_suggestion.agent import resolution_suggestion_agent
        print("✅ Sub-agents instantiated successfully")
        
        # Test tools
        from network_incident.sub_agents.resolution_suggestion.retrieval_tool import incident_retrieval_tool
        print("✅ Tools instantiated successfully")
        
        # Test that the agent has the expected attributes
        print(f"Main agent name: {network_incident.name}")
        print(f"Main agent model: {network_incident.model}")
        print(f"Number of tools in main agent: {len(network_incident.tools)}")
        
        print(f"Ingestion agent name: {incident_ingestion_agent.name}")
        print(f"Number of tools in ingestion agent: {len(incident_ingestion_agent.tools)}")
        
        print(f"Resolution agent name: {resolution_suggestion_agent.name}")
        print(f"Number of tools in resolution agent: {len(resolution_suggestion_agent.tools)}")
        
        print("\n🎉 All agents instantiated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Agent instantiation error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent_instantiation()
