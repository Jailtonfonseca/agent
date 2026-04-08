"""Advanced workflow example with custom tools and validation."""

from src.agents import (
    PlannerAgent, 
    CoderAgent, 
    ReviewerAgent, 
    TesterAgent,
    ComplianceAgent
)
from src.memory import ArchitectureLedger
from src.orchestration import GroupChatManager

def create_production_pipeline():
    """Create a production-ready agent pipeline."""
    
    # Initialize architecture ledger for context awareness
    ledger = ArchitectureLedger(storage_path="adrs.json")
    
    # Create specialized agents
    planner = PlannerAgent(
        llm_config={"model": "gpt-4"},
        architecture_ledger=ledger
    )
    
    coder = CoderAgent(
        llm_config={"model": "gpt-4"},
        sandbox_config={"use_docker": True, "network_disabled": True}
    )
    
    reviewer = ReviewerAgent(
        llm_config={"model": "gpt-4"},
        linter_tools=["ruff", "mypy", "bandit"]
    )
    
    tester = TesterAgent(
        llm_config={"model": "gpt-4"},
        test_framework="pytest",
        coverage_threshold=0.85
    )
    
    compliance = ComplianceAgent(
        llm_config={"model": "gpt-4"}
    )
    
    # Create orchestration manager
    manager = GroupChatManager(
        agents=[planner, coder, reviewer, tester, compliance],
        max_rounds=20
    )
    
    return manager, ledger

def main():
    manager, ledger = create_production_pipeline()
    
    # Complex task with multiple requirements
    task = """
    Create a REST API endpoint for user registration with:
    - Email validation
    - Password hashing (bcrypt)
    - Rate limiting
    - Input sanitization
    - Comprehensive tests
    """
    
    print("Starting production pipeline...")
    result = manager.run(task)
    
    print(f"\nPipeline completed: {result['status']}")
    print(f"Messages exchanged: {len(result['messages'])}")

if __name__ == "__main__":
    main()
