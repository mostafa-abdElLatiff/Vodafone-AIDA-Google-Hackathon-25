"""
Test script to verify the ingestion agent functionality.
"""

import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ingestion_functionality():
    """Test the ingestion agent with sample data."""
    try:
        print("Testing ingestion functionality...")
        
        # Load sample data
        sample_file = "network_incident/sub_agents/incident_ingestion/network_incident_qa_50_pairs_with_suggestions.csv"
        df = pd.read_csv(sample_file)
        
        print(f"✅ Loaded sample data with {len(df)} records")
        print(f"Columns: {list(df.columns)}")
        
        # Test data validation
        from network_incident.sub_agents.incident_ingestion.file_handler import validate_dataframe
        is_valid = validate_dataframe(df)
        print(f"✅ Data validation: {'PASSED' if is_valid else 'FAILED'}")
        
        if not is_valid:
            print("❌ Sample data doesn't meet validation requirements")
            return False
        
        # Test data conversion
        from network_incident.sub_agents.incident_ingestion.ingestion import convert_data_to_json
        json_data = convert_data_to_json(df)
        print(f"✅ Data conversion: {len(json_data)} records converted to JSON")
        
        # Test that required fields are present
        required_fields = ['incident_id', 'full_date', 'year', 'month', 'severity', 'service_impact', 'incident_description']
        sample_record = json_data[0]
        missing_fields = [field for field in required_fields if field not in sample_record]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        else:
            print("✅ All required fields present in converted data")
        
        print("\n🎉 Ingestion functionality test completed successfully!")
        print("Note: This test only validates data processing, not actual database operations.")
        return True
        
    except Exception as e:
        print(f"❌ Ingestion test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_imports():
    """Test that all ingestion agent components can be imported."""
    try:
        print("Testing ingestion agent imports...")
        
        from network_incident.sub_agents.incident_ingestion.agent import (
            incident_ingestion_agent, 
            ingest_tool, 
            file_upload_tool
        )
        print("✅ Ingestion agent imported successfully")
        
        from network_incident.sub_agents.incident_ingestion.ingestion import (
            update_incidents_table,
            convert_data_to_json,
            generate_and_add_embeddings,
            ingest_data_into_elasticsearch_index
        )
        print("✅ Ingestion functions imported successfully")
        
        from network_incident.sub_agents.incident_ingestion.file_handler import (
            handle_file_upload,
            validate_dataframe
        )
        print("✅ File handler functions imported successfully")
        
        print("✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all ingestion tests."""
    print("Testing Network Incident Ingestion System...")
    print("=" * 50)
    
    tests = [
        ("Agent Imports", test_agent_imports),
        ("Ingestion Functionality", test_ingestion_functionality)
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
        print("🎉 All ingestion tests passed! System is ready.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()
