# Data Fields Cnofigs
DATA_FIELDS = ['incident_id', 'timestamp', 'severity', 'service_impact', 'incident_description', 'resolution_steps', 'root_cause']
FIELDS_TO_EMBED = ['incident_description', 'resolution_steps', 'root_cause', 'service_impact']


# Model Configs
LLM_NAME = 'gemini-2.5-flash'
EMBEDDINGS_MODEL_NAME = "text-embedding-005"

# Elasticsearch Configs
ES_INDEX_NAME = 'network_incidents'

# BigQuery
DATASET_ID = 'aida_hackathon-team5'
TABLE_ID = 'network-incidents'
