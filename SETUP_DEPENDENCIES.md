# Setup Dependencies for Network Incident Resolution Agent

## Required Dependencies

To deploy and run the Network Incident Resolution Agent, you need to install the following dependencies:

### 1. Google ADK and AI Platform Dependencies

```bash
# Install Google ADK (Agent Development Kit)
pip install google-adk

# Install Google Cloud AI Platform
pip install google-cloud-aiplatform

# Install Google Generative AI
pip install google-genai

# Install additional Google Cloud dependencies
pip install google-cloud-bigquery
```

### 2. Data Processing Dependencies

```bash
# Install pandas (if not already installed)
pip install pandas

# Install numpy (if not already installed)
pip install numpy
```

### 3. Search and Embeddings Dependencies

```bash
# Install Elasticsearch client
pip install elasticsearch

# Install LangChain for Google Vertex AI
pip install langchain-google-vertexai

# Install progress bar
pip install tqdm
```

### 4. Utility Dependencies

```bash
# Install Pydantic for data validation
pip install pydantic

# Install python-dotenv for environment variables
pip install python-dotenv

# Install absl-py for command line flags
pip install absl-py
```

## Complete Installation Command

You can install all dependencies at once:

```bash
pip install google-adk google-cloud-aiplatform google-genai google-cloud-bigquery pandas numpy elasticsearch langchain-google-vertexai tqdm pydantic python-dotenv absl-py
```

## Alternative: Using requirements.txt

If you prefer to use a requirements file, create one with the above dependencies:

```bash
pip install -r requirements.txt
```

## Verification

After installing the dependencies, test the setup:

```bash
python deploy_agent.py test
```

## Troubleshooting

### Common Issues:

1. **Pandas Version Conflicts**:
   - If you get pandas import errors, try: `pip install --upgrade pandas`

2. **Google ADK Not Found**:
   - Ensure you're using the correct Python environment
   - Try: `pip install --upgrade google-adk`

3. **Permission Issues**:
   - On Windows, you might need to run as Administrator
   - On Linux/Mac, you might need `sudo pip install`

4. **Virtual Environment**:
   - It's recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install [dependencies]
   ```

## Environment Setup

Make sure you have the following environment variables set:

```bash
export GOOGLE_CLOUD_PROJECT="vodaf-aida25lcpm-205"
export GOOGLE_CLOUD_LOCATION="europe-west1"
export GOOGLE_CLOUD_STORAGE_BUCKET="aida-hackathon-team-5"
```

Or create a `.env` file in the project root:

```env
GOOGLE_CLOUD_PROJECT=vodaf-aida25lcpm-205
GOOGLE_CLOUD_LOCATION=europe-west1
GOOGLE_CLOUD_STORAGE_BUCKET=aida-hackathon-team-5
```

## Next Steps

Once all dependencies are installed:

1. Test the setup: `python deploy_agent.py test`
2. Deploy the agent: `python deploy_agent.py deploy`
3. Connect your frontend to the deployed agent

## Support

If you encounter issues:
1. Check the error messages carefully
2. Ensure all dependencies are installed
3. Verify your GCP credentials are set up
4. Check that your project has the necessary APIs enabled
