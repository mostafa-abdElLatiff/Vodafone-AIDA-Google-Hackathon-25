from google.cloud import aiplatform
import pandas as pd

# Initialize Vertex AI
aiplatform.init(project="vodaf-aida25lcpm-205", location="europe-west1")

# Load dataset
df = pd.read_excel("use_case_2_network_incident_logs.xlsx")

# Filter required columns
required_columns = [
    'incident_id', 'timestamp', 'severity', 'service_impact',
    'incident_description', 'resolution_steps', 'root_cause'
]
df = df.dropna(subset=required_columns)

# Load embedding model
embedding_model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

# Prepare data for indexing
documents = []
for _, row in df.iterrows():
    embedding = embedding_model.get_embeddings([row['incident_description']])[0].values
    metadata = {
        "incident_id": str(row["incident_id"]),
        "timestamp": str(row["timestamp"]),
        "severity": row["severity"],
        "service_impact": row["service_impact"],
        "resolution_steps": row["resolution_steps"],
        "root_cause": row["root_cause"]
    }
    documents.append({
        "id": str(row["incident_id"]),
        "embedding": embedding,
        "metadata": metadata
    })

# Upload to Vertex AI Vector Search
index = aiplatform.MatchingEngineIndex(index_name="network_incident_index")
index.upsert_datapoints(datapoints=documents)

print(f"Successfully ingested {len(documents)} incidents into Vertex AI Vector Search.")