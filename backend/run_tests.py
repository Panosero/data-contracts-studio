#!/usr/bin/env python3
"""Test runner for all unit tests."""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run all unit tests and report results."""

    # Get the current directory (backend)
    backend_dir = Path(__file__).parent
    tests_dir = backend_dir / "tests" / "unit"

    # Find all test files
    test_files = list(tests_dir.glob("test_*.py"))

    if not test_files:
        print("No test files found!")
        return False

    print(f"Running {len(test_files)} test files...")
    print("=" * 60)

    all_passed = True
    results = []

    for test_file in sorted(test_files):
        print(f"\nRunning {test_file.name}...")
        print("-" * 40)

        try:
            # Run the test file
            result = subprocess.run(
                [sys.executable, str(test_file)],
                cwd=backend_dir,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.returncode == 0:
                print("✓ PASSED")
                results.append((test_file.name, True, ""))
                # Show the output for successful tests
                if result.stdout:
                    print(result.stdout)
            else:
                print("✗ FAILED")
                all_passed = False
                error_msg = result.stderr or result.stdout or "Unknown error"
                results.append((test_file.name, False, error_msg))
                print(f"Error: {error_msg}")

        except subprocess.TimeoutExpired:
            print("✗ TIMEOUT")
            all_passed = False
            results.append((test_file.name, False, "Test timed out"))
        except Exception as e:
            print(f"✗ ERROR: {e}")
            all_passed = False
            results.append((test_file.name, False, str(e)))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)

    for test_name, passed, error in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status:10} {test_name}")
        if not passed and error:
            print(f"           Error: {error[:100]}...")

    print(f"\nResults: {passed_count}/{total_count} tests passed")
    print(f"Success rate: {(passed_count/total_count)*100:.1f}%")

    return all_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
