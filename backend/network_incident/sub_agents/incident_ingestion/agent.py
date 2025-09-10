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
from . import prompt
import pandas as pd 

MODEL = "gemini-2.5-pro"


class IngestIncidentTool:
    """
    A custom tool that encapsulates the entire data ingestion pipeline.
    """
    name = "ingest_incident_data"
    description = "Transforms incident data, updates BigQuery, generates embeddings, and indexes into Elasticsearch."

    def __call__(self, df: pd.DataFrame) -> str:
        """
        The main callable method for the tool.
        """
        try:
            print("Starting ingestion process...")
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

# Instantiate the custom tool class and pass the instance directly to FunctionTool.
ingest_tool = FunctionTool(IngestIncidentTool())

incident_ingestion_agent = LlmAgent(
    name="incident_ingestion_agent",
    model=MODEL,
    description=(
        "This agent reads structured network incident logs from an Excel or CSV file, generates embeddings for each incident description, "
        "and stores them in a vector database along with relevant metadata. It is used to build a searchable knowledge base of past incidents."
    ),
    instruction=prompt.INCIDENT_INGESTION_PROMPT,
    tools=[ingest_tool],
    output_key="ingestion_status"
)
