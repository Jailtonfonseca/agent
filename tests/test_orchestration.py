"""Tests for orchestration module."""
import pytest
from src.orchestration.group_chat import GroupChatManager
from src.agents.planner import PlannerAgent

class TestGroupChatManager:
    def test_manager_creation(self):
        agents = [PlannerAgent()]
        manager = GroupChatManager(agents, max_rounds=5)
        assert len(manager.agents) == 1
    
    def test_manager_run(self):
        agents = [PlannerAgent()]
        manager = GroupChatManager(agents, max_rounds=2)
        result = manager.run("Test task")
        assert "messages" in result
        assert "status" in result
