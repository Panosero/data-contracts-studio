#!/usr/bin/env python3
"""
Test script to debug auto-generation service
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.auto_generation_service import AutoGenerationService

def test_database_schema():
    print("=== Testing Database Schema Generation ===")
    schema = """CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""
    
    print(f"Input schema:\n{schema}\n")
    
    fields = AutoGenerationService.generate_from_database_schema(schema, "users")
    print(f"Generated {len(fields)} fields:")
    for field in fields:
        print(f"  - {field.name}: {field.type} (required: {field.required})")
    
    return fields

def test_api_response():
    print("\n=== Testing API Response Generation ===")
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
    
    print(f"Input JSON:\n{api_response}\n")
    
    fields = AutoGenerationService.generate_from_api_response(api_response)
    print(f"Generated {len(fields)} fields:")
    for field in fields:
        print(f"  - {field.name}: {field.type} (required: {field.required})")
    
    return fields

def test_csv_data():
    print("\n=== Testing CSV Data Generation ===")
    csv_data = """name,age,email,active
John Doe,30,john@example.com,true
Jane Smith,25,jane@example.com,false
Bob Johnson,35,bob@example.com,true"""
    
    print(f"Input CSV:\n{csv_data}\n")
    
    fields = AutoGenerationService.generate_from_csv_data(csv_data)
    print(f"Generated {len(fields)} fields:")
    for field in fields:
        print(f"  - {field.name}: {field.type} (required: {field.required})")
    
    return fields

if __name__ == "__main__":
    db_fields = test_database_schema()
    api_fields = test_api_response()
    csv_fields = test_csv_data()
    
    print(f"\n=== Summary ===")
    print(f"Database schema: {len(db_fields)} fields")
    print(f"API response: {len(api_fields)} fields")
    print(f"CSV data: {len(csv_fields)} fields")
