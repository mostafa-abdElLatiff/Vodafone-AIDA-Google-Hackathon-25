"""
Main inference module for network incident resolution.
"""

import json
import logging
from typing import Dict, Any, Optional
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate

from .retrieval import get_search_context
from .sub_agents.resolution_suggestion.prompt import RESOLUTION_SUGGESTION_PROMPT
from configs.config import (
    KEYWORD_FIELDS_TO_SEARCH,
    VECTOR_FIELDS_TO_SEARCH,
    LLM_NAME,
    GCP_PROJECT_ID,
    GCP_LOCATION
)

# Initialize the LLM
llm = ChatVertexAI(
    model_name=LLM_NAME,
    project=GCP_PROJECT_ID,
    location=GCP_LOCATION,
    temperature=0.1
)

# Create the prompt template
prompt_main = ChatPromptTemplate.from_template(RESOLUTION_SUGGESTION_PROMPT)

def chain_inference(
    query: str,
    keyword_fields: list = None,
    vector_fields: list = None,
    num_candidates: int = 50,
    k: int = 20,
    search_method: str = 'hybrid',
) -> Dict[str, Any]:
    """
    Performs end-to-end inference for network incident resolution.
    
    Args:
        query (str): The incident query.
        keyword_fields (list): Fields for keyword search.
        vector_fields (list): Fields for vector search.
        num_candidates (int): Number of candidates for kNN.
        k (int): Number of results to return.
        search_method (str): Search method.
        
    Returns:
        dict: The inference result with answer.
    """
    try:
        # Use default fields if not provided
        if keyword_fields is None:
            keyword_fields = KEYWORD_FIELDS_TO_SEARCH
        if vector_fields is None:
            vector_fields = VECTOR_FIELDS_TO_SEARCH
        
        # Perform search
        search_results = get_search_context(
            query=query,
            keyword_fields=keyword_fields,
            vector_fields=vector_fields,
            num_candidates=num_candidates,
            k=k,
            search_method=search_method
        )
        
        # Inference Chain
        chain = (
            RunnableParallel(
                question=itemgetter("question"),
                context=itemgetter("context"),
            )
            | RunnableParallel(
                answer=prompt_main | llm | StrOutputParser(),
            )
            | RunnableParallel(
                answer=itemgetter("answer"), 
            )
        )
        
        result = chain.invoke(
            {
                "question": query,
                "context": search_results,
            }
        )

        return result
        
    except Exception as e:
        logging.error(f"Chain inference failed: {e}")
        return {"answer": f"Error during inference: {e}"}

def process_incident_query(query: str) -> str:
    """
    Simple interface for processing incident queries.
    
    Args:
        query (str): The incident query.
        
    Returns:
        str: The resolution suggestion.
    """
    try:
        result = chain_inference(
            query=query,
            keyword_fields=KEYWORD_FIELDS_TO_SEARCH,
            vector_fields=VECTOR_FIELDS_TO_SEARCH,
            num_candidates=50,
            k=20
        )
        
        return result.get("answer", "No response generated")
        
    except Exception as e:
        logging.error(f"Error processing incident query: {e}")
        return f"Error processing query: {e}"
