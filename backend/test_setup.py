"""
Test script to verify the network incident system setup.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network_incident.retrieval import search_network_incidents, format_search_results
from network_incident.inference import process_incident_query
from configs.config import (
    ELASTICSEARCH_HOST,
    ELASTICSEARCH_USERNAME,
    ELASTICSEARCH_PASSWORD,
    INDEX_NAME,
    KEYWORD_FIELDS_TO_SEARCH,
    VECTOR_FIELDS_TO_SEARCH
)

def test_elasticsearch_connection():
    """Test Elasticsearch connection."""
    try:
        from elasticsearch import Elasticsearch
        
        client = Elasticsearch(
            hosts=[ELASTICSEARCH_HOST],
            basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
        )
        
        if client.ping():
            print("✅ Elasticsearch connection successful")
            return True
        else:
            print("❌ Elasticsearch connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Elasticsearch connection error: {e}")
        return False

def test_search_functionality():
    """Test search functionality."""
    try:
        query = "network outage"
        
        # Test search
        results = search_network_incidents(
            user_query=query,
            keyword_fields=KEYWORD_FIELDS_TO_SEARCH,
            vector_fields=VECTOR_FIELDS_TO_SEARCH,
            k=5
        )
        
        if results:
            formatted = format_search_results(results)
            print(f"✅ Search successful, found {len(formatted)} results")
            return True
        else:
            print("❌ Search returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def test_inference():
    """Test inference functionality."""
    try:
        query = "4G network outage in London"
        result = process_incident_query(query)
        
        if result and "Error" not in result:
            print("✅ Inference successful")
            print(f"Response: {result[:100]}...")
            return True
        else:
            print(f"❌ Inference failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Inference error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Network Incident System Setup...")
    print("=" * 50)
    
    tests = [
        ("Elasticsearch Connection", test_elasticsearch_connection),
        ("Search Functionality", test_search_functionality),
        ("Inference", test_inference)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"  Test failed: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")

if __name__ == "__main__":
    main()
