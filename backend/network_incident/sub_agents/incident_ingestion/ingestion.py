import logging
import json
from google.cloud import bigquery
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm
from langchain_google_vertexai import VertexAIEmbeddings
from configs.config import (
    DATA_FIELDS, 
    FIELDS_TO_EMBED, 
    EMBEDDINGS_MODEL_NAME, 
    ES_INDEX_NAME,
    ELASTICSEARCH_HOST,
    ELASTICSEARCH_USERNAME,
    ELASTICSEARCH_PASSWORD,
    DATASET_ID,
    TABLE_ID,
    GCP_PROJECT_ID,
    GCP_LOCATION
)

# Initialize Elasticsearch client
client = Elasticsearch(
    hosts=[ELASTICSEARCH_HOST],
    basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
)

# def validate_data_before_ingestion(data):

def update_incidents_table(incoming_data):
    """
    Updates BigQuery table with incoming incident data.
    Replaces existing records with same incident_id and inserts new records.
    
    Args:
        incoming_data (list): List of dictionaries containing incident data
        
    Returns:
        tuple: (new_count, updated_count) - counts of new and updated records
    """
    # Initialize BigQuery client
    client = bigquery.Client()

    # Reference to the BigQuery table
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID)

    # Fetch only the incident_id column from BigQuery for comparison
    query = f"""
    SELECT incident_id
    FROM `{GCP_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """
    existing_data = client.query(query).to_dataframe()

    # Extract the incident_id from the existing data as a set for fast lookup
    existing_ids = set(existing_data['incident_id'].tolist()) if not existing_data.empty else set()

    # Convert incoming data to DataFrame for easy manipulation
    incoming_df = pd.DataFrame(incoming_data)

    # Prepare lists for updates and inserts
    updates = []
    inserts = []

    for index, row in incoming_df.iterrows():
        incident_id = row['incident_id']
        if incident_id in existing_ids:
            # Prepare an update record
            updates.append(row.to_dict())
        else:
            # Prepare an insert record
            inserts.append(row.to_dict())
    
    # Updating existing records using MERGE statement
    if updates:
        logging.info(f"Updating {len(updates)} existing records...")
        
        # Create a temporary table for updates
        temp_table_id = f"{TABLE_ID}_temp_updates"
        temp_table_ref = client.dataset(DATASET_ID).table(temp_table_id)
        
        # Create temporary table with update data
        update_df = pd.DataFrame(updates)
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema=[
                bigquery.SchemaField("incident_id", "STRING"),
                bigquery.SchemaField("full_date", "STRING"),
                bigquery.SchemaField("year", "INTEGER"),
                bigquery.SchemaField("month", "INTEGER"),
                bigquery.SchemaField("month_name", "STRING"),
                bigquery.SchemaField("day", "INTEGER"),
                bigquery.SchemaField("day_name", "STRING"),
                bigquery.SchemaField("hour", "INTEGER"),
                bigquery.SchemaField("minute", "INTEGER"),
                bigquery.SchemaField("severity", "STRING"),
                bigquery.SchemaField("service_impact", "STRING"),
                bigquery.SchemaField("incident_description", "STRING"),
                bigquery.SchemaField("resolution_steps", "STRING"),
                bigquery.SchemaField("root_cause", "STRING"),
            ]
        )
        
        job = client.load_table_from_dataframe(update_df, temp_table_ref, job_config=job_config)
        job.result()  # Wait for the job to complete
        
        # Use MERGE to update existing records
        merge_query = f"""
        MERGE `{GCP_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` AS target
        USING `{GCP_PROJECT_ID}.{DATASET_ID}.{temp_table_id}` AS source
        ON target.incident_id = source.incident_id
        WHEN MATCHED THEN
        UPDATE SET
            full_date = source.full_date,
            year = source.year,
            month = source.month,
            month_name = source.month_name,
            day = source.day,
            day_name = source.day_name,
            hour = source.hour,
            minute = source.minute,
            severity = source.severity,
            service_impact = source.service_impact,
            incident_description = source.incident_description,
            resolution_steps = source.resolution_steps,
            root_cause = source.root_cause
        """
        
        client.query(merge_query).result()
        
        # Clean up temporary table
        client.delete_table(temp_table_ref)
        logging.info(f"Updated {len(updates)} existing records")

    # Inserting new records
    if inserts:
        logging.info(f"Inserting {len(inserts)} new records...")
        
        # Create a temporary table for inserts
        temp_table_id = f"{TABLE_ID}_temp_inserts"
        temp_table_ref = client.dataset(DATASET_ID).table(temp_table_id)
        
        # Create temporary table with insert data
        insert_df = pd.DataFrame(inserts)
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema=[
                bigquery.SchemaField("incident_id", "STRING"),
                bigquery.SchemaField("full_date", "STRING"),
                bigquery.SchemaField("year", "INTEGER"),
                bigquery.SchemaField("month", "INTEGER"),
                bigquery.SchemaField("month_name", "STRING"),
                bigquery.SchemaField("day", "INTEGER"),
                bigquery.SchemaField("day_name", "STRING"),
                bigquery.SchemaField("hour", "INTEGER"),
                bigquery.SchemaField("minute", "INTEGER"),
                bigquery.SchemaField("severity", "STRING"),
                bigquery.SchemaField("service_impact", "STRING"),
                bigquery.SchemaField("incident_description", "STRING"),
                bigquery.SchemaField("resolution_steps", "STRING"),
                bigquery.SchemaField("root_cause", "STRING"),
            ]
        )
        
        job = client.load_table_from_dataframe(insert_df, temp_table_ref, job_config=job_config)
        job.result()  # Wait for the job to complete
        
        # Use INSERT to add new records
        insert_query = f"""
        INSERT INTO `{GCP_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        SELECT * FROM `{GCP_PROJECT_ID}.{DATASET_ID}.{temp_table_id}`
        """
        
        client.query(insert_query).result()
        
        # Clean up temporary table
        client.delete_table(temp_table_ref)
        logging.info(f"Inserted {len(inserts)} new records")

    logging.info("BigQuery update process completed.")
    return len(inserts), len(updates)

