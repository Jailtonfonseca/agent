"""Basic usage example of the multi-agent system."""

from src.agents import PlannerAgent, CoderAgent, ReviewerAgent
from src.orchestration import GroupChatManager

def main():
    # Initialize agents
    planner = PlannerAgent(
        llm_config={"model": "gpt-4", "temperature": 0.7}
    )
    
    coder = CoderAgent(
        llm_config={"model": "gpt-4", "temperature": 0.7},
        sandbox_config={"use_docker": True}
    )
    
    reviewer = ReviewerAgent(
        llm_config={"model": "gpt-4"},
        linter_tools=["ruff"]
    )
    
    # Create group chat manager
    manager = GroupChatManager(
        agents=[planner, coder, reviewer],
        max_rounds=10
    )
    
    # Run a task
    task = "Create a Python function that calculates the factorial of a number"
    print(f"Running task: {task}\n")
    
    result = manager.run(task)
    
    print(f"\nStatus: {result['status']}")
    print(f"Total messages: {len(result['messages'])}")
    
    # Print conversation
    for msg in result['messages']:
        print(f"\n{msg.get('role', 'unknown')}: {msg.get('content', '')[:200]}...")

if __name__ == "__main__":
    main()
