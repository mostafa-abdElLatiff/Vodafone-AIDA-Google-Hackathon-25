# Data Fields Configs
DATA_FIELDS = ['incident_id', 'timestamp', 'severity', 'service_impact', 'incident_description', 'resolution_steps', 'root_cause']
FIELDS_TO_EMBED = ['incident_description', 'resolution_steps', 'root_cause', 'service_impact']

# Model Configs
LLM_NAME = 'gemini-2.5-flash'
EMBEDDINGS_MODEL_NAME = "text-embedding-005"

# Elasticsearch Configs
ELASTICSEARCH_HOST = "http://10.132.0.8:9200"
ELASTICSEARCH_USERNAME = "elastic"
ELASTICSEARCH_PASSWORD = "awsomepassword"
INDEX_NAME = "network_incidents"
ES_INDEX_NAME = 'network_incidents'  # Keep for backward compatibility

# Search Fields
KEYWORD_FIELDS_TO_SEARCH = ['incident_description', 'resolution_steps', 'root_cause', 'service_impact']
VECTOR_FIELDS_TO_SEARCH = ['incident_description_vector', 'resolution_steps_vector', 'root_cause_vector', 'service_impact_vector']

# GCP Configs
GCP_PROJECT_ID = "vodaf-aida25lcpm-205"
GCP_LOCATION = "europe-west1"

# BigQuery
DATASET_ID = 'aida_hackathon_team_5'
TABLE_ID = 'network_incidents'
