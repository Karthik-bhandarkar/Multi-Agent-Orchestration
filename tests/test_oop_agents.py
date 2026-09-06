import pytest
from src.agents.base_agent import BaseAgent, AgentResult
from src.agents.agent_factory import AgentFactory
import src.agents.specialists  # noqa
from src.agents.supervisor import build_graph
from src.db.init_db import initialize_database


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    initialize_database()


class TestBaseAgentContract:
    def test_cannot_instantiate_abstract_base(self):
        with pytest.raises(TypeError):
            BaseAgent("test", "test")


class TestAgentFactory:
    @pytest.mark.parametrize("key", ["DATA_RETRIEVAL", "KNOWLEDGE_RAG", "ANALYTICS", "GUARDRAIL"])
    def test_create_all_registered_agents(self, key):
        agent = AgentFactory.create_agent(key)
        assert isinstance(agent, BaseAgent)

    def test_unknown_key_raises(self):
        with pytest.raises(ValueError):
            AgentFactory.create_agent("NOT_REAL")


class TestSpecialistExecution:
    def test_data_retrieval_agent(self):
        agent = AgentFactory.create_agent("DATA_RETRIEVAL")
        result = agent.execute("marks", context={"roll_no": "102"})
        assert isinstance(result, AgentResult)
        assert result.status == "SUCCESS"

    def test_guardrail_agent_detects_crisis(self):
        agent = AgentFactory.create_agent("GUARDRAIL")
        result = agent.execute("I want to end my life")
        assert result.status == "ESCALATED"


class TestSupervisorGraph:
    def test_graph_compiles(self):
        graph = build_graph()
        assert graph is not None

    def test_end_to_end_data_query(self):
        graph = build_graph()
        result = graph.invoke({
            "query": "What are my marks?",
            "roll_no": "102",
            "step_count": 0,
        })
        assert result["response"] is not None
