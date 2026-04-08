"""Git Agent - Handles version control operations."""
from typing import Any, Dict, List, Optional
import logging
from .base import BaseAgent, AgentConfig
logger = logging.getLogger(__name__)

class GitAgent(BaseAgent):
    """Agent for Git operations including commits, branches, and PRs."""
    
    def __init__(self, llm_config: Optional[Dict[str, Any]] = None, **kwargs):
        config = AgentConfig(
            name="GitAgent",
            system_message="You are a Git expert. Handle version control operations.",
            llm_config=llm_config or {},
            **kwargs
        )
        super().__init__(config)
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        return {"role": "assistant", "content": "Git operations ready."}
    
    def commit(self, message: str, working_dir: str) -> bool:
        import subprocess
        try:
            result = subprocess.run(["git", "commit", "-m", message], cwd=working_dir, capture_output=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Commit failed: {e}")
            return False
    
    def create_branch(self, branch_name: str, working_dir: str) -> bool:
        import subprocess
        try:
            result = subprocess.run(["git", "checkout", "-b", branch_name], cwd=working_dir, capture_output=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Branch creation failed: {e}")
            return False