def convert_data_to_json(data):
    # Make a copy to avoid modifying the original DataFrame
    df_prepared = data.copy()

    # Convert 'timestamp' column to datetime
    df_prepared['timestamp'] = pd.to_datetime(df_prepared['timestamp'])

    # Retain the full ISO 8601 formatted date in a new column
    df_prepared['full_date'] = df_prepared['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Extract date and time components
    df_prepared['year'] = df_prepared['timestamp'].dt.year
    df_prepared['month'] = df_prepared['timestamp'].dt.month
    df_prepared['month_name'] = df_prepared['timestamp'].dt.strftime('%B').lower()
    df_prepared['day'] = df_prepared['timestamp'].dt.day
    df_prepared['day_name'] = df_prepared['timestamp'].dt.strftime('%A').lower()
    df_prepared['hour'] = df_prepared['timestamp'].dt.hour
    df_prepared['minute'] = df_prepared['timestamp'].dt.minute

    # Lower string fields
    df_prepared['severity'] = df_prepared['severity'].lower()
    df_prepared['service_impact'] = df_prepared['service_impact'].lower()
    df_prepared['incident_description'] = df_prepared['incident_description'].lower()
    df_prepared['resolution_steps'] = df_prepared['resolution_steps'].lower()
    df_prepared['root_cause'] = df_prepared['root_cause'].lower()
    
    # Drop the original 'timestamp' column
    df_prepared = df_prepared.drop(columns=['timestamp'])
    
    # Convert DataFrame to a list of dictionaries
    return df_prepared.to_dict('records')


def generate_and_add_embeddings(json_data):
    """
    Generates and adds embeddings for specified text fields in a list of JSON-like objects.
    
    Args:
        json_data (list): A list of dictionaries (JSON-like objects).
        fields_to_embed (list): A list of field names to generate embeddings for.
    
    Returns:
        list: The original list of dictionaries with added embedding fields.
    """
    try:
        # Initialize the Vertex AI embedding model
        embeddings_model = VertexAIEmbeddings(
            model_name=EMBEDDINGS_MODEL_NAME,
            project=GCP_PROJECT_ID,
            location=GCP_LOCATION
        )
        
        for record in json_data:
            for field in FIELDS_TO_EMBED:
                if field in record and record[field]:
                    text_to_embed = record[field]
                    # Generate embedding for the field's text
                    embedding = embeddings_model.embed_query(text_to_embed)
                    
                    # Add a new field for the embedding
                    record[f'{field}_vector'] = embedding
        
        return json_data
        
    except Exception as e:
        logging.info(f"An error occurred while generating embeddings: {e}")
        return json_data


def ingest_data_into_elasticsearch_index(json_data):
    """
    Indexes data into Elasticsearch, handling both new documents and updates.
    
    Args:
        json_data (list): List of dictionaries containing incident data with embeddings
        
    Returns:
        tuple: (success_count, failed_count) - counts of successful and failed operations
    """
    # Prepare the data for bulk operations (both inserts and updates)
    actions = []
    
    for doc in json_data:
        # Use incident_id as the document ID for consistent updates
        doc_id = doc.get('incident_id')
        
        action = {
            "_index": ES_INDEX_NAME,
            "_id": doc_id,  # Use incident_id as document ID
            "_op_type": "index",  # This will insert or update the document
            "_source": doc,
        }
        actions.append(action)
    
    # Use helpers.bulk to insert/update the data with a progress bar
    logging.info("Starting bulk indexing/updating...")
    try:
        success, failed = helpers.bulk(
            client, 
            tqdm(actions, desc="Indexing/updating documents"),
            chunk_size=100,  # Process in chunks for better performance
            request_timeout=60  # Increase timeout for large batches
        )
        
        logging.info(f"Bulk indexing complete. {success} documents successfully processed.")
        if failed:
            logging.warning(f"{len(failed)} documents failed to process:")
            for item in failed:
                logging.warning(f"Failed document: {item}")
        
        return success, len(failed) if failed else 0
        
    except Exception as e:
        logging.error(f"An error occurred during Elasticsearch indexing: {e}")
        return 0, len(actions)
    