"""
Minimal test to verify the agent works without ADK CLI.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_minimal_agent():
    """Test the agent with a simple query."""
    try:
        print("Testing minimal agent execution...")
        
        # Import the agent
        from network_incident.agent import network_incident
        
        print(f"Agent name: {network_incident.name}")
        print(f"Agent model: {network_incident.model}")
        print(f"Number of tools: {len(network_incident.tools)}")
        
        # Test with a simple query
        query = "What is the resolution for 4g outage?"
        print(f"\nTesting with query: {query}")
        
        # Run the agent
        result = await network_incident.run_async(query)
        
        print(f"Result: {result}")
        print("✅ Agent execution successful!")
        return True
        
    except Exception as e:
        print(f"❌ Agent execution error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_minimal_agent())
