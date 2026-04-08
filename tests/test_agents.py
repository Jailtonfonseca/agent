"""Tests for agent classes."""
import pytest
from src.agents.base import BaseAgent, AgentConfig
from src.agents.planner import PlannerAgent
from src.agents.coder import CoderAgent

class TestAgentConfig:
    def test_config_creation(self):
        config = AgentConfig(
            name="TestAgent",
            system_message="Test message"
        )
        assert config.name == "TestAgent"
        assert config.system_message == "Test message"
        assert config.max_consecutive_auto_reply == 10

class TestPlannerAgent:
    def test_planner_initialization(self):
        agent = PlannerAgent()
        assert agent.name == "PlannerAgent"
        assert agent.is_active == True
    
    def test_planner_process_message(self):
        agent = PlannerAgent()
        result = agent.process_message({"content": "Create a function"})
        assert "role" in result
        assert "content" in result

class TestCoderAgent:
    def test_coder_initialization(self):
        agent = CoderAgent()
        assert agent.name == "CoderAgent"
    
    def test_coder_process_empty_message(self):
        agent = CoderAgent()
        result = agent.process_message({})
        assert "No coding task" in result["content"]
