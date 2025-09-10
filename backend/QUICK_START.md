# Quick Start Guide

## Fixed Issues

The main issue was with the tool definition. The ADK framework expects functions to have a `__name__` attribute, but class instances don't have this attribute. I've fixed this by:

1. **Converting class-based tools to function-based tools** - This ensures compatibility with ADK
2. **Fixing import paths** - Using relative imports where appropriate
3. **Ensuring proper tool instantiation** - Using `FunctionTool(function)` instead of `FunctionTool(Class())`

## How to Use

### 1. Test the System
```bash
cd backend
python test_complete_system.py
```

### 2. Run the ADK Agent
```bash
adk run backend.network_incident.agent:root_agent
```

### 3. Test with a Query
When the agent is running, try:
```
What is the resolution for 4g outage?
```

## System Architecture

- **Main Agent** (`network_incident`): Routes queries to appropriate sub-agents
- **Ingestion Agent**: Processes uploaded incident data files
- **Resolution Agent**: Searches for similar incidents and provides resolution suggestions
- **Retrieval Tool**: Performs Elasticsearch hybrid search

## Key Files

- `backend/network_incident/agent.py` - Main router agent
- `backend/network_incident/retrieval.py` - Elasticsearch search functionality
- `backend/network_incident/sub_agents/resolution_suggestion/retrieval_tool.py` - Search tool
- `backend/network_incident/sub_agents/incident_ingestion/agent.py` - Data ingestion tools

## Configuration

All configuration is in `configs/config.py`:
- Elasticsearch connection details
- Google Cloud project settings
- Search field definitions

## Troubleshooting

If you encounter issues:

1. **Import errors**: Make sure you're running from the correct directory
2. **Tool errors**: Check that all functions are properly defined
3. **Connection errors**: Verify Elasticsearch and Google Cloud credentials

## Next Steps

1. Ensure Elasticsearch is running and accessible
2. Set up Google Cloud credentials
3. Test with sample data
4. Integrate with frontend
