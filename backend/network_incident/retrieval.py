"""
Elasticsearch retrieval module for network incident search.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

# Import configuration
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

# Initialize embeddings model
embeddings_model = VertexAIEmbeddings(
    model_name=EMBEDDINGS_MODEL_NAME,
    project=GCP_PROJECT_ID,
    location=GCP_LOCATION
)

def format_search_results(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Formats the raw Elasticsearch response to return only useful fields,
    excluding vector fields.

    Args:
        response (dict): The raw JSON response from an Elasticsearch search.

    Returns:
        list: A list of dictionaries, where each dictionary represents a
              formatted search hit with irrelevant fields removed.
    """
    formatted_hits = []
    # Check if the response contains hits
    if 'hits' in response and 'hits' in response['hits']:
        for hit in response['hits']['hits']:
            # Start with the document's source data
            source = hit.get('_source', {})
            
            formatted_hit = dict()
            # Iterate through the source fields and only keep the useful ones
            for key, value in source.items():
                # A common pattern is to identify vector fields by a suffix like '_vector'.
                # We also check for complex types that might be internal to the search process.
                if not isinstance(value, list) and not key.endswith('_vector'):
                    formatted_hit[key] = value
            
            formatted_hits.append(formatted_hit)
            
    return formatted_hits

def search_network_incidents(
    user_query: str, 
    keyword_fields: List[str], 
    vector_fields: List[str], 
    num_candidates: int = 50, 
    k: int = 10, 
    search_method: str = 'hybrid'
) -> Optional[Dict[str, Any]]:
    """
    Performs a hybrid (keyword + semantic) search on the network_incidents index.

    Args:
        user_query (str): The natural language query from the user.
        keyword_fields (list): A list of text field names for keyword search.
        vector_fields (list): A list of dense_vector field names for semantic search.
        num_candidates (int): Number of candidates for kNN search.
        k (int): Number of results to return.
        search_method (str): Search method ('hybrid', 'vector', 'keyword').

    Returns:
        dict: Elasticsearch search response or None if error.
    """
    try:
        # Connect to Elasticsearch
        es_client = Elasticsearch(
            hosts=[ELASTICSEARCH_HOST],
            basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
        )

        if not es_client.ping():
            logging.error("Could not connect to Elasticsearch. Please check your connection details.")
            return None

        logging.info(f"Connected to Elasticsearch. Performing {search_method} search on index '{INDEX_NAME}'...")

        # 1. Build the keyword-based search query using multi_match
        query_clause = {
            "multi_match": {
                "query": user_query,
                "fields": keyword_fields,
                "type": "cross_fields",
                "operator": "and"
            }
        }

        request_body = {
            "query": query_clause
        }

        # 2. Add kNN search clause if a hybrid or vector search is requested
        if embeddings_model and vector_fields and search_method in ['hybrid', 'vector']:
            logging.info("Generating vector embedding for the query...")
            
            def get_embedding():
                return embeddings_model.embed_query(user_query)
            
            query_vector = get_embedding()

            knn_queries = [
                {
                    "field": vector_field,
                    "query_vector": query_vector,
                    "k": k,
                    "num_candidates": num_candidates
                }
                for vector_field in vector_fields
            ]

            request_body["knn"] = knn_queries
        
        # Execute the search query
        response = es_client.search(index=INDEX_NAME, body=request_body, size=k)

        logging.info(f"Got {len(response['hits']['hits'])} results")
        
        return response

    except Exception as e:
        logging.error(f"An error occurred during search: {e}")
        return None

def get_search_context(
    query: str,
    keyword_fields: List[str] = None,
    vector_fields: List[str] = None,
    num_candidates: int = 50,
    k: int = 20,
    search_method: str = 'hybrid'
) -> str:
    """
    Performs search and returns formatted context as JSON string.
    
    Args:
        query (str): The search query.
        keyword_fields (list): Fields for keyword search.
        vector_fields (list): Fields for vector search.
        num_candidates (int): Number of candidates for kNN.
        k (int): Number of results to return.
        search_method (str): Search method.
        
    Returns:
        str: JSON string of formatted search results.
    """
    # Use default fields if not provided
    if keyword_fields is None:
        keyword_fields = KEYWORD_FIELDS_TO_SEARCH
    if vector_fields is None:
        vector_fields = VECTOR_FIELDS_TO_SEARCH
    
    # Perform search
    search_results = search_network_incidents(
        user_query=query,
        keyword_fields=keyword_fields,
        vector_fields=vector_fields,
        num_candidates=num_candidates,
        k=k,
        search_method=search_method
    )
    
    if search_results is None:
        return "[]"
    
    # Format search results
    context = format_search_results(search_results)
    return json.dumps(context, indent=2)
