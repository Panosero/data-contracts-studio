"""Unit tests for auto-generation service sanitization functionality.

This module tests the enhanced auto-generation sanitization that allows
more permissive field names while still handling problematic characters.
"""

import pytest
from app.services.auto_generation_service import AutoGenerationService


class TestAutoGenerationService:
    """Test suite for AutoGenerationService sanitization functionality."""

    @pytest.fixture
    def auto_generation_service(self) -> AutoGenerationService:
        """Create AutoGenerationService instance for testing.

        Returns:
            AutoGenerationService instance.
        """
        return AutoGenerationService()

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "input_field,expected_output",
        [
            # Should be preserved (valid)
            ("user_id", "user_id"),
            ("UserName", "UserName"),
            ("field-name", "field-name"),
            ("$price", "$price"),
            ("_internal", "_internal"),
            ("email@domain", "email@domain"),
            ("field.name", "field.name"),
            ("item#1", "item#1"),
            ("status!", "status!"),
            ("field?", "field?"),
            # Should be sanitized (problematic characters)
            ("field name", "field_name"),  # space -> underscore
            ("field(1)", "field_1_"),  # parentheses -> underscores
            ("field[0]", "field_0_"),  # brackets -> underscores
            ("field{key}", "field_key_"),  # braces -> underscores
            ("field/path", "field_path"),  # slash -> underscore
            ("field\\path", "field_path"),  # backslash -> underscore
            ("field|pipe", "field_pipe"),  # pipe -> underscore
            ("field<tag>", "field_tag_"),  # angle brackets -> underscores
            ("field,list", "field_list"),  # comma -> underscore
            ("field;semi", "field_semi"),  # semicolon -> underscore
            ("field:colon", "field_colon"),  # colon -> underscore
            ('field"quote', "field_quote"),  # quote -> underscore
            ("field'apos", "field_apos"),  # apostrophe -> underscore
            ("field\ttab", "field_tab"),  # tab -> underscore
            ("field\nnewline", "field_newline"),  # newline -> underscore
            # Edge cases  
            ("", "unnamed_field"),  # empty string -> safe default
            ("_", "field_underscore"),  # single underscore -> safer name
            ("___", "___"),  # multiple underscores
            ("123", "field_123"),  # numeric -> prefixed for safety
            ("field___name", "field___name"),  # multiple underscores preserved
        ],
    )
    def test_sanitize_field_name(
        self, auto_generation_service: AutoGenerationService, input_field: str, expected_output: str
    ) -> None:
        """Test field name sanitization with various inputs.

        Args:
            auto_generation_service: Service instance for testing.
            input_field: Input field name to sanitize.
            expected_output: Expected sanitized output.
        """
        result = auto_generation_service.sanitize_field_name(input_field)
        assert (
            result == expected_output
        ), f"Expected '{input_field}' to be sanitized to '{expected_output}', but got '{result}'"

    @pytest.mark.unit
    def test_sanitize_field_name_unicode(self, auto_generation_service: AutoGenerationService) -> None:
        """Test field name sanitization with Unicode characters.

        Args:
            auto_generation_service: Service instance for testing.
        """
        # Unicode characters should be preserved if they're valid identifiers
        test_cases = [
            ("field_é", "field_é"),  # accented character
            ("field_ñ", "field_ñ"),  # tilde
            ("field_中文", "field_中文"),  # Chinese characters
            ("field_🚀", "field_🚀"),  # emoji preserved (permissive approach)
        ]

        for input_field, expected in test_cases:
            result = auto_generation_service.sanitize_field_name(input_field)
            assert (
                result == expected
            ), f"Expected '{input_field}' to be sanitized to '{expected}', but got '{result}'"

    @pytest.mark.unit
    def test_sanitize_field_name_length_limits(self, auto_generation_service: AutoGenerationService) -> None:
        """Test field name sanitization with length limits.

        Args:
            auto_generation_service: Service instance for testing.
        """
        # Very long field name
        long_field = "a" * 1000
        result = auto_generation_service.sanitize_field_name(long_field)

        # Should handle very long names gracefully
        assert len(result) <= 255, "Sanitized field name should not exceed reasonable length"
        assert result.startswith("a"), "Sanitized field should preserve beginning"
