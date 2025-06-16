#!/usr/bin/env python3
"""Comprehensive test runner for Data Contracts Studio Backend.

This script provides a unified interface for running different types of tests
with proper reporting and coverage analysis.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class TestRunner:
    """Manages test execution with different configurations."""
    
    def __init__(self, backend_dir: Path) -> None:
        """Initialize the test runner.
        
        Args:
            backend_dir: Path to the backend directory.
        """
        self.backend_dir = backend_dir
        self.tests_dir = backend_dir / "tests"
    
    def run_unit_tests(self, verbose: bool = False) -> bool:
        """Run unit tests.
        
        Args:
            verbose: Enable verbose output.
            
        Returns:
            True if all tests passed, False otherwise.
        """
        cmd = [
            "python", "-m", "pytest",
            str(self.tests_dir / "unit"),
            "-m", "unit",
            "--tb=short"
        ]
        
        if verbose:
            cmd.append("-v")
            
        return self._run_command(cmd, "Unit Tests")
    
    def run_integration_tests(self, verbose: bool = False) -> bool:
        """Run integration tests.
        
        Args:
            verbose: Enable verbose output.
            
        Returns:
            True if all tests passed, False otherwise.
        """
        cmd = [
            "python", "-m", "pytest", 
            str(self.tests_dir / "integration"),
            "-m", "integration",
            "--tb=short"
        ]
        
        if verbose:
            cmd.append("-v")
            
        return self._run_command(cmd, "Integration Tests")
    
    def run_all_tests(self, verbose: bool = False, coverage: bool = True) -> bool:
        """Run all tests with optional coverage.
        
        Args:
            verbose: Enable verbose output.
            coverage: Generate coverage report.
            
        Returns:
            True if all tests passed, False otherwise.
        """
        cmd = ["python", "-m", "pytest", str(self.tests_dir)]
        
        if verbose:
            cmd.append("-v")
        
        if coverage:
            cmd.extend(["--cov=app", "--cov-report=term-missing"])
            
        return self._run_command(cmd, "All Tests")
    
    def run_linting(self) -> Tuple[bool, bool, bool]:
        """Run code quality checks.
        
        Returns:
            Tuple of (black_passed, isort_passed, flake8_passed).
        """
        print("🔍 Running code quality checks...")
        print("=" * 60)
        
        # Black formatting check
        black_cmd = ["python", "-m", "black", "--check", "app", "tests", "scripts"]
        black_passed = self._run_command(black_cmd, "Black Format Check", fail_on_error=False)
        
        # isort import sorting check  
        isort_cmd = ["python", "-m", "isort", "--check-only", "app", "tests", "scripts"]
        isort_passed = self._run_command(isort_cmd, "isort Import Check", fail_on_error=False)
        
        # flake8 linting
        flake8_cmd = ["python", "-m", "flake8", "app", "tests", "scripts"]
        flake8_passed = self._run_command(flake8_cmd, "flake8 Linting", fail_on_error=False)
        
        return black_passed, isort_passed, flake8_passed
    
    def run_type_checking(self) -> bool:
        """Run mypy type checking.
        
        Returns:
            True if type checking passed, False otherwise.
        """
        cmd = ["python", "-m", "mypy", "app"]
        return self._run_command(cmd, "MyPy Type Checking", fail_on_error=False)
    
    def _run_command(self, cmd: List[str], test_name: str, fail_on_error: bool = True) -> bool:
        """Run a command and report results.
        
        Args:
            cmd: Command to execute.
            test_name: Name of the test for reporting.
            fail_on_error: Whether to exit on error.
            
        Returns:
            True if command succeeded, False otherwise.
        """
        print(f"\n🧪 Running {test_name}...")
        print(f"Command: {' '.join(cmd)}")
        print("-" * 40)
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.backend_dir,
                capture_output=False,
                check=False
            )
            
            if result.returncode == 0:
                print(f"✅ {test_name} PASSED")
                return True
            else:
                print(f"❌ {test_name} FAILED (exit code: {result.returncode})")
                if fail_on_error:
                    sys.exit(result.returncode)
                return False
                
        except FileNotFoundError:
            print(f"❌ {test_name} FAILED - Command not found: {cmd[0]}")
            if fail_on_error:
                sys.exit(1)
            return False
        except KeyboardInterrupt:
            print(f"\n⚠️ {test_name} interrupted by user")
            sys.exit(1)


def main() -> None:
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Run tests for Data Contracts Studio Backend")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "all", "lint", "mypy"], 
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--no-coverage", action="store_true", help="Disable coverage reporting")
    parser.add_argument("--lint-only", action="store_true", help="Run only linting checks")
    
    args = parser.parse_args()
    
    # Get backend directory (parent of scripts directory)
    backend_dir = Path(__file__).parent.parent
    runner = TestRunner(backend_dir)
    
    print("🚀 Data Contracts Studio Backend Test Runner")
    print("=" * 60)
    
    success = True
    
    if args.lint_only or args.type == "lint":
        black_ok, isort_ok, flake8_ok = runner.run_linting()
        success = all([black_ok, isort_ok, flake8_ok])
    
    elif args.type == "mypy":
        success = runner.run_type_checking()
    
    elif args.type == "unit":
        success = runner.run_unit_tests(verbose=args.verbose)
    
    elif args.type == "integration":
        success = runner.run_integration_tests(verbose=args.verbose)
    
    elif args.type == "all":
        # Run linting first
        print("\n📋 Step 1: Code Quality Checks")
        black_ok, isort_ok, flake8_ok = runner.run_linting()
        
        # Run type checking
        print("\n📋 Step 2: Type Checking")
        mypy_ok = runner.run_type_checking()
        
        # Run tests
        print("\n📋 Step 3: Running Tests")
        tests_ok = runner.run_all_tests(
            verbose=args.verbose, 
            coverage=not args.no_coverage
        )
        
        success = all([black_ok, isort_ok, flake8_ok, mypy_ok, tests_ok])
    
    # Final summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 All checks PASSED!")
        sys.exit(0)
    else:
        print("💥 Some checks FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()
