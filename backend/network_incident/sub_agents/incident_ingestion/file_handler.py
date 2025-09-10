"""
File upload handler for incident ingestion.
"""

import pandas as pd
import logging
from typing import Union
import io

def handle_file_upload(file_content: bytes, filename: str) -> pd.DataFrame:
    """
    Handles file upload from frontend and converts to DataFrame.
    
    Args:
        file_content (bytes): The uploaded file content.
        filename (str): The name of the uploaded file.
        
    Returns:
        pd.DataFrame: Processed data as DataFrame.
        
    Raises:
        ValueError: If file format is not supported.
    """
    try:
        # Determine file type based on extension
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'csv':
            # Read CSV file
            df = pd.read_csv(io.BytesIO(file_content))
        elif file_extension in ['xlsx', 'xls']:
            # Read Excel file
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Validate required columns
        required_columns = ['incident_id', 'timestamp', 'severity', 'service_impact', 
                          'incident_description', 'resolution_steps', 'root_cause']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        logging.info(f"Successfully processed file {filename} with {len(df)} rows")
        return df
        
    except Exception as e:
        logging.error(f"Error processing file {filename}: {e}")
        raise

def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Validates that the DataFrame has the required structure and data.
    
    Args:
        df (pd.DataFrame): The DataFrame to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        # Check for required columns
        required_columns = ['incident_id', 'timestamp', 'severity', 'service_impact', 
                          'incident_description', 'resolution_steps', 'root_cause']
        
        if not all(col in df.columns for col in required_columns):
            return False
        
        # Check for empty DataFrame
        if df.empty:
            return False
        
        # Check for null values in critical columns
        critical_columns = ['incident_id', 'incident_description']
        if df[critical_columns].isnull().any().any():
            return False
        
        return True
        
    except Exception as e:
        logging.error(f"Error validating DataFrame: {e}")
        return False
