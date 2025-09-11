"""
Client for connecting to the deployed Network Incident Resolution Agent
"""

import os
import json
import io
import logging
from typing import Dict, Any, Optional, Union
import requests
import pandas as pd
from google.cloud import aiplatform
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


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
    
    def predict(self, query: str, file_content: Optional[bytes] = None, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a query to the deployed agent
        
        Args:
            query: The user query
            file_content: Optional uploaded file content as bytes
            filename: Optional filename for uploaded file
            
        Returns:
            Dictionary containing the agent's response
        """
        try:
            # Prepare the request payload
            payload = {
                "query": query,
                "file_content": file_content.hex() if file_content else None,  # Convert bytes to hex string
                "filename": filename
            }
            
            # If we have a direct endpoint, use it
            if self.agent_endpoint:
                response = requests.post(
                    self.agent_endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=300  # Increased timeout for file processing
                )
                response.raise_for_status()
                return response.json()
            
            # Otherwise, use the agent engines API
            # This would require the agent to be deployed and accessible
            return {
                "answer": "Agent endpoint not configured. Please deploy the agent first.",
                "reference": "Deployment Required"
            }
            
        except Exception as e:
            logger.error(f"Error connecting to agent: {e}")
            return {
                "answer": f"Error connecting to agent: {str(e)}",
                "reference": "Connection Error"
            }


class LocalAgentClient:
    """
    Local client that directly calls the agent functions
    Used for development and testing
    """
    
    def __init__(self):
        """Initialize the local agent client"""
        self.agent = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the ADK agent"""
        try:
            # Import the agent
            import sys
            import os
            
            # Add the backend path to sys.path if not already there
            backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
            if backend_path not in sys.path:
                sys.path.append(backend_path)
            
            # Import the root agent
            from network_incident.agent import root_agent
            self.agent = root_agent
            logger.info("Agent initialized successfully")
            
        except ImportError as e:
            logger.error(f"Failed to import agent: {e}")
            self.agent = None
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            self.agent = None
    
    def predict(self, query: str, file_content: Optional[bytes] = None, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Process query using local agent
        
        Args:
            query: The user query
            file_content: Optional uploaded file content as bytes
            filename: Optional filename for uploaded file
            
        Returns:
            Dictionary containing the agent's response
        """
        try:
            if self.agent is None:
                return {
                    "answer": "Agent not properly initialized. Please check your setup.",
                    "reference": "Initialization Error"
                }
            
            # Prepare the input for the agent
            agent_input = {"query": query}
            
            # If file is uploaded, add it to the input
            if file_content and filename:
                agent_input["file_content"] = file_content
                agent_input["filename"] = filename
                logger.info(f"Processing query with uploaded file: {filename}")
            else:
                logger.info(f"Processing query: {query}")
            
            # Call the agent
            result = self.agent.run(agent_input)
            
            # Extract the response based on agent's output structure
            if isinstance(result, dict):
                # Handle different possible response formats
                if "answer" in result:
                    return {
                        "answer": result["answer"],
                        "reference": result.get("reference", "Agent Response")
                    }
                elif "ingestion_status" in result:
                    return {
                        "answer": result["ingestion_status"],
                        "reference": "Data Ingestion"
                    }
                else:
                    # If result is a dict but doesn't have expected keys
                    return {
                        "answer": str(result),
                        "reference": "Agent Response"
                    }
            else:
                # If result is not a dict, convert to string
                return {
                    "answer": str(result),
                    "reference": "Agent Response"
                }
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": f"Error processing query: {str(e)}",
                "reference": "Processing Error" 
            }   

    def ingest_data(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Send data for ingestion using local agent
        
        Args:
            file_content: The file content as bytes
            filename: The filename
            
        Returns:
            Dictionary containing the ingestion result
        """
        ingestion_query = f"Please ingest the data from the uploaded file: {filename}"
        return self.predict(ingestion_query, file_content=file_content, filename=filename)
    
    def search_incidents(self, query: str) -> Dict[str, Any]:
        """
        Search for incident resolution suggestions
        
        Args:
            query: The search query describing the incident
            
        Returns:
            Dictionary containing the search results and suggestions
        """
        search_query = f"Please help me resolve this network incident: {query}"
        return self.predict(search_query)


# # Convenience functions for easier usage
# def create_local_client() -> LocalAgentClient:
#     """Create a local agent client"""
#     return LocalAgentClient()


# def create_remote_client(project_id: str = "vodaf-aida25lcpm-205", 
#                         location: str = "europe-west1",
#                         agent_endpoint: Optional[str] = None) -> AgentClient:
#     """Create a remote agent client"""
#     return AgentClient(project_id=project_id, location=location, agent_endpoint=agent_endpoint)


# # Example usage functions
# def process_user_request(query: str, 
#                         uploaded_file: Optional[bytes] = None, 
#                         filename: Optional[str] = None,
#                         use_local: bool = True) -> Dict[str, Any]:
#     """
#     Process a user request with optional file upload
    
#     Args:
#         query: User query
#         uploaded_file: Optional uploaded file content
#         filename: Optional filename
#         use_local: Whether to use local or remote client
        
#     Returns:
#         Agent response
#     """
#     if use_local:
#         client = create_local_client()
#     else:
#         client = create_remote_client()
    
#     return client.predict(query, file_content=uploaded_file, filename=filename)


# def ingest_file_data(file_content: bytes, filename: str, use_local: bool = True) -> Dict[str, Any]:
#     """
#     Ingest file data into the system
    
#     Args:
#         file_content: File content as bytes
#         filename: Name of the file
#         use_local: Whether to use local or remote client
        
#     Returns:
#         Ingestion result
#     """
#     if use_local:
#         client = create_local_client()
#     else:
#         client = create_remote_client()
    
#     return client.ingest_data(file_content, filename)