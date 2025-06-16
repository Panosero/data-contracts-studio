"""Unit tests for enhanced field name validation functionality.

This module tests the enhanced field name validation that allows
more permissive field names while maintaining data integrity.
"""

import pytest
from pydantic import ValidationError
from app.schemas.contract import FieldSchema


class TestFieldValidation:
    """Test suite for enhanced field name validation."""

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "field_name,should_pass",
        [
            # Valid cases - should pass
            ("user_id", True),
            ("UserName", True),
            ("field-name", True),
            ("$price", True),
            ("_internal", True),
            ("email@domain", True),
            ("field.name", True),
            ("item#1", True),
            ("status!", True),
            ("field?", True),
            # Invalid cases - should fail
            ("field name", False),  # space
            ("field(1)", False),  # parentheses
            ("field[0]", False),  # brackets
            ("field{0}", False),  # braces
            ('field"test"', False),  # quotes
            ("field/path", False),  # slash
            ("field|pipe", False),  # pipe
            ("field<tag>", False),  # angle brackets
            ("field=value", False),  # equals
            ("field+add", False),  # plus
            ("field*mult", False),  # asterisk
            ("field%mod", False),  # percent
            ("field&and", False),  # ampersand
            ("field\ttab", False),  # tab
            ("field\nnewline", False),  # newline
            # Edge cases
            ("", False),  # empty string
            ("_", True),  # single underscore
            ("123", True),  # numeric
        ],
    )
    def test_field_name_validation(self, field_name: str, should_pass: bool) -> None:
        """Test field name validation with various inputs.

        Args:
            field_name: Field name to validate.
            should_pass: Whether validation should pass.
        """
        if should_pass:
            # Should not raise ValidationError
            field = FieldSchema(name=field_name, type="string")
            assert field.name == field_name
        else:
            # Should raise ValidationError
            with pytest.raises(ValidationError):
                FieldSchema(name=field_name, type="string")

    @pytest.mark.unit
    def test_field_validation_with_complete_schema(self) -> None:
        """Test field validation with complete field schema."""
        # Valid field schema
        valid_field = FieldSchema(
            name="user_id", type="integer", description="Unique user identifier", required=True
        )

        assert valid_field.name == "user_id"
        assert valid_field.type == "integer"
        assert valid_field.description == "Unique user identifier"
        assert valid_field.required is True

        # Invalid field schema with bad field name
        with pytest.raises(ValidationError) as exc_info:
            FieldSchema(name="user id", type="integer", description="Unique user identifier")  # space in name

        # Verify the error is about field name validation
        error_messages = str(exc_info.value)
        assert "name" in error_messages.lower()

    @pytest.mark.unit
    def test_field_validation_unicode_support(self) -> None:
        """Test field validation with Unicode characters."""
        # Should support valid Unicode identifiers
        unicode_fields = [
            "field_é",  # accented character
            "field_ñ",  # tilde
            "field_中文",  # Chinese characters
        ]

        for field_name in unicode_fields:
            field = FieldSchema(name=field_name, type="string")
            assert field.name == field_name

    @pytest.mark.unit
    def test_field_validation_length_limits(self) -> None:
        """Test field validation with length limits."""
        # Very short names should be valid
        short_field = FieldSchema(name="a", type="string")
        assert short_field.name == "a"

        # Very long names should be handled gracefully
        long_name = "field_" + "a" * 250

        if len(long_name) <= 255:  # Assuming reasonable limit
            field = FieldSchema(name=long_name, type="string")
            assert field.name == long_name
        else:
            # Should raise validation error for extremely long names
            with pytest.raises(ValidationError):
                FieldSchema(name=long_name, type="string")
