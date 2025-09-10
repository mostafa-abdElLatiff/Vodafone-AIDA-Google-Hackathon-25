"""
Example usage of the Network Incident Management System.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network_incident.inference import process_incident_query
from network_incident.sub_agents.incident_ingestion.agent import IngestIncidentTool
import pandas as pd

def example_query_processing():
    """Example of processing incident queries."""
    print("=== Example Query Processing ===")
    
    queries = [
        "4G network outage in London",
        "High packet loss in Manchester region",
        "DNS resolution issues affecting multiple sites",
        "Fiber cut causing service disruption"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        try:
            response = process_incident_query(query)
            print(f"Response: {response[:200]}...")
        except Exception as e:
            print(f"Error: {e}")

def example_data_ingestion():
    """Example of data ingestion."""
    print("\n=== Example Data Ingestion ===")
    
    # Create sample data
    sample_data = {
        'incident_id': ['INC001', 'INC002', 'INC003'],
        'timestamp': ['2024-01-15 10:30:00', '2024-01-15 14:45:00', '2024-01-15 16:20:00'],
        'severity': ['High', 'Medium', 'Low'],
        'service_impact': ['4G outage', 'Packet loss', 'DNS issues'],
        'incident_description': [
            '4G network completely down in London area',
            'High packet loss reported in Manchester region',
            'DNS resolution failures affecting multiple sites'
        ],
        'resolution_steps': [
            'Restart base station, check fiber connections',
            'Check router configurations, replace faulty equipment',
            'Update DNS server settings, clear cache'
        ],
        'root_cause': [
            'Fiber cut due to construction work',
            'Router hardware failure',
            'DNS server misconfiguration'
        ]
    }
    
    df = pd.DataFrame(sample_data)
    
    try:
        # Ingest data
        tool = IngestIncidentTool()
        result = tool(df)
        print(f"Ingestion result: {result}")
    except Exception as e:
        print(f"Ingestion error: {e}")

def main():
    """Run examples."""
    print("Network Incident Management System - Example Usage")
    print("=" * 60)
    
    # Note: These examples will only work if the system is properly configured
    # with Elasticsearch, BigQuery, and Google Cloud credentials
    
    print("\nNote: These examples require proper configuration of:")
    print("- Elasticsearch connection")
    print("- Google Cloud credentials")
    print("- BigQuery access")
    print("- Vertex AI access")
    
    # Uncomment these lines when the system is configured:
    # example_query_processing()
    # example_data_ingestion()
    
    print("\nTo test the system, run: python test_setup.py")

if __name__ == "__main__":
    main()
