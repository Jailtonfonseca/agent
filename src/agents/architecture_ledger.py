"""Architecture Ledger Agent - Tracks architectural decisions."""
from typing import Any, Dict, List, Optional
import logging
from .base import BaseAgent, AgentConfig
logger = logging.getLogger(__name__)

class ArchitectureLedgerAgent(BaseAgent):
    """Agent that maintains and queries architectural decision records."""
    
    def __init__(self, llm_config: Optional[Dict[str, Any]] = None, **kwargs):
        config = AgentConfig(
            name="ArchitectureLedgerAgent",
            system_message="You maintain architectural decision records.",
            llm_config=llm_config or {},
            **kwargs
        )
        super().__init__(config)
        self._adrs: List[Dict[str, Any]] = []
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        return {"role": "assistant", "content": "ADR ledger ready."}
    
    def add_adr(self, adr: Dict[str, Any]) -> None:
        self._adrs.append(adr)
    
    def query_relevant(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        return self._adrs[:limit]
