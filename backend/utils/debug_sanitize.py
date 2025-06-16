#!/usr/bin/env python3
import re


def debug_sanitize(name):
    print(f"Testing: {name!r}")

    if not name or not name.strip():
        return "unnamed_field"

    # Start with the trimmed, lowercase name
    sanitized = name.strip().lower()
    print(f"  After trim/lower: {sanitized!r}")

    # Replace spaces and other common separators with underscores
    sanitized = re.sub(r"[\s\-\.]+", "_", sanitized)
    print(f"  After space/dash/dot replacement: {sanitized!r}")

    # Remove all invalid characters (keep only alphanumeric, underscore, hyphen)
    sanitized = re.sub(r"[^a-zA-Z0-9_\-]", "", sanitized)
    print(f"  After removing invalid chars: {sanitized!r}")

    # Ensure it starts with a letter or underscore
    if not sanitized or not (sanitized[0].isalpha() or sanitized[0] == "_"):
        sanitized = f"field_{sanitized}" if sanitized else "field"
        print(f"  After ensuring valid start: {sanitized!r}")

    # Ensure it's not empty after sanitization
    if not sanitized:
        return "unnamed_field"

    return sanitized


# Test cases
for test_case in ["field_!", "{", "valid_field"]:
    result = debug_sanitize(test_case)
    print(f"Final result: {result!r}")
    print("---")
