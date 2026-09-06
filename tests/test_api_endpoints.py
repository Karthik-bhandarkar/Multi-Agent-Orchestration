import time
import pytest
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "HEALTHY"}


class TestChatEndpoint:
    def test_chat_valid_query(self):
        response = client.post("/chat", json={
            "session_id": "pytest_session_1",
            "query": "What are my marks?",
            "roll_no": "102",
        })
        assert response.status_code == 200
        body = response.json()
        assert "response" in body
        assert "agent_used" in body

    def test_chat_crisis_bypasses_llm(self):
        response = client.post("/chat", json={
            "session_id": "pytest_session_2",
            "query": "I want to end my life",
        })
        assert response.status_code == 200
        body = response.json()
        assert body["agent_used"] == "CriticalGuardrailAgent"
        assert body["latency_ms"] < 15.0


class TestHistoryEndpoint:
    def test_history_after_chat(self):
        client.post("/chat", json={
            "session_id": "pytest_session_3",
            "query": "marks please",
            "roll_no": "102",
        })
        response = client.get("/history/pytest_session_3")
        assert response.status_code == 200
        assert len(response.json()["turns"]) >= 1

    def test_history_latency_benchmark(self):
        start = time.perf_counter()
        client.get("/history/pytest_session_3")
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"\n[BENCHMARK] /history latency: {elapsed_ms:.2f} ms")


class TestResetEndpoint:
    def test_reset_clears_session(self):
        client.post("/chat", json={
            "session_id": "pytest_session_4",
            "query": "test",
            "roll_no": "102",
        })
        reset_response = client.delete("/reset/pytest_session_4")
        assert reset_response.status_code == 200

        history_response = client.get("/history/pytest_session_4")
        assert len(history_response.json()["turns"]) == 0
