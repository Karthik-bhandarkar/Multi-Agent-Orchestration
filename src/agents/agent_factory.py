from typing import Type, Dict
from src.agents.base_agent import BaseAgent


class AgentFactory:
    """Factory Pattern: decouples agent instantiation from the supervisor router."""

    _registry: Dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register(cls, key: str, agent_cls: Type[BaseAgent]) -> None:
        cls._registry[key] = agent_cls

    @classmethod
    def create_agent(cls, key: str, **kwargs) -> BaseAgent:
        if key not in cls._registry:
            raise ValueError(f"No agent registered under key: {key}")
        return cls._registry[key](**kwargs)

    @classmethod
    def available_agents(cls) -> list:
        return list(cls._registry.keys())
