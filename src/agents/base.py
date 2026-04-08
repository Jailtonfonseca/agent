"""Base agent class with common functionality for all agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    
    name: str
    system_message: str
    llm_config: Dict[str, Any] = field(default_factory=dict)
    max_consecutive_auto_reply: int = 10
    human_input_mode: str = "NEVER"  # NEVER, TERMINATE, ALWAYS
    code_execution_config: Optional[Dict[str, Any]] = None
    tools: Optional[List[Callable]] = None
    description: str = ""
    
    def __post_init__(self):
        if not self.description:
            self.description = self.system_message[:100] + "..."


@dataclass
class AgentState:
    """Represents the current state of an agent."""
    
    is_active: bool = True
    message_count: int = 0
    last_activity: Optional[datetime] = None
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    
    Provides common functionality including:
    - Configuration management
    - State tracking
    - Logging and monitoring
    - Tool registration
    - Message handling
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the base agent.
        
        Args:
            config: Agent configuration object
        """
        self.config = config
        self.state = AgentState()
        self._tools: Dict[str, Callable] = {}
        self._message_history: List[Dict[str, Any]] = []
        
        logger.info(f"Initialized agent: {config.name}")
        
        if config.tools:
            for tool in config.tools:
                self.register_tool(tool)
    
    @property
    def name(self) -> str:
        """Return the agent's name."""
        return self.config.name
    
    @property
    def is_active(self) -> bool:
        """Check if the agent is active."""
        return self.state.is_active
    
    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message and generate a response.
        
        Args:
            message: The incoming message dictionary
            
        Returns:
            Response message dictionary
        """
        pass
    
    def register_tool(self, tool: Callable, name: Optional[str] = None) -> None:
        """
        Register a tool function with the agent.
        
        Args:
            tool: The tool function to register
            name: Optional name for the tool (defaults to function name)
        """
        tool_name = name or tool.__name__
        self._tools[tool_name] = tool
        logger.debug(f"Registered tool: {tool_name}")
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Retrieve a registered tool by name.
        
        Args:
            name: Name of the tool
            
        Returns:
            The tool function or None if not found
        """
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        """
        List all registered tool names.
        
        Returns:
            List of tool names
        """
        return list(self._tools.keys())
    
    def _update_state(self, **kwargs) -> None:
        """
        Update the agent's state with new values.
        
        Args:
            **kwargs: State attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
        
        self.state.last_activity = datetime.now()
    
    def _add_error(self, error: str) -> None:
        """
        Record an error in the agent's state.
        
        Args:
            error: Error message to record
        """
        self.state.errors.append(error)
        logger.error(f"Agent {self.name} error: {error}")
    
    def _clear_errors(self) -> None:
        """Clear all recorded errors."""
        self.state.errors.clear()
    
    def deactivate(self) -> None:
        """Deactivate the agent."""
        self._update_state(is_active=False)
        logger.info(f"Agent {self.name} deactivated")
    
    def activate(self) -> None:
        """Activate the agent."""
        self._update_state(is_active=True)
        logger.info(f"Agent {self.name} activated")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the agent's activity.
        
        Returns:
            Dictionary with agent statistics
        """
        return {
            "name": self.name,
            "is_active": self.state.is_active,
            "message_count": self.state.message_count,
            "last_activity": self.state.last_activity.isoformat() if self.state.last_activity else None,
            "error_count": len(self.state.errors),
            "tool_count": len(self._tools),
        }
    
    def to_autogen_config(self) -> Dict[str, Any]:
        """
        Convert agent configuration to AutoGen-compatible format.
        
        Returns:
            Dictionary suitable for autogen.AssistantAgent
        """
        config_dict = {
            "name": self.config.name,
            "system_message": self.config.system_message,
            "llm_config": self.config.llm_config,
            "max_consecutive_auto_reply": self.config.max_consecutive_auto_reply,
            "human_input_mode": self.config.human_input_mode,
        }
        
        if self.config.code_execution_config:
            config_dict["code_execution_config"] = self.config.code_execution_config
        
        return config_dict
