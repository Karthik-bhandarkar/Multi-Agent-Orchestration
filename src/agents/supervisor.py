import sys
from typing import TypedDict, Optional, Literal
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from src.core.config import settings
from src.agents.agent_factory import AgentFactory
import src.agents.specialists  # noqa: F401
from src.utils.exception import CustomException
from src.utils.logger import get_logger

logger = get_logger(__name__)

MAX_STEPS = 8


class RouteDecision(BaseModel):
    agent_key: Literal["DATA_RETRIEVAL", "KNOWLEDGE_RAG", "ANALYTICS", "GUARDRAIL"] = Field(
        description="The single best agent to handle this query"
    )
    reasoning: str = Field(description="Brief justification for the routing decision")


class SupervisorState(TypedDict):
    query: str
    roll_no: Optional[str]
    agent_key: Optional[str]
    response: Optional[str]
    step_count: int


def _get_llm():
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        temperature=0,
        max_tokens=200,
    )


def router_node(state: SupervisorState) -> SupervisorState:
    if not settings.GROQ_API_KEY or "your_" in settings.GROQ_API_KEY or settings.GROQ_API_KEY == "":
        query_lower = state.get("query", "").lower()
        if any(w in query_lower for w in ["mark", "score", "grade"]):
            state["agent_key"] = "DATA_RETRIEVAL"
        elif any(w in query_lower for w in ["die", "suicide", "harm", "kill"]):
            state["agent_key"] = "GUARDRAIL"
        elif any(w in query_lower for w in ["pass", "summary", "performance"]):
            state["agent_key"] = "ANALYTICS"
        else:
            state["agent_key"] = "KNOWLEDGE_RAG"
        logger.info(f"CI Fallback Router decision: {state['agent_key']}")
        return state

    try:
        llm = _get_llm().with_structured_output(RouteDecision)
        decision: RouteDecision = llm.invoke(
            f"""Classify this student query into exactly one category:
            - DATA_RETRIEVAL: asking for specific marks/scores/attendance records
            - KNOWLEDGE_RAG: asking about academic policies, rules, regulations
            - ANALYTICS: asking for performance summary, pass/fail, averages
            - GUARDRAIL: any distress, self-harm, or emergency content

            Query: {state['query']}
            """
        )
        state["agent_key"] = decision.agent_key
        logger.info(f"Router decision: {decision.agent_key} ({decision.reasoning})")
    except Exception as e:
        logger.error(f"Router failed, defaulting to KNOWLEDGE_RAG: {e}")
        state["agent_key"] = "KNOWLEDGE_RAG"
    return state


def agent_execution_node(state: SupervisorState) -> SupervisorState:
    state["step_count"] = state.get("step_count", 0) + 1

    if state["step_count"] > MAX_STEPS:
        state["response"] = "Maximum reasoning steps exceeded. Please rephrase your query."
        return state

    try:
        agent = AgentFactory.create_agent(state["agent_key"])
        result = agent.execute(state["query"], context={"roll_no": state.get("roll_no")})
        state["response"] = result.content
    except Exception as e:
        raise CustomException(e, sys) from e

    return state


def build_graph():
    graph = StateGraph(SupervisorState)
    graph.add_node("router", router_node)
    graph.add_node("execute_agent", agent_execution_node)

    graph.set_entry_point("router")
    graph.add_edge("router", "execute_agent")
    graph.add_edge("execute_agent", END)

    return graph.compile()
