import logging
import json
from google.cloud import bigquery
import pandas as pd
from configs.config import DATA_FIELDS, FIELDS_TO_EMBED, EMBEDDINGS_MODEL_NAME, ES_INDEX_NAME

# def validate_data_before_ingestion(data):

def update_incidents_table(incoming_data):
    # Initialize BigQuery client
    client = bigquery.Client()

    # Reference to the BigQuery table
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID)

    # Fetch only the incident_id column from BigQuery for comparison
    query = f"""
    SELECT incident_id
    FROM `{DATASET_ID}.{TABLE_ID}`
    """
    existing_data = client.query(query).to_dataframe()

    # Extract the incident_id from the existing data as a set for fast lookup
    existing_ids = set(existing_data['incident_id'].tolist())

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
    
    # Updating existing records
    for update in updates:
        update_query = f"""
        UPDATE `{DATASET_ID}.{TABLE_ID}`
        SET
            timestamp = '{update['timestamp']}',
            severity = '{update['severity']}',
            service_impact = '{update['service_impact']}',
            incident_description = '{update['incident_description']}',
            resolution_steps = '{update['resolution_steps']}',
            root_cause = '{update['root_cause']}'
        WHERE incident_id = '{update['incident_id']}'
        """
        client.query(update_query)
        print(f"Updated incident {update['incident_id']}")

    # Inserting new records
    if inserts:
        # You can use BigQuery's insert method or load the data in bulk
        rows_to_insert = [tuple(row.values()) for row in inserts]
        insert_query = f"""
        INSERT INTO `{DATASET_ID}.{TABLE_ID}` (incident_id, timestamp, severity, service_impact, incident_description, resolution_steps, root_cause)
        VALUES
        """
        insert_query += ",".join([str(row) for row in rows_to_insert])
        client.query(insert_query)
        print(f"Inserted {len(inserts)} new records")

    print("Process completed.")

def convert_data_to_json(data):
    # Make a copy to avoid modifying the original DataFrame
    df_prepared = df.copy()

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
        embeddings_model = VertexAIEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
        
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
    # Prepare the data for bulk insertion
    actions = [
        {
            "_index": ES_INDEX_NAME,
            "_source": doc,
        }
        for doc in json_data
    ]
    
    # Use helpers.bulk to insert the data with a progress bar
    logging.info("Starting bulk insertion...")
    try:
        success, failed = helpers.bulk(client, tqdm(actions, desc="Inserting documents"))
        logging.info(f"Bulk insertion complete. {success} documents successfully inserted.")
        if failed:
            logging.info(f"{len(failed)} documents failed to insert:")
            for item in failed:
                logging.info(item)
    except Exception as e:
        logging.info(f"An error occurred: {e}")
    