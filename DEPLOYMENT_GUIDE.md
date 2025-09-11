# Network Incident Resolution Agent - Deployment Guide

## Overview
This guide will help you deploy the Network Incident Resolution Agent and connect it to your frontend application running on Cloud Run.

## Prerequisites

1. **GCP Project Setup**:
   - Project ID: `vodaf-aida25lcpm-205`
   - Location: `europe-west1`
   - Ensure you have the necessary permissions for Agent Engines

2. **Required Services**:
   - Vertex AI Agent Engines
   - Cloud Storage (for staging)
   - BigQuery
   - Elasticsearch (already configured)

3. **Authentication**:
   - Ensure you're authenticated with GCP
   - Set up Application Default Credentials

## Step 1: Deploy the Agent

### Option A: Using the deployment script (Recommended)
```bash
python deploy_agent.py deploy
```

### Option B: Using the quick deploy script
```bash
./deploy.sh
```

### Option C: Manual deployment
```bash
cd deployment
python deploy.py --create --project_id=vodaf-aida25lcpm-205 --location=europe-west1 --bucket=aida-hackathon-team-5
```

## Step 2: Get the Agent Endpoint

After deployment, you'll receive an output like:
```
Created remote agent: projects/vodaf-aida25lcpm-205/locations/europe-west1/agentEngines/1234567890
```

**Important**: Note the agent endpoint URL - you'll need this for the frontend connection.

## Step 3: Update Frontend Configuration

### Update the agent client in `frontend/agent_client.py`:

```python
# Replace the LocalAgentClient with AgentClient
from agent_client import AgentClient

# In your app.py, change:
# st.session_state.agent_client = LocalAgentClient()
# to:
st.session_state.agent_client = AgentClient(
    project_id="vodaf-aida25lcpm-205",
    location="europe-west1",
    agent_endpoint="YOUR_AGENT_ENDPOINT_URL"  # Replace with actual endpoint
)
```

## Step 4: Redeploy Frontend to Cloud Run

```bash
# Build and deploy your frontend
gcloud run deploy network-incident-frontend \
  --source frontend \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
```

## Step 5: Test the Connection

1. **Upload Data**: Use the sidebar to upload a CSV/Excel file
2. **Trigger Ingestion**: Type "ingest this data" in the chat
3. **Test Resolution**: Ask questions like "How to resolve 4G outage issues?"

## Configuration Files

### Environment Variables
Create a `.env` file in the backend directory:
```env
GOOGLE_CLOUD_PROJECT=vodaf-aida25lcpm-205
GOOGLE_CLOUD_LOCATION=europe-west1
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
```

### Agent Configuration
The agent is configured with:
- **Model**: `gemini-2.5-pro`
- **Sub-agents**: Ingestion and Resolution
- **Dependencies**: All required packages for BigQuery, Elasticsearch, etc.

## Troubleshooting

### Common Issues:

1. **Permission Denied**:
   - Ensure you have `Vertex AI Agent Engines Admin` role
   - Check that the project has the necessary APIs enabled

2. **Deployment Fails**:
   - Verify all dependencies are in `requirements.txt`
   - Check that the bucket exists and is accessible
   - Ensure the project ID and location are correct

3. **Frontend Connection Issues**:
   - Verify the agent endpoint URL is correct
   - Check that the agent is deployed and running
   - Ensure CORS is properly configured

4. **Data Ingestion Issues**:
   - Verify BigQuery permissions
   - Check Elasticsearch connectivity
   - Ensure the data format matches expected schema

### Debugging Commands:

```bash
# Test deployment setup
python deploy_agent.py test

# List deployed agents
python deploy_agent.py list

# Delete an agent (if needed)
python deploy_agent.py delete --resource-id=YOUR_RESOURCE_ID

# Test local agent
cd frontend
python -c "from agent_client import LocalAgentClient; client = LocalAgentClient(); print(client.predict('test query'))"
```

## Architecture

```
Frontend (Cloud Run) 
    ↓ HTTP/API calls
Network Incident Agent (Vertex AI Agent Engines)
    ↓ Routes to
├── Ingestion Agent
│   ├── BigQuery (Data Storage)
│   └── Elasticsearch (Search Index)
└── Resolution Agent
    ├── Elasticsearch (Search)
    └── LLM (Response Generation)
```

## Monitoring

- **Agent Logs**: Check Vertex AI Agent Engines logs in GCP Console
- **Frontend Logs**: Check Cloud Run logs
- **BigQuery**: Monitor data ingestion in BigQuery console
- **Elasticsearch**: Check index status and search performance

## Security Considerations

1. **Authentication**: Ensure proper IAM roles are assigned
2. **Data Privacy**: Data is processed within your GCP project
3. **Network Security**: Use VPC if required for Elasticsearch access
4. **API Security**: Consider adding authentication to the agent endpoint

## Cost Optimization

1. **Agent Scaling**: Configure appropriate scaling parameters
2. **Data Storage**: Monitor BigQuery and Elasticsearch storage costs
3. **Compute**: Use appropriate machine types for your workload

## Support

If you encounter issues:
1. Check the logs in GCP Console
2. Verify all configuration settings
3. Test with sample data first
4. Contact the development team for assistance

---

**Note**: This deployment creates a production-ready system. Make sure to test thoroughly before using with real data.
