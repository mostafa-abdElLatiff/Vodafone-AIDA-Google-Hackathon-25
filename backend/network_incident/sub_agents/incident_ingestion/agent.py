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

import logging
import pandas as pd
from typing import Tuple, Union
from google.adk.tools import FunctionTool
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

# Import your custom modules
try:
    from backend.network_incident.sub_agents.incident_ingestion.ingestion import (
        update_incidents_table, 
        convert_data_to_json, 
        generate_and_add_embeddings, 
        ingest_data_into_elasticsearch_index
    )
    from backend.network_incident.sub_agents.incident_ingestion.file_handler import (
        handle_file_upload, 
        validate_dataframe
    )
    from backend.network_incident.sub_agents.incident_ingestion import prompt
except ImportError as e:
    logging.error(f"Failed to import required modules: {e}")
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MODEL = "gemini-2.5-pro"


def ingest_incident_data(df: pd.DataFrame) -> str:
    """
    Transforms incident data, updates BigQuery, generates embeddings, and indexes into Elasticsearch.
    
    Args:
        df (pd.DataFrame): The incident data DataFrame.
        
    Returns:
        str: Detailed status message with counts.
        
    Raises:
        ValueError: If DataFrame is invalid or empty
        RuntimeError: If ingestion process fails
    """
    if df is None or df.empty:
        raise ValueError("DataFrame cannot be None or empty")
    
    try:
        logger.info("Starting ingestion process...")
        
        # Validate the DataFrame
        if not validate_dataframe(df):
            error_msg = "Invalid data format. Please ensure the file contains all required columns and valid data."
            logger.error(error_msg)
            return f"❌ Error: {error_msg}"
        
        total_records = len(df)
        logger.info(f"Processing {total_records} incident records...")
        
        # Step 1: Convert and enrich data
        try:
            json_data = convert_data_to_json(df)
        except Exception as e:
            logger.error(f"Failed to convert data to JSON: {e}")
            return f"❌ Data conversion failed: {str(e)}"

        # Step 2: Update BigQuery and get counts
        try:
            new_count, updated_count = update_incidents_table(json_data)
        except Exception as e:
            logger.error(f"Failed to update BigQuery: {e}")
            return f"❌ BigQuery update failed: {str(e)}"

        # Step 3: Generate embeddings
        try:
            enriched_data = generate_and_add_embeddings(json_data)
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return f"❌ Embedding generation failed: {str(e)}"

        # Step 4: Index into Elasticsearch
        try:
            es_success, es_failed = ingest_data_into_elasticsearch_index(enriched_data)
        except Exception as e:
            logger.error(f"Failed to index into Elasticsearch: {e}")
            return f"❌ Elasticsearch indexing failed: {str(e)}"

        # Prepare detailed status message
        status_message = (
            f"✅ Data ingestion completed successfully!\n\n"
            f"📊 **Summary:**\n"
            f"• Total records processed: {total_records}\n"
            f"• New incidents added: {new_count}\n"
            f"• Existing incidents updated: {updated_count}\n"
            f"• Elasticsearch documents indexed: {es_success}\n"
            f"• Elasticsearch failures: {es_failed}\n\n"
            f"🔍 **Database Updates:**\n"
            f"• BigQuery table updated with {new_count} new and {updated_count} updated records\n"
            f"• Elasticsearch index updated with {es_success} documents\n\n"
            f"✨ All data has been successfully ingested and is now available for search and resolution suggestions."
        )

        logger.info(f"Ingestion completed: {new_count} new, {updated_count} updated, {es_success} indexed")
        return status_message

    except Exception as e:
        logger.error(f"Unexpected error during ingestion: {e}")
        return f"❌ Unexpected ingestion error: {str(e)}"


def process_uploaded_file(file_content: Union[bytes, str], filename: str) -> str:
    """
    Process uploaded incident data files (CSV/Excel) and ingests them into the system.
    
    Args:
        file_content (Union[bytes, str]): The uploaded file content.
        filename (str): The name of the uploaded file.
        
    Returns:
        str: Status message.
        
    Raises:
        ValueError: If file content or filename is invalid
        RuntimeError: If file processing fails
    """
    if not filename or not file_content:
        raise ValueError("Both file_content and filename must be provided")
    
    try:
        logger.info(f"Processing uploaded file: {filename}")
        
        # Handle file upload and convert to DataFrame
        try:
            df = handle_file_upload(file_content, filename)
        except Exception as e:
            logger.error(f"Failed to handle file upload: {e}")
            return f"❌ File upload handling failed: {str(e)}"
        
        # Validate DataFrame was created successfully
        if df is None or df.empty:
            error_msg = f"No data found in file {filename} or file could not be processed"
            logger.error(error_msg)
            return f"❌ {error_msg}"
        
        # Use the existing ingestion function
        result = ingest_incident_data(df)
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error processing file {filename}: {e}")
        return f"❌ File processing failed: {str(e)}"


# Validation function for tool creation
def validate_tools():
    """Validate that all required functions are available"""
    required_functions = [
        update_incidents_table,
        convert_data_to_json,
        generate_and_add_embeddings,
        ingest_data_into_elasticsearch_index,
        handle_file_upload,
        validate_dataframe
    ]
    
    for func in required_functions:
        if not callable(func):
            raise RuntimeError(f"Required function {func.__name__} is not callable")


# Create the tool instances using the functions directly
try:
    validate_tools()
    ingest_tool = FunctionTool(ingest_incident_data)
    file_upload_tool = FunctionTool(process_uploaded_file)
    logger.info("Tools created successfully")
except Exception as e:
    logger.error(f"Failed to create tools: {e}")
    raise


# Validate that prompt module has the required attribute
if not hasattr(prompt, 'INCIDENT_INGESTION_PROMPT'):
    raise AttributeError("prompt module must have INCIDENT_INGESTION_PROMPT attribute")


incident_ingestion_agent = LlmAgent(
    name="incident_ingestion_agent",
    model=MODEL,
    description=(
        "This agent reads structured network incident logs from an Excel or CSV file, generates embeddings for each incident description, "
        "and stores them in a vector database along with relevant metadata. It is used to build a searchable knowledge base of past incidents. "
        "The agent can process both direct DataFrame input and uploaded files (CSV/Excel format)."
    ),
    instruction=prompt.INCIDENT_INGESTION_PROMPT,
    tools=[ingest_tool, file_upload_tool],
    output_key="ingestion_status"
)