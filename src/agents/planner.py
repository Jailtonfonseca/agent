"""Planner Agent - Decomposes requirements into subtasks."""

from typing import Any, Dict, List, Optional
import logging
from .base import BaseAgent, AgentConfig

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """
    Agent responsible for analyzing requirements and decomposing them into actionable subtasks.
    
    Features:
    - Requirement analysis and clarification
    - Task decomposition with dependencies
    - Architecture-aware planning using ADR ledger
    - Complexity estimation for model routing
    """
    
    DEFAULT_SYSTEM_MESSAGE = """You are an expert software architect and planner. Your role is to:

1. Analyze requirements provided in natural language
2. Ask clarifying questions if requirements are ambiguous
3. Decompose requirements into small, testable subtasks
4. Identify task dependencies and execution order
5. Estimate complexity (LOW, MEDIUM, HIGH) for each task
6. Reference existing architectural decisions when relevant

Always output your plan in a structured format:
- Overview: Brief summary of the goal
- Tasks: Numbered list with [COMPLEXITY] tags
- Dependencies: Which tasks depend on others
- Risks: Potential challenges or considerations

Be concise but thorough. Focus on creating actionable plans that can be executed by coding agents."""

    def __init__(
        self,
        llm_config: Optional[Dict[str, Any]] = None,
        architecture_ledger: Optional[Any] = None,
        **kwargs
    ):
        """
        Initialize the Planner Agent.
        
        Args:
            llm_config: LLM configuration for the agent
            architecture_ledger: Optional ArchitectureLedger instance for context
            **kwargs: Additional arguments passed to BaseAgent
        """
        config = AgentConfig(
            name="PlannerAgent",
            system_message=self.DEFAULT_SYSTEM_MESSAGE,
            llm_config=llm_config or {},
            description="Analyzes requirements and creates execution plans",
            **kwargs
        )
        
        super().__init__(config)
        
        self.architecture_ledger = architecture_ledger
        self._current_plan: Optional[Dict[str, Any]] = None
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a requirement message and generate a plan.
        
        Args:
            message: Dictionary containing 'content' with the requirement
            
        Returns:
            Dictionary with the generated plan
        """
        content = message.get("content", "")
        
        if not content:
            return {
                "role": "assistant",
                "content": "No requirement provided. Please describe what you want to build or accomplish."
            }
        
        # Query architecture ledger if available
        context = ""
        if self.architecture_ledger:
            relevant_adrs = self.architecture_ledger.query_relevant(content, limit=3)
            if relevant_adrs:
                context = "\n\nRelevant Architectural Decisions:\n"
                for adr in relevant_adrs:
                    context += f"- {adr['id']}: {adr['title']}\n"
        
        # Build enhanced prompt with context
        enhanced_content = content + context
        
        logger.info(f"Planning task: {content[:100]}...")
        
        # Store current plan reference
        self._current_plan = {
            "requirement": content,
            "status": "planning",
            "tasks": [],
        }
        
        # In actual implementation, this would call the LLM
        # For now, return a placeholder response
        response_content = f"""## Plan Generated

**Requirement**: {content[:200]}

{context}

**Next Steps**: This plan will be executed by CoderAgent → TesterAgent → ReviewerAgent pipeline.

*Note: Full LLM integration required for complete planning functionality.*"""

        self._update_state(message_count=self.state.message_count + 1)
        
        return {
            "role": "assistant",
            "content": response_content,
            "plan": self._current_plan,
        }
    
    def create_task_breakdown(
        self,
        requirement: str,
        max_tasks: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Create a detailed task breakdown for a requirement.
        
        Args:
            requirement: The requirement to break down
            max_tasks: Maximum number of tasks to generate
            
        Returns:
            List of task dictionaries
        """
        # Placeholder implementation
        return [
            {
                "id": 1,
                "description": "Analyze requirement and identify components",
                "complexity": "LOW",
                "estimated_tokens": 1000,
                "dependencies": [],
            }
        ]
    
    def estimate_complexity(self, task_description: str) -> str:
        """
        Estimate the complexity of a task.
        
        Args:
            task_description: Description of the task
            
        Returns:
            Complexity level: "LOW", "MEDIUM", or "HIGH"
        """
        # Simple heuristic based on description length
        # In production, use LLM classification
        word_count = len(task_description.split())
        
        if word_count < 20:
            return "LOW"
        elif word_count < 50:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def get_current_plan(self) -> Optional[Dict[str, Any]]:
        """Return the current active plan."""
        return self._current_plan
    
    def clear_plan(self) -> None:
        """Clear the current plan."""
        self._current_plan = None
