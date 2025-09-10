"""
Deployment configuration for Network Incident Resolution Agent
"""

# GCP Configuration
GCP_PROJECT_ID = "vodaf-aida25lcpm-205"
GCP_LOCATION = "europe-west1"
GCP_BUCKET = "aida-hackathon-team-5"  # Replace with your actual bucket name

# Agent Configuration
AGENT_DISPLAY_NAME = "Network Incident Resolution Agent"
AGENT_DESCRIPTION = "AI-powered assistant for network incident resolution and data ingestion"

# Elasticsearch Configuration
ELASTICSEARCH_HOST = "http://10.132.0.8:9200"
ELASTICSEARCH_USERNAME = "elastic"
ELASTICSEARCH_PASSWORD = "awsomepassword"

# BigQuery Configuration
BIGQUERY_DATASET_ID = "aida_hackathon_team_5"
BIGQUERY_TABLE_ID = "network_incidents"

# Model Configuration
LLM_MODEL = "gemini-2.5-pro"
EMBEDDINGS_MODEL = "text-embedding-005"
