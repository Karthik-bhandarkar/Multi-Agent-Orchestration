import pytest
from src.rag.vector_store import VectorStore


@pytest.fixture(scope="module")
def vector_store():
    vs = VectorStore()
    vs.build_index("data/academic_regulations.txt")
    return vs


class TestRAGRetrieval:
    def test_relevant_query_high_score(self, vector_store):
        results = vector_store.search("What is the minimum attendance requirement?", top_k=2)
        assert len(results) > 0
        assert results[0]["score"] > 0.50
        assert "attendance" in results[0]["text"].lower()

    def test_top_k_respected(self, vector_store):
        results = vector_store.search("grading scale", top_k=1)
        assert len(results) == 1

    def test_irrelevant_query_lower_score(self, vector_store):
        results = vector_store.search("What is the weather today?", top_k=1)
        assert results[0]["score"] < 0.75
