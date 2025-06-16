"""Comprehensive unit tests for auto-generation service functionality.

This module provides comprehensive test coverage for all auto-generation methods
to meet the 80% coverage requirement.
"""

import json
import pytest
from app.services.auto_generation_service import AutoGenerationService


class TestAutoGenerationServiceComprehensive:
    """Comprehensive test suite for AutoGenerationService functionality."""

    def test_generate_from_database_schema_basic(self) -> None:
        """Test basic database schema generation."""
        schema_sql = """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            age INTEGER,
            created_at TIMESTAMP
        );
        """

        result = AutoGenerationService.generate_from_database_schema(schema_sql, "users")

        assert isinstance(result, list)
        assert len(result) > 0

        # Check that field names are present
        field_names = [field.name for field in result]
        expected_fields = ["id", "name", "email", "age", "created_at"]

        for expected_field in expected_fields:
            assert expected_field in field_names or any(expected_field in name for name in field_names)

    def test_generate_from_database_schema_empty(self) -> None:
        """Test database schema generation with empty input."""
        result = AutoGenerationService.generate_from_database_schema("", "table")
        assert result == []

    def test_generate_from_database_schema_comments(self) -> None:
        """Test database schema generation with comments."""
        schema_sql = """
        -- This is a comment
        CREATE TABLE products (
            # Another comment
            product_id INTEGER,
            product_name VARCHAR(100)
        );
        """

        result = AutoGenerationService.generate_from_database_schema(schema_sql, "products")
        assert isinstance(result, list)

    def test_generate_from_api_response_basic(self) -> None:
        """Test API response field generation."""
        api_response = json.dumps(
            {
                "user_id": 123,
                "username": "john_doe",
                "email": "john@example.com",
                "is_active": True,
                "balance": 99.99,
                "tags": ["user", "premium"],
                "metadata": {"role": "admin", "department": "IT"},
            }
        )

        result = AutoGenerationService.generate_from_api_response(api_response)

        assert isinstance(result, list)
        assert len(result) > 0

        field_names = [field.name for field in result]
        assert "user_id" in field_names
        assert "username" in field_names
        assert "email" in field_names

    def test_generate_from_api_response_invalid_json(self) -> None:
        """Test API response generation with invalid JSON."""
        with pytest.raises(ValueError, match="Invalid JSON format"):
            AutoGenerationService.generate_from_api_response("invalid json")

    def test_generate_from_api_response_array(self) -> None:
        """Test API response generation with JSON array."""
        api_response = json.dumps([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob", "age": 30}])

        result = AutoGenerationService.generate_from_api_response(api_response)
        assert isinstance(result, list)

    def test_generate_from_csv_data_basic(self) -> None:
        """Test CSV data field generation."""
        csv_data = """id,name,email,age
1,John Doe,john@example.com,25
2,Jane Smith,jane@example.com,30
3,Bob Johnson,bob@example.com,35"""

        result = AutoGenerationService.generate_from_csv_data(csv_data)

        assert isinstance(result, list)
        assert len(result) == 4  # id, name, email, age

        field_names = [field.name for field in result]
        assert "id" in field_names
        assert "name" in field_names
        assert "email" in field_names
        assert "age" in field_names

    def test_generate_from_csv_data_empty(self) -> None:
        """Test CSV generation with empty data."""
        result = AutoGenerationService.generate_from_csv_data("")
        assert result == []

    def test_generate_from_csv_data_json_array(self) -> None:
        """Test CSV generation with JSON array input."""
        json_array = json.dumps(
            [
                {"product_id": 1, "product_name": "Widget", "price": 19.99},
                {"product_id": 2, "product_name": "Gadget", "price": 29.99},
            ]
        )

        result = AutoGenerationService.generate_from_csv_data(json_array)
        assert isinstance(result, list)

    def test_generate_from_csv_data_json_object(self) -> None:
        """Test CSV generation with single JSON object."""
        json_object = json.dumps(
            {"order_id": 12345, "customer_name": "Alice Johnson", "total": 155.50, "status": "completed"}
        )

        result = AutoGenerationService.generate_from_csv_data(json_object)
        assert isinstance(result, list)

    def test_generate_from_csv_data_with_quotes(self) -> None:
        """Test CSV with quoted values."""
        csv_data = '''product_id,"product name","description with, comma"
1,"Super Widget","A great widget, very useful"
2,"Mega Gadget","Another gadget, super cool"'''

        result = AutoGenerationService.generate_from_csv_data(csv_data)
        assert isinstance(result, list)
        assert len(result) >= 3

    def test_generate_from_csv_data_empty_headers(self) -> None:
        """Test CSV with some empty headers."""
        csv_data = """id,,name,
1,,John,
2,,Jane,"""

        result = AutoGenerationService.generate_from_csv_data(csv_data)
        # Should skip empty headers
        field_names = [field.name for field in result]
        assert "id" in field_names
        assert "name" in field_names
        # Should not have fields for empty headers
        assert len([name for name in field_names if not name.strip()]) == 0

    def test_infer_type_from_samples_integer(self) -> None:
        """Test type inference for integer values."""
        samples = ["1", "2", "3", "123", "0"]
        result = AutoGenerationService._infer_type_from_samples(samples)
        assert result == "integer"

    def test_infer_type_from_samples_number(self) -> None:
        """Test type inference for float/number values."""
        samples = ["1.5", "2.0", "3.14", "0.5"]
        result = AutoGenerationService._infer_type_from_samples(samples)
        assert result == "number"

    def test_infer_type_from_samples_boolean(self) -> None:
        """Test type inference for boolean values."""
        samples = ["true", "false", "True", "False"]
        result = AutoGenerationService._infer_type_from_samples(samples)
        assert result == "boolean"

    def test_infer_type_from_samples_string(self) -> None:
        """Test type inference for string values."""
        samples = ["hello", "world", "test string", "another"]
        result = AutoGenerationService._infer_type_from_samples(samples)
        assert result == "string"

    def test_infer_type_from_samples_mixed(self) -> None:
        """Test type inference for mixed values."""
        samples = ["hello", "123", "true", "3.14"]
        result = AutoGenerationService._infer_type_from_samples(samples)
        assert result == "string"

    def test_infer_type_from_samples_empty(self) -> None:
        """Test type inference for empty samples."""
        result = AutoGenerationService._infer_type_from_samples([])
        assert result == "string"

    def test_parse_sql_field_integer(self) -> None:
        """Test SQL field parsing for integer types."""
        result = AutoGenerationService._parse_sql_field("user_id INTEGER PRIMARY KEY")
        assert result is not None
        assert result.name == "user_id"
        assert result.type == "integer"

    def test_parse_sql_field_varchar(self) -> None:
        """Test SQL field parsing for varchar types."""
        result = AutoGenerationService._parse_sql_field("name VARCHAR(255) NOT NULL")
        assert result is not None
        assert result.name == "name"
        assert result.type == "string"

    def test_parse_sql_field_timestamp(self) -> None:
        """Test SQL field parsing for timestamp types."""
        result = AutoGenerationService._parse_sql_field("created_at TIMESTAMP")
        assert result is not None
        assert result.name == "created_at"
        assert result.type == "datetime"

    def test_parse_sql_field_invalid(self) -> None:
        """Test SQL field parsing with invalid input."""
        # Single word should return None
        result = AutoGenerationService._parse_sql_field("invalid")
        assert result is None

        # Valid format but unknown type should default to string
        result = AutoGenerationService._parse_sql_field("invalid_field UNKNOWN_TYPE")
        assert result is not None
        assert result.name == "invalid_field"
        assert result.type == "string"

    def test_parse_json_structure_nested(self) -> None:
        """Test parsing nested JSON structures."""
        data = {"user": {"id": 123, "profile": {"name": "John", "age": 30}}, "tags": ["user", "active"]}

        result = AutoGenerationService._parse_json_structure(data)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_parse_json_structure_array(self) -> None:
        """Test parsing JSON arrays."""
        data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob", "extra": "field"}]

        result = AutoGenerationService._parse_json_structure(data)
        assert isinstance(result, list)

    def test_parse_json_structure_primitives(self) -> None:
        """Test parsing JSON with various primitive types."""
        data = {
            "string_field": "hello",
            "int_field": 42,
            "float_field": 3.14,
            "bool_field": True,
            "null_field": None,
        }

        result = AutoGenerationService._parse_json_structure(data)
        assert isinstance(result, list)
        assert len(result) == 5

        # Check that different types are correctly inferred
        type_mapping = {field.name: field.type for field in result}
        assert type_mapping.get("string_field") == "string"
        assert type_mapping.get("int_field") == "integer"
        assert type_mapping.get("float_field") == "number"
        assert type_mapping.get("bool_field") == "boolean"
        assert type_mapping.get("null_field") == "null"
