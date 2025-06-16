"""Unit tests for basic field name validation functionality.

This module tests the core field validation logic and sanitization
for data contract field schemas.
"""

import pytest
from app.schemas.contract import FieldSchema
from pydantic import ValidationError


class TestBasicFieldValidation:
    """Test suite for basic field name validation and sanitization."""

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "input_name,expected_result",
        [
            # Basic validation cases
            ("valid_field", "valid_field"),  # Valid field should remain unchanged
            ("ValidField", "ValidField"),  # Valid field with uppercase should remain unchanged
            ("field-name", "field-name"),  # Hyphen should be allowed
            ("_private", "_private"),  # Leading underscore should be allowed
            ("field123", "field123"),  # Numbers after letters should be allowed
            ("camelCase", "camelCase"),  # Camel case should be allowed
            # Edge cases that should be handled
            ("", None),  # Empty should fail validation
            ("   ", None),  # Whitespace only should fail validation
            ("123field", None),  # Starting with number should fail (or be handled)
        ],
    )
    def test_field_name_basic_validation(self, input_name: str, expected_result: str) -> None:
        """Test basic field name validation.

        Args:
            input_name: Input field name to validate.
            expected_result: Expected result (None if should fail).
        """
        if expected_result is None:
            # Should raise ValidationError
            with pytest.raises(ValidationError):
                FieldSchema(name=input_name, type="string")
        else:
            # Should succeed
            field = FieldSchema(name=input_name, type="string")
            assert field.name == expected_result

    @pytest.mark.unit
    def test_field_schema_types(self) -> None:
        """Test field schema with different data types."""
        valid_types = [
            "string",
            "integer",
            "number",
            "boolean",
            "array",
            "object",
            "date",
            "datetime",
            "time",
            "binary",
            "null",
        ]

        for field_type in valid_types:
            field = FieldSchema(name="test_field", type=field_type)
            assert field.name == "test_field"
            assert field.type == field_type

    @pytest.mark.unit
    def test_field_schema_optional_properties(self) -> None:
        """Test field schema with optional properties."""
        field = FieldSchema(
            name="test_field",
            type="string",
            description="A test field",
            required=True,
            default_value="default",
        )

        assert field.name == "test_field"
        assert field.type == "string"
        assert field.description == "A test field"
        assert field.required is True
        assert field.default_value == "default"

    @pytest.mark.unit
    def test_field_schema_minimal(self) -> None:
        """Test field schema with minimal required properties."""
        field = FieldSchema(name="minimal_field", type="string")

        assert field.name == "minimal_field"
        assert field.type == "string"
        # Optional properties should have sensible defaults
        assert field.required is False  # Assuming default is False

    @pytest.mark.unit
    def test_field_validation_error_messages(self) -> None:
        """Test that validation errors provide meaningful messages."""
        with pytest.raises(ValidationError) as exc_info:
            FieldSchema(name="", type="string")

        error_message = str(exc_info.value)
        assert "name" in error_message.lower()

        # Test invalid type
        with pytest.raises(ValidationError) as exc_info:
            FieldSchema(name="valid_name", type="invalid_type")

        error_message = str(exc_info.value)
        assert "type" in error_message.lower()
