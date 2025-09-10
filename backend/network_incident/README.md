# Network Incident Management System

This module provides a comprehensive solution for managing network incidents using AI-powered retrieval and resolution suggestions.

## Architecture

The system consists of several key components:

### 1. Main Router Agent (`agent.py`)
- Routes incoming requests to appropriate sub-agents
- Handles both data ingestion and query processing

### 2. Incident Ingestion Agent (`sub_agents/incident_ingestion/`)
- Processes uploaded incident data files (CSV/Excel)
- Generates embeddings using Google Vertex AI
- Stores data in BigQuery and Elasticsearch
- Handles file uploads from frontend

### 3. Resolution Suggestion Agent (`sub_agents/resolution_suggestion/`)
- Processes natural language incident queries
- Performs hybrid search (keyword + semantic) using Elasticsearch
- Generates resolution suggestions based on historical data

### 4. Retrieval Module (`retrieval.py`)
- Implements Elasticsearch search functionality
- Supports hybrid search with both keyword and vector fields
- Formats search results for downstream processing

### 5. Inference Module (`inference.py`)
- Provides end-to-end inference pipeline
- Combines retrieval with LLM-based response generation
- Simple interface for query processing

### 6. API Module (`api.py`)
- FastAPI endpoints for frontend integration
- Handles file uploads and query processing
- RESTful interface for the system

## Configuration

All configuration is managed in `configs/config.py`:

- **Elasticsearch**: Connection details and index settings
- **Google Cloud**: Project ID, location, and model settings
- **Search Fields**: Keyword and vector fields for search
- **BigQuery**: Dataset and table configuration

## Usage

### 1. Data Ingestion
```python
from network_incident.sub_agents.incident_ingestion.agent import IngestIncidentTool
import pandas as pd

# Load your data
df = pd.read_csv('incidents.csv')

# Ingest data
tool = IngestIncidentTool()
result = tool(df)
print(result)
```

### 2. Query Processing
```python
from network_incident.inference import process_incident_query

# Process a query
query = "4G network outage in London"
response = process_incident_query(query)
print(response)
```

### 3. API Usage
```bash
# Start the API server
python -m network_incident.api

# Query incidents
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "network outage in London"}'

# Upload data
curl -X POST "http://localhost:8000/upload" \
     -F "file=@incidents.csv"
```

## Testing

Run the test script to verify setup:

```bash
python test_setup.py
```

This will test:
- Elasticsearch connection
- Search functionality
- Inference pipeline

## Dependencies

See `requirements.txt` for all required packages. Key dependencies:
- FastAPI for API endpoints
- Elasticsearch for search functionality
- LangChain for LLM integration
- Google Cloud libraries for BigQuery and Vertex AI
- Pandas for data processing

## File Structure

```
network_incident/
├── agent.py                 # Main router agent
├── retrieval.py            # Elasticsearch search functionality
├── inference.py            # End-to-end inference pipeline
├── api.py                  # FastAPI endpoints
├── prompt.py               # Main agent prompts
├── sub_agents/
│   ├── incident_ingestion/
│   │   ├── agent.py        # Ingestion agent
│   │   ├── ingestion.py    # Data processing functions
│   │   ├── file_handler.py # File upload handling
│   │   └── prompt.py       # Ingestion prompts
│   └── resolution_suggestion/
│       ├── agent.py        # Resolution agent
│       ├── retrieval_tool.py # Search tool
│       └── prompt.py       # Resolution prompts
└── README.md               # This file
```
