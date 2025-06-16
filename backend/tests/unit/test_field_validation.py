#!/usr/bin/env python3
"""Unit tests for field name validation."""

import os
import sys
from app.schemas.contract import FieldSchema

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def test_enhanced_field_validation():
    """Test the new more permissive field name validation."""

    # Test cases: (input, should_pass, expected_result)
    test_cases = [
        # Valid cases - should pass
        ("user_id", True, "user_id"),
        ("UserName", True, "UserName"),
        ("field-name", True, "field-name"),
        ("$price", True, "$price"),
        ("_internal", True, "_internal"),
        ("email@domain", True, "email@domain"),
        ("field.name", True, "field.name"),
        ("item#1", True, "item#1"),
        ("status!", True, "status!"),
        ("field?", True, "field?"),
        ("field name", True, "field name"),  # spaces now allowed
        # Invalid cases - should fail
        ("field(1)", False, None),  # parentheses
        ("field[0]", False, None),  # brackets
        ("field{0}", False, None),  # braces
        ('field"test"', False, None),  # quotes
        ("field/path", False, None),  # slash
        ("field|pipe", False, None),  # pipe
        ("field<tag>", False, None),  # angle brackets
        ("field=value", False, None),  # equals
        ("field+add", False, None),  # plus
        ("field*mult", False, None),  # asterisk
        ("field%mod", False, None),  # percent
        ("field&and", False, None),  # ampersand
        ("field^xor", False, None),  # caret
        ("field~not", False, None),  # tilde
        ("field:colon", False, None),  # colon
        ("field;semi", False, None),  # semicolon
        ("field,comma", False, None),  # comma
        ("123field", False, None),  # starts with number
        ("", False, None),  # empty
        ("   ", False, None),  # whitespace only
    ]

    print("Testing enhanced field name validation:")
    print("=" * 60)

    passed = 0
    failed = 0

    for input_name, should_pass, expected in test_cases:
        try:
            field = FieldSchema(name=input_name, type="string")
            result = field.name

            if should_pass:
                if result == expected:
                    print(f"✓ PASS: '{input_name}' -> '{result}' (allowed)")
                    passed += 1
                else:
                    print(f"✗ FAIL: '{input_name}' -> '{result}' (expected: '{expected}')")
                    failed += 1
            else:
                print(f"✗ FAIL: '{input_name}' -> '{result}' (should have been rejected)")
                failed += 1

        except Exception as e:
            if not should_pass:
                print(f"✓ PASS: '{input_name}' -> REJECTED ({str(e).split(',')[0]})")
                passed += 1
            else:
                print(f"✗ FAIL: '{input_name}' -> REJECTED (should have been allowed)")
                failed += 1

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print(f"Success rate: {(passed/(passed+failed)*100):.1f}%")


if __name__ == "__main__":
    test_enhanced_field_validation()
