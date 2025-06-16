#!/usr/bin/env python3
"""Test script for field name validation."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.schemas.contract import FieldSchema


def test_field_validation():
    """Test field name validation and sanitization."""
    test_cases = [
        ("field_!", "field__"),  # Invalid character should be replaced
        ("{", "field_{"),  # Invalid start should be prefixed
        ("valid_field", "valid_field"),  # Valid field should remain unchanged
        ("ValidField", "ValidField"),  # Valid field with uppercase should remain unchanged
        ("123field", "field_123field"),  # Starting with number should be prefixed
        ("field-name", "field-name"),  # Hyphen should be allowed
        ("", "field_unknown"),  # Empty should be replaced
        ("   ", "field_unknown"),  # Whitespace only should be replaced
    ]

    print("Testing field name validation:")
    print("-" * 50)

    for input_name, expected in test_cases:
        try:
            field = FieldSchema(name=input_name, type="string")
            result = field.name
            status = "✓ PASS" if result == expected else "✗ FAIL"
            print(f"{status}: '{input_name}' -> '{result}' (expected: '{expected}')")
        except Exception as e:
            print(f"✗ ERROR: '{input_name}' -> Exception: {e}")

    print("-" * 50)


if __name__ == "__main__":
    test_field_validation()
