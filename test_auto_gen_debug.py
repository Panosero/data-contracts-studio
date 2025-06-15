#!/usr/bin/env python3
"""Test script to debug auto-generation service."""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.auto_generation_service import AutoGenerationService

def test_database_schema():
    """Test database schema parsing."""
    print("=== Testing Database Schema Parsing ===")
    
    schema = """CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""
    
    print(f"Input schema:\n{schema}\n")
    
    try:
        fields = AutoGenerationService.generate_from_database_schema(schema, "users")
        print(f"Generated {len(fields)} fields:")
        for field in fields:
            print(f"  - {field.name}: {field.type} (required: {field.required})")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_api_response():
    """Test API response parsing."""
    print("\n=== Testing API Response Parsing ===")
    
    api_response = """{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "profile": {
    "age": 30,
    "city": "New York"
  },
  "orders": [
    {
      "id": 1,
      "total": 99.99,
      "date": "2023-01-01"
    }
  ]
}"""
    
    print(f"Input API response:\n{api_response}\n")
    
    try:
        fields = AutoGenerationService.generate_from_api_response(api_response)
        print(f"Generated {len(fields)} fields:")
        for field in fields:
            print(f"  - {field.name}: {field.type} (required: {field.required})")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_csv_data():
    """Test CSV data parsing."""
    print("\n=== Testing CSV Data Parsing ===")
    
    csv_data = """name,age,email,active
John Doe,30,john@example.com,true
Jane Smith,25,jane@example.com,false
Bob Johnson,35,bob@example.com,true"""
    
    print(f"Input CSV data:\n{csv_data}\n")
    
    try:
        fields = AutoGenerationService.generate_from_csv_data(csv_data)
        print(f"Generated {len(fields)} fields:")
        for field in fields:
            print(f"  - {field.name}: {field.type} (required: {field.required})")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_schema()
    test_api_response()
    test_csv_data()
