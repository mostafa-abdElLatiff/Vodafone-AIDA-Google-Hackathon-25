# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from google.adk.tools import FunctionTool
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from .ingestion import update_incidents_table, convert_data_to_json, generate_and_add_embeddings, ingest_data_into_elasticsearch_index
from .file_handler import handle_file_upload, validate_dataframe
from . import prompt
import pandas as pd
import logging 

MODEL = "gemini-2.5-pro"


def ingest_incident_data(df: pd.DataFrame) -> str:
    """
    Transforms incident data, updates BigQuery, generates embeddings, and indexes into Elasticsearch.
    
    Args:
        df (pd.DataFrame): The incident data DataFrame.
        
    Returns:
        str: Status message.
    """
    try:
        logging.info("Starting ingestion process...")
        
        # Validate the DataFrame
        if not validate_dataframe(df):
            return "Error: Invalid data format. Please ensure the file contains all required columns and valid data."
        
        # Step 1: Convert and enrich data
        json_data = convert_data_to_json(df)

        # Step 2: Update BigQuery
        update_incidents_table(json_data)

        # Step 3: Generate embeddings
        enriched_data = generate_and_add_embeddings(json_data)

        # Step 4: Index into Elasticsearch
        ingest_data_into_elasticsearch_index(enriched_data)

        return f"Ingestion complete: {len(enriched_data)} records processed."

    except Exception as e:
        logging.error(f"Ingestion failed: {e}")
        return f"Ingestion failed: {e}"

def process_uploaded_file(file_content: bytes, filename: str) -> str:
    """
    Process uploaded incident data files (CSV/Excel) and ingests them into the system.
    
    Args:
        file_content (bytes): The uploaded file content.
        filename (str): The name of the uploaded file.
        
    Returns:
        str: Status message.
    """
    try:
        logging.info(f"Processing uploaded file: {filename}")
        
        # Handle file upload and convert to DataFrame
        df = handle_file_upload(file_content, filename)
        
        # Use the existing ingestion function
        result = ingest_incident_data(df)
        
        return result
        
    except Exception as e:
        logging.error(f"File processing failed: {e}")
        return f"File processing failed: {e}"

# Create the tool instances using the functions directly
ingest_tool = FunctionTool(ingest_incident_data)
file_upload_tool = FunctionTool(process_uploaded_file)

incident_ingestion_agent = LlmAgent(
    name="incident_ingestion_agent",
    model=MODEL,
    description=(
        "This agent reads structured network incident logs from an Excel or CSV file, generates embeddings for each incident description, "
        "and stores them in a vector database along with relevant metadata. It is used to build a searchable knowledge base of past incidents."
    ),
    instruction=prompt.INCIDENT_INGESTION_PROMPT,
    tools=[ingest_tool, file_upload_tool],
    output_key="ingestion_status"
)
