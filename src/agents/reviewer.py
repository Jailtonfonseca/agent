"""Reviewer Agent - Analyzes code quality and provides feedback."""

from typing import Any, Dict, List, Optional
import logging
from .base import BaseAgent, AgentConfig

logger = logging.getLogger(__name__)


class ReviewerAgent(BaseAgent):
    """
    Agent responsible for reviewing code changes and ensuring quality standards.
    
    Features:
    - Code review with best practices enforcement
    - Security vulnerability detection
    - Performance optimization suggestions
    - Style guide compliance checking
    - Architecture consistency validation
    """
    
    DEFAULT_SYSTEM_MESSAGE = """You are a senior software engineer and code reviewer. Your role is to:

1. Review code changes for correctness, clarity, and maintainability
2. Identify potential bugs, security issues, and performance problems
3. Ensure adherence to coding standards and best practices
4. Validate that changes align with architectural decisions
5. Provide constructive, actionable feedback
6. Approve changes only when they meet quality standards

Review Criteria:
- Correctness: Does the code work as intended?
- Clarity: Is the code easy to understand?
- Maintainability: Will future developers be able to modify this easily?
- Security: Are there any vulnerabilities or unsafe patterns?
- Performance: Are there obvious inefficiencies?
- Testing: Are there adequate tests for the changes?

Output your review in a structured format with clear APPROVE/REQUEST_CHANGES decision."""

    def __init__(
        self,
        llm_config: Optional[Dict[str, Any]] = None,
        linter_tools: Optional[List[str]] = None,
        **kwargs
    ):
        """
        Initialize the Reviewer Agent.
        
        Args:
            llm_config: LLM configuration for the agent
            linter_tools: List of linter tools to use (e.g., ["ruff", "mypy"])
            **kwargs: Additional arguments passed to BaseAgent
        """
        config = AgentConfig(
            name="ReviewerAgent",
            system_message=self.DEFAULT_SYSTEM_MESSAGE,
            llm_config=llm_config or {},
            description="Reviews code changes for quality and standards",
            **kwargs
        )
        
        super().__init__(config)
        
        self.linter_tools = linter_tools or ["ruff", "mypy"]
        self._current_review: Optional[Dict[str, Any]] = None
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a code review request.
        
        Args:
            message: Dictionary containing code diff and context
            
        Returns:
            Dictionary with review results
        """
        content = message.get("content", "")
        code_diff = message.get("code_diff", "")
        file_context = message.get("file_context", {})
        
        if not code_diff and not content:
            return {
                "role": "assistant",
                "content": "No code provided for review. Please provide a diff or code snippet."
            }
        
        logger.info(f"Reviewing code changes...")
        
        # Run linting tools if configured
        lint_results = []
        for tool in self.linter_tools:
            # Placeholder for actual linting
            lint_results.append({
                "tool": tool,
                "status": "pending",
                "issues": [],
            })
        
        # In actual implementation, this would call the LLM
        response_content = f"""## Code Review

**Changes**: {len(code_diff)} characters of diff

### Linting Results:
{self._format_lint_results(lint_results)}

### Review Status: PENDING

*Note: Full LLM integration required for complete review functionality.*

### Review Checklist:
- [ ] Code correctness verified
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Code style compliant
- [ ] Adequate test coverage
- [ ] Documentation updated

**Decision**: Awaiting detailed analysis..."""

        self._update_state(message_count=self.state.message_count + 1)
        
        self._current_review = {
            "status": "in_progress",
            "lint_results": lint_results,
            "decision": None,
        }
        
        return {
            "role": "assistant",
            "content": response_content,
            "review": self._current_review,
        }
    
    def _format_lint_results(self, results: List[Dict[str, Any]]) -> str:
        """Format linting results for display."""
        output = []
        for result in results:
            status = result.get("status", "unknown")
            tool = result.get("tool", "unknown")
            issue_count = len(result.get("issues", []))
            output.append(f"- {tool}: {status} ({issue_count} issues)")
        return "\n".join(output)
    
    def run_linter(self, tool: str, file_path: str, content: str) -> Dict[str, Any]:
        """
        Run a specific linter on code content.
        
        Args:
            tool: Name of the linter tool
            file_path: Path to the file (for context)
            content: Code content to lint
            
        Returns:
            Dictionary with linting results
        """
        import subprocess
        import tempfile
        import os
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(content)
                temp_path = f.name
            
            if tool == "ruff":
                result = subprocess.run(
                    ["ruff", "check", "--output-format=json", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            elif tool == "mypy":
                result = subprocess.run(
                    ["mypy", "--no-error-summary", "--json", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            else:
                return {
                    "tool": tool,
                    "status": "unsupported",
                    "issues": [],
                }
            
            issues = []
            if result.stdout:
                import json
                try:
                    issues = json.loads(result.stdout)
                except json.JSONDecodeError:
                    issues = [{"message": result.stdout}]
            
            return {
                "tool": tool,
                "status": "completed",
                "issues": issues,
            }
        except Exception as e:
            logger.error(f"Linter {tool} failed: {e}")
            return {
                "tool": tool,
                "status": "error",
                "error": str(e),
                "issues": [],
            }
        finally:
            if 'temp_path' in locals():
                os.unlink(temp_path)
    
    def approve(self, comments: Optional[str] = None) -> Dict[str, Any]:
        """
        Approve the code changes.
        
        Args:
            comments: Optional approval comments
            
        Returns:
            Updated review dictionary
        """
        if not self._current_review:
            self._current_review = {}
        
        self._current_review.update({
            "status": "approved",
            "decision": "APPROVE",
            "comments": comments,
        })
        
        logger.info("Code review: APPROVED")
        
        return self._current_review
    
    def request_changes(self, reasons: List[str]) -> Dict[str, Any]:
        """
        Request changes to the code.
        
        Args:
            reasons: List of reasons requiring changes
            
        Returns:
            Updated review dictionary
        """
        if not self._current_review:
            self._current_review = {}
        
        self._current_review.update({
            "status": "changes_requested",
            "decision": "REQUEST_CHANGES",
            "reasons": reasons,
        })
        
        logger.info(f"Code review: CHANGES REQUESTED ({len(reasons)} reasons)")
        
        return self._current_review
    
    def get_current_review(self) -> Optional[Dict[str, Any]]:
        """Return the current active review."""
        return self._current_review
