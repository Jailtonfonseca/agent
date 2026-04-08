"""Coder Agent - Generates and edits code."""

from typing import Any, Dict, List, Optional
import logging
from .base import BaseAgent, AgentConfig

logger = logging.getLogger(__name__)


class CoderAgent(BaseAgent):
    """
    Agent responsible for generating, editing, and refactoring code.
    
    Features:
    - Code generation from specifications
    - Incremental patch-based editing
    - Multi-language support
    - Integration with dependency graph
    - Self-correction based on test feedback
    """
    
    DEFAULT_SYSTEM_MESSAGE = """You are an expert software engineer specializing in writing clean, efficient, and maintainable code. Your role is to:

1. Generate code based on specifications from the PlannerAgent
2. Follow best practices for the target language/framework
3. Write self-documenting code with clear naming
4. Include appropriate error handling and edge cases
5. Generate unified diffs when modifying existing files
6. Reference the dependency graph for context-aware changes

Coding Standards:
- Use meaningful variable and function names
- Keep functions small and focused (single responsibility)
- Add docstrings for public APIs
- Handle errors gracefully
- Write testable code

When modifying files, always output unified diff format unless creating new files."""

    def __init__(
        self,
        llm_config: Optional[Dict[str, Any]] = None,
        dependency_graph: Optional[Any] = None,
        sandbox_config: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize the Coder Agent.
        
        Args:
            llm_config: LLM configuration for the agent
            dependency_graph: Optional DependencyGraph instance for context
            sandbox_config: Configuration for code execution sandbox
            **kwargs: Additional arguments passed to BaseAgent
        """
        config = AgentConfig(
            name="CoderAgent",
            system_message=self.DEFAULT_SYSTEM_MESSAGE,
            llm_config=llm_config or {},
            description="Generates and edits code based on specifications",
            code_execution_config=sandbox_config,
            **kwargs
        )
        
        super().__init__(config)
        
        self.dependency_graph = dependency_graph
        self._current_file_context: Dict[str, str] = {}
        self._generated_patches: List[Dict[str, Any]] = []
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a coding task and generate code.
        
        Args:
            message: Dictionary containing 'content' with the task specification
            
        Returns:
            Dictionary with generated code or patches
        """
        content = message.get("content", "")
        file_context = message.get("file_context", {})
        
        if not content:
            return {
                "role": "assistant",
                "content": "No coding task provided. Please specify what code to generate or modify."
            }
        
        # Update file context
        self._current_file_context.update(file_context)
        
        # Query dependency graph if available
        deps_context = ""
        if self.dependency_graph:
            relevant_deps = self.dependency_graph.get_relevant_dependencies(content)
            if relevant_deps:
                deps_context = "\n\nRelevant Dependencies:\n"
                for dep in relevant_deps:
                    deps_context += f"- {dep}\n"
        
        logger.info(f"Coding task: {content[:100]}...")
        
        # In actual implementation, this would call the LLM
        response_content = f"""## Code Generation Task

**Specification**: {content[:200]}

{deps_context}

**Status**: Ready to generate code.

*Note: Full LLM integration required for complete code generation functionality.*

### Example Output Format:

For new files:
```python
# filename.py
def example():
    pass
```

For modifications (unified diff):
```diff
--- a/src/module.py
+++ b/src/module.py
@@ -1,2 +1,5 @@
+def new_function():
+    pass
+
 def existing():
     pass
```"""

        self._update_state(message_count=self.state.message_count + 1)
        
        return {
            "role": "assistant",
            "content": response_content,
            "file_context": self._current_file_context,
        }
    
    def generate_patch(
        self,
        file_path: str,
        original_content: str,
        instructions: str
    ) -> Optional[str]:
        """
        Generate a unified diff patch for file modifications.
        
        Args:
            file_path: Path to the file being modified
            original_content: Current content of the file
            instructions: Instructions for the modification
            
        Returns:
            Unified diff string or None if no changes needed
        """
        # Placeholder implementation
        # In production, use LLM to generate the patch
        patch = f"""--- a/{file_path}
+++ b/{file_path}
@@ -1,0 +1,5 @@
+# Generated by CoderAgent
+# Instructions: {instructions[:100]}
+
+pass
"""
        self._generated_patches.append({
            "file_path": file_path,
            "patch": patch,
            "instructions": instructions,
        })
        
        return patch
    
    def apply_patch(self, patch: str, working_dir: str) -> bool:
        """
        Apply a unified diff patch to a file.
        
        Args:
            patch: Unified diff string
            working_dir: Working directory for patch application
            
        Returns:
            True if successful, False otherwise
        """
        import subprocess
        
        try:
            result = subprocess.run(
                ["git", "apply", "--cached"],
                input=patch.encode(),
                cwd=working_dir,
                capture_output=True,
                timeout=30,
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to apply patch: {e}")
            return False
    
    def get_generated_patches(self) -> List[Dict[str, Any]]:
        """Return list of generated patches."""
        return self._generated_patches.copy()
    
    def clear_patches(self) -> None:
        """Clear the generated patches list."""
        self._generated_patches.clear()
    
    def set_file_context(self, file_path: str, content: str) -> None:
        """
        Set the context for a specific file.
        
        Args:
            file_path: Path to the file
            content: File content
        """
        self._current_file_context[file_path] = content
    
    def get_file_context(self, file_path: str) -> Optional[str]:
        """
        Get the context for a specific file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content or None if not in context
        """
        return self._current_file_context.get(file_path)
