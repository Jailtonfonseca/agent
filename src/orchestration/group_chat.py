"""Group Chat Manager - Orchestrates multi-agent conversations."""
from typing import Any, Dict, List, Optional
import logging
logger = logging.getLogger(__name__)

class GroupChatManager:
    """Manages conversations between multiple agents."""
    
    def __init__(self, agents: List[Any], max_rounds: int = 10):
        self.agents = {agent.name: agent for agent in agents}
        self.max_rounds = max_rounds
        self._message_history: List[Dict[str, Any]] = []
    
    def run(self, initial_message: str) -> Dict[str, Any]:
        """Run a multi-agent conversation."""
        logger.info(f"Starting group chat with {len(self.agents)} agents")
        messages = [{"role": "user", "content": initial_message}]
        
        for round_num in range(self.max_rounds):
            for agent_name, agent in self.agents.items():
                if not agent.is_active:
                    continue
                
                last_message = messages[-1]
                response = agent.process_message(last_message)
                messages.append(response)
                
                if self._should_terminate(response):
                    return {"messages": messages, "status": "completed"}
        
        return {"messages": messages, "status": "max_rounds_reached"}
    
    def _should_terminate(self, message: Dict[str, Any]) -> bool:
        content = message.get("content", "")
        return "TERMINATE" in content or "COMPLETE" in content
    
    def get_history(self) -> List[Dict[str, Any]]:
        return self._message_history.copy()
