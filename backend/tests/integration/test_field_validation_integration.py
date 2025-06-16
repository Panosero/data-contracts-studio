#!/usr/bin/env python3
"""Integration test for the complete field validation solution."""

import requests
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


def test_api_integration():
    """Test the complete API integration with field validation."""

    base_url = "http://localhost:8000/api/v1"

    print("Testing API Integration with Enhanced Field Validation")
    print("=" * 60)

    try:
        # Test 1: Get all contracts (should work now)
        print("\n1. Testing GET /contracts/ (original failing endpoint)...")
        response = requests.get(f"{base_url}/contracts/", timeout=10)
        if response.status_code == 200:
            contracts = response.json()
            print(f"✓ SUCCESS: Retrieved {len(contracts)} contracts")
        else:
            print(f"✗ FAILED: Status {response.status_code}")
            return False

        # Test 2: Create contract with spaces in field names
        print("\n2. Testing contract creation with spaces in field names...")
        contract_data = {
            "name": "Integration Test Contract",
            "version": "1.0.0",
            "status": "active",
            "fields": [
                {
                    "name": "user name",
                    "type": "string",
                    "required": True,
                    "description": "User's full name with spaces",
                },
                {
                    "name": "email address",
                    "type": "string",
                    "required": True,
                    "description": "User's email address",
                },
            ],
        }

        response = requests.post(
            f"{base_url}/contracts/",
            json=contract_data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 201:
            created_contract = response.json()
            contract_id = created_contract["id"]
            print(f"✓ SUCCESS: Created contract {contract_id} with spaces in field names")

            # Verify field names were preserved
            field_names = [f["name"] for f in created_contract["fields"]]
            expected_names = ["user name", "email address"]
            if field_names == expected_names:
                print(f"✓ SUCCESS: Field names preserved correctly: {field_names}")
            else:
                print(f"✗ FAILED: Field names not preserved. Got: {field_names}")
                return False
        else:
            print(f"✗ FAILED: Status {response.status_code}, Response: {response.text}")
            return False

        # Test 3: Try to create contract with invalid field names (should fail)
        print("\n3. Testing contract creation with invalid field names...")
        invalid_contract_data = {
            "name": "Invalid Test Contract",
            "version": "1.0.0",
            "status": "active",
            "fields": [
                {
                    "name": "field{invalid}",
                    "type": "string",
                    "required": True,
                    "description": "This should be rejected",
                }
            ],
        }

        response = requests.post(
            f"{base_url}/contracts/",
            json=invalid_contract_data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 422:
            error_data = response.json()
            print("✓ SUCCESS: Invalid field names properly rejected")
            print(f"  Error message: {error_data.get('message', 'No message')}")
        else:
            print(f"✗ FAILED: Expected 422, got {response.status_code}")
            return False

        # Test 4: Test auto-generation endpoint
        print("\n4. Testing auto-generation with CSV data containing spaces...")
        csv_data = "user name,email address,age\nJohn Doe,john@example.com,30\nJane Smith,jane@example.com,25"

        auto_gen_data = {"source_type": "file", "source_data": csv_data}

        response = requests.post(
            f"{base_url}/contracts/auto-generate",
            json=auto_gen_data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 200:
            generated_fields = response.json()
            print(f"✓ SUCCESS: Generated {len(generated_fields)} fields from CSV")

            # Check if spaces are preserved in generated field names
            field_names = [f["name"] for f in generated_fields]
            if "user name" in field_names and "email address" in field_names:
                print("✓ SUCCESS: Spaces preserved in auto-generated field names")
            else:
                print(f"✗ FAILED: Spaces not preserved. Got field names: {field_names}")
                return False
        else:
            print(f"✗ FAILED: Status {response.status_code}, Response: {response.text}")
            return False

        print("\n" + "=" * 60)
        print("✓ ALL INTEGRATION TESTS PASSED!")
        print("✓ Original validation error fixed")
        print("✓ Spaces in field names now supported")
        print("✓ Invalid characters still properly rejected")
        print("✓ Auto-generation works with spaces")
        return True

    except requests.RequestException as e:
        print(f"\n✗ FAILED: Network error - {e}")
        print("Make sure the FastAPI server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"\n✗ FAILED: Unexpected error - {e}")
        return False


if __name__ == "__main__":
    success = test_api_integration()
    sys.exit(0 if success else 1)
