"""
Retrieval tool for resolution suggestion agent.
"""

from google.adk.tools import FunctionTool
from backend.network_incident.retrieval import get_search_context
from configs.config import KEYWORD_FIELDS_TO_SEARCH, VECTOR_FIELDS_TO_SEARCH
import logging

class NetworkIncidentRetrievalTool:
    """
    A tool that searches for similar network incidents using Elasticsearch.
    """
    name = "search_similar_incidents"
    description = "Searches for similar network incidents based on the provided query using hybrid search (keyword + semantic)."

    def __call__(self, query: str, num_results: int = 20) -> str:
        """
        Search for similar incidents.
        
        Args:
            query (str): The search query describing the current incident.
            num_results (int): Number of results to return.
            
        Returns:
            str: JSON string containing similar incidents.
        """
        try:
            logging.info(f"Searching for similar incidents with query: {query}")
            
            context = get_search_context(
                query=query,
                keyword_fields=KEYWORD_FIELDS_TO_SEARCH,
                vector_fields=VECTOR_FIELDS_TO_SEARCH,
                k=num_results,
                search_method='hybrid'
            )
            
            logging.info(f"Found context with {len(context)} characters")
            return context
            
        except Exception as e:
            logging.error(f"Error during incident search: {e}")
            return f"Error searching for incidents: {e}"

# Create the tool instance
incident_retrieval_tool = FunctionTool(NetworkIncidentRetrievalTool())
