"""
Client for connecting to the deployed Network Incident Resolution Agent
"""

import os
import json
from typing import Dict, Any, Optional
import requests
from google.cloud import aiplatform
from google.oauth2 import service_account


class AgentClient:
    """Client for interacting with the deployed Network Incident Resolution Agent"""
    
    def __init__(self, 
                 project_id: str = "vodaf-aida25lcpm-205",
                 location: str = "europe-west1",
                 agent_endpoint: Optional[str] = None):
        """
        Initialize the agent client
        
        Args:
            project_id: GCP project ID
            location: GCP location
            agent_endpoint: Direct endpoint URL (if available)
        """
        self.project_id = project_id
        self.location = location
        self.agent_endpoint = agent_endpoint
        
        # Initialize AI Platform
        aiplatform.init(project=project_id, location=location)
    
    def predict(self, query: str, uploaded_data: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a query to the deployed agent
        
        Args:
            query: The user query
            uploaded_data: Optional uploaded data for ingestion
            
        Returns:
            Dictionary containing the agent's response
        """
        try:
            # Prepare the request payload
            payload = {
                "query": query,
                "uploaded_data": uploaded_data
            }
            
            # If we have a direct endpoint, use it
            if self.agent_endpoint:
                response = requests.post(
                    self.agent_endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=60
                )
                response.raise_for_status()
                return response.json()
            
            # Otherwise, use the agent engines API
            # This would require the agent to be deployed and accessible
            # For now, we'll return a placeholder response
            return {
                "answer": "Agent endpoint not configured. Please deploy the agent first.",
                "reference": "Deployment Required"
            }
            
        except Exception as e:
            return {
                "answer": f"Error connecting to agent: {str(e)}",
                "reference": "Connection Error"
            }
    
    def ingest_data(self, data: str) -> Dict[str, Any]:
        """
        Send data for ingestion
        
        Args:
            data: The data to ingest (CSV/Excel content)
            
        Returns:
            Dictionary containing the ingestion result
        """
        return self.predict("ingest this data", uploaded_data=data)


class LocalAgentClient:
    """
    Local client that directly calls the agent functions
    Used for development and testing
    """
    
    def __init__(self):
        """Initialize the local agent client"""
        pass
    
    def predict(self, query: str, uploaded_data: Optional[str] = None) -> Dict[str, Any]:
        """
        Process query using local agent
        
        Args:
            query: The user query
            uploaded_data: Optional uploaded data for ingestion
            
        Returns:
            Dictionary containing the agent's response
        """
        try:
            # Import the agent locally
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
            
            from network_incident.agent import root_agent
            
            # Check if this is an ingestion request
            ingestion_keywords = ['ingest', 'upload', 'process', 'add data', 'insert data']
            is_ingestion_request = any(keyword in query.lower() for keyword in ingestion_keywords)
            
            if is_ingestion_request and uploaded_data:
                # Handle ingestion
                import pandas as pd
                import io
                
                # Convert uploaded data to DataFrame
                df = pd.read_csv(io.StringIO(uploaded_data))
                
                # Call ingestion agent directly
                from network_incident.sub_agents.incident_ingestion.agent import ingest_incident_data
                result = ingest_incident_data(df)
                
                return {
                    "answer": result,
                    "reference": "Data Ingestion"
                }
            else:
                # Handle resolution queries
                from network_incident.inference import chain_inference
                result = chain_inference(query)
                
                return {
                    "answer": result.get("answer", "No response generated"),
                    "reference": "Resolution Suggestion"
                }
                
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "reference": "Processing Error"
            }
    
    def ingest_data(self, data: str) -> Dict[str, Any]:
        """
        Send data for ingestion using local agent
        
        Args:
            data: The data to ingest (CSV/Excel content)
            
        Returns:
            Dictionary containing the ingestion result
        """
        return self.predict("ingest this data", uploaded_data=data)
