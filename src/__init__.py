"""
Advanced Multi-Agent System built on Microsoft AutoGen.

This package provides a production-ready multi-agent framework with:
- Architectural awareness and dynamic context management
- Multi-stage validation pipeline
- Enterprise-grade security and sandboxing
- Tiered model routing for cost efficiency
- Human-AI collaboration features
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .agents.base import BaseAgent
from .orchestration.group_chat import GroupChatManager
from .memory.architecture_ledger import ArchitectureLedger

__all__ = [
    "BaseAgent",
    "GroupChatManager",
    "ArchitectureLedger",
]
