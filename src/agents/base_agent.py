from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel


class AgentResult(BaseModel):
    agent_name: str
    status: Literal["SUCCESS", "FAILURE", "ESCALATED"]
    content: str
    metadata: Dict[str, Any] = {}
    latency_ms: float


class BaseAgent(ABC):
    """
    Abstract base class enforcing a uniform execution contract
    across all domain specialists.
    """

    def __init__(self, name: str, domain: str):
        self._name = name
        self._domain = domain

    @property
    def name(self) -> str:
        return self._name

    @property
    def domain(self) -> str:
        return self._domain

    @abstractmethod
    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        """Every specialist must implement this. Must return an AgentResult."""
        raise NotImplementedError
