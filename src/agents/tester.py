"""Tester Agent - Generates and executes tests."""

from typing import Any, Dict, List, Optional
import logging
from .base import BaseAgent, AgentConfig

logger = logging.getLogger(__name__)


class TesterAgent(BaseAgent):
    """
    Agent responsible for generating and executing tests.
    
    Features:
    - Automatic test generation from specifications
    - Test case expansion based on failures
    - Coverage analysis
    - Integration with CI/CD pipelines
    """
    
    DEFAULT_SYSTEM_MESSAGE = """You are an expert QA engineer and test automation specialist. Your role is to:

1. Generate comprehensive test suites for code changes
2. Create unit tests, integration tests, and edge case tests
3. Ensure adequate code coverage (>80% target)
4. Write clear, maintainable test code
5. Auto-generate new tests when failures occur
6. Validate that tests properly verify requirements

Testing Standards:
- Follow AAA pattern (Arrange, Act, Assert)
- Use descriptive test names that explain the scenario
- Test both happy paths and edge cases
- Mock external dependencies appropriately
- Include regression tests for bug fixes

Output tests in the appropriate format for the language/framework."""

    def __init__(
        self,
        llm_config: Optional[Dict[str, Any]] = None,
        test_framework: str = "pytest",
        coverage_threshold: float = 0.8,
        **kwargs
    ):
        """
        Initialize the Tester Agent.
        
        Args:
            llm_config: LLM configuration for the agent
            test_framework: Testing framework to use (pytest, unittest, etc.)
            coverage_threshold: Minimum code coverage threshold (0.0-1.0)
            **kwargs: Additional arguments passed to BaseAgent
        """
        config = AgentConfig(
            name="TesterAgent",
            system_message=self.DEFAULT_SYSTEM_MESSAGE,
            llm_config=llm_config or {},
            description="Generates and executes tests",
            **kwargs
        )
        
        super().__init__(config)
        
        self.test_framework = test_framework
        self.coverage_threshold = coverage_threshold
        self._current_tests: List[Dict[str, Any]] = []
        self._coverage_report: Optional[Dict[str, Any]] = None
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a test generation request.
        
        Args:
            message: Dictionary containing code and specifications
            
        Returns:
            Dictionary with generated tests
        """
        content = message.get("content", "")
        code_to_test = message.get("code", "")
        specifications = message.get("specifications", [])
        
        if not code_to_test and not content:
            return {
                "role": "assistant",
                "content": "No code provided for testing. Please provide code to generate tests for."
            }
        
        logger.info(f"Generating tests for code...")
        
        # In actual implementation, this would call the LLM
        response_content = f"""## Test Generation Task

**Framework**: {self.test_framework}
**Coverage Target**: {self.coverage_threshold * 100}%

**Code to Test**: {len(code_to_test)} characters

### Generated Tests:

*Note: Full LLM integration required for complete test generation functionality.*

### Example Test Structure:

```python
def test_example_case():
    # Arrange
    expected = ...
    
    # Act
    result = function_under_test(...)
    
    # Assert
    assert result == expected
```

### Test Plan:
1. Unit tests for individual functions
2. Integration tests for component interactions
3. Edge case tests
4. Regression tests (if applicable)"""

        self._update_state(message_count=self.state.message_count + 1)
        
        return {
            "role": "assistant",
            "content": response_content,
            "tests": self._current_tests,
        }
    
    def generate_test_file(
        self,
        source_file: str,
        source_code: str,
        test_type: str = "unit"
    ) -> str:
        """
        Generate a test file for the given source code.
        
        Args:
            source_file: Path to the source file
            source_code: Content of the source file
            test_type: Type of tests to generate (unit, integration, e2e)
            
        Returns:
            Generated test file content
        """
        # Placeholder implementation
        test_content = f'''"""Tests for {source_file}."""

import pytest
# TODO: Import modules under test


class TestGenerated:
    """Auto-generated test class."""
    
    def test_placeholder(self):
        """Placeholder test - implement based on source code analysis."""
        # TODO: Implement actual test
        assert True, "Test not yet implemented"
'''
        
        self._current_tests.append({
            "source_file": source_file,
            "test_type": test_type,
            "content": test_content,
        })
        
        return test_content
    
    def run_tests(self, test_path: str, working_dir: str) -> Dict[str, Any]:
        """
        Run tests using the configured test framework.
        
        Args:
            test_path: Path to test file or directory
            working_dir: Working directory for test execution
            
        Returns:
            Dictionary with test results
        """
        import subprocess
        
        try:
            if self.test_framework == "pytest":
                cmd = [
                    "pytest",
                    test_path,
                    "--tb=short",
                    f"--cov={working_dir}",
                    "--cov-report=json",
                    "-v",
                ]
            else:
                cmd = ["python", "-m", "unittest", "discover", "-s", test_path]
            
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=300,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Test execution timed out",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def analyze_coverage(self, coverage_report_path: str) -> Dict[str, Any]:
        """
        Analyze code coverage from a coverage report.
        
        Args:
            coverage_report_path: Path to coverage JSON report
            
        Returns:
            Coverage analysis dictionary
        """
        import json
        
        try:
            with open(coverage_report_path, 'r') as f:
                report = json.load(f)
            
            total_coverage = report.get('totals', {}).get('percent_covered', 0)
            meets_threshold = total_coverage >= (self.coverage_threshold * 100)
            
            self._coverage_report = {
                "total_coverage": total_coverage,
                "meets_threshold": meets_threshold,
                "threshold": self.coverage_threshold * 100,
                "files": report.get('files', {}),
            }
            
            return self._coverage_report
        except Exception as e:
            logger.error(f"Failed to analyze coverage: {e}")
            return {
                "error": str(e),
                "meets_threshold": False,
            }
    
    def generate_tests_for_failure(
        self,
        failure_details: Dict[str, Any]
    ) -> str:
        """
        Generate new tests to cover a specific failure.
        
        Args:
            failure_details: Details about the test failure
            
        Returns:
            New test code to address the failure
        """
        # Placeholder implementation
        return f'''def test_regression_{failure_details.get("test_name", "unknown")}():
    """Regression test for: {failure_details.get("error", "Unknown error")}"""
    # TODO: Implement test based on failure analysis
    pass
'''
    
    def get_current_tests(self) -> List[Dict[str, Any]]:
        """Return list of generated tests."""
        return self._current_tests.copy()
    
    def get_coverage_report(self) -> Optional[Dict[str, Any]]:
        """Return the current coverage report."""
        return self._coverage_report
