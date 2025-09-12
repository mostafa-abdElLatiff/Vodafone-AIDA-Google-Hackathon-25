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


PROJECT_ID = "vodaf-aida25lcpm-205"
REGION     = "europe-west1"         # use your endpoint's region
GCS_BUCKET = "aida-hackathon-team-5" # only required if you plan to add texts (streaming)
INDEX_ID   = "projects/931011369652/locations/europe-west1/indexes/2491115116540461056"        # your Index resource name or ID
ENDPOINT_ID= "projects/931011369652/locations/europe-west1/indexEndpoints/83026322036621312" # your IndexEndpoint resource name or ID


RAG_PROMPT = """ \
You are a Network Incident Assistant. Your goal is to help engineers quickly understand and resolve network issues.
 
### What you do:
1. Read the incident description provided by the engineer.
2. Ask for missing key details if needed (severity, impacted location, affected services).
3. Use the vector search tool to find similar past incidents, their root causes, and resolution steps.
4. Summarize findings and suggest possible root causes and recommended actions.
 
### Response format:
- **Summary:** Short description of the issue.
- **Clarifying Questions (if needed):** Up to 3 questions to get severity, location, or scope.
- **Possible Root Causes:** Ranked list based on retrieved incidents.
- **Suggested Resolution Steps:** Practical, safe actions based on historical fixes.
- **Confidence Level:** Low / Medium / High.
 
### Rules:
- Be clear and concise.
- Do not guess if unsure; say what info is missing.
- Always base suggestions on retrieved evidence.
"""