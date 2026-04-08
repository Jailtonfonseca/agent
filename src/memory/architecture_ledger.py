"""Architecture Ledger - Stores and retrieves architectural decisions."""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
logger = logging.getLogger(__name__)

@dataclass
class ADR:
    """Architectural Decision Record."""
    id: str
    title: str
    status: str  # proposed, accepted, deprecated
    context: str
    decision: str
    consequences: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)

class ArchitectureLedger:
    """Manages architectural decision records."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self._adrs: Dict[str, ADR] = {}
        self._storage_path = storage_path
    
    def add_adr(self, adr: ADR) -> None:
        self._adrs[adr.id] = adr
        logger.info(f"Added ADR: {adr.id} - {adr.title}")
    
    def get_adr(self, adr_id: str) -> Optional[ADR]:
        return self._adrs.get(adr_id)
    
    def query_relevant(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        adrs_list = list(self._adrs.values())
        results = []
        for adr in adrs_list[:limit]:
            results.append({
                "id": adr.id,
                "title": adr.title,
                "status": adr.status,
            })
        return results
    
    def list_adrs(self) -> List[Dict[str, Any]]:
        return [{"id": a.id, "title": a.title, "status": a.status} for a in self._adrs.values()]
    
    def save(self) -> None:
        if not self._storage_path:
            return
        data = {k: {"id": v.id, "title": v.title, "status": v.status, 
                    "context": v.context, "decision": v.decision} 
                for k, v in self._adrs.items()}
        with open(self._storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self) -> None:
        if not self._storage_path or not self._storage_path.exists():
            return
        with open(self._storage_path, 'r') as f:
            data = json.load(f)
        for k, v in data.items():
            self._adrs[k] = ADR(**v)
