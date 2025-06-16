#!/usr/bin/env python3
"""Unit tests for AutoGenerationService field name sanitization."""

import os
import sys
from app.services.auto_generation_service import AutoGenerationService

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_enhanced_auto_generation():
    """Test the new more permissive auto-generation sanitization."""

    # Test cases: (input, expected_output)
    test_cases = [
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
        ("field name", "field name"),  # spaces now allowed
        # Should be sanitized (problematic characters)
        ("field(1)", "field_1_"),  # parentheses -> underscores
        ("field[0]", "field_0_"),  # brackets -> underscores
        ("field{0}", "field_0_"),  # braces -> underscores
        ('field"test"', "field_test_"),  # quotes -> underscores
        ("field/path", "field_path"),  # slash -> underscore
        ("field|pipe", "field_pipe"),  # pipe -> underscore
        ("field<tag>", "field_tag_"),  # angle brackets -> underscores
        ("field=value", "field_value"),  # equals -> underscore
        ("field+add", "field_add"),  # plus -> underscore
        ("field*mult", "field_mult"),  # asterisk -> underscore
        ("field%mod", "field_mod"),  # percent -> underscore
        ("field&and", "field_and"),  # ampersand -> underscore
        ("field^xor", "field_xor"),  # caret -> underscore
        ("field~not", "field_not"),  # tilde -> underscore
        ("field:colon", "field_colon"),  # colon -> underscore
        ("field;semi", "field_semi"),  # semicolon -> underscore
        ("field,comma", "field_comma"),  # comma -> underscore
        ("123field", "field_123field"),  # starts with number -> prefix
        ("{", "field_underscore"),  # single brace -> special case
        ("", "unnamed_field"),  # empty -> default
        ("   ", "unnamed_field"),  # whitespace only -> default
    ]

    print("Testing enhanced auto-generation sanitization:")
    print("=" * 65)

    passed = 0
    failed = 0

    for input_name, expected in test_cases:
        result = AutoGenerationService._sanitize_field_name(input_name)

        if result == expected:
            print(f"✓ PASS: '{input_name}' -> '{result}'")
            passed += 1
        else:
            print(f"✗ FAIL: '{input_name}' -> '{result}' (expected: '{expected}')")
            failed += 1

    print("=" * 65)
    print(f"Results: {passed} passed, {failed} failed")
    print(f"Success rate: {(passed/(passed+failed)*100):.1f}%")


if __name__ == "__main__":
    test_enhanced_auto_generation()
