import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from api.schemas import (
    ChatRequest,
    ChatResponse,
    HistoryResponse,
    HistoryTurn,
    ResetResponse,
)
from src.core.config import settings
from src.core.lru_cache import LRUCache
from src.agents.supervisor import build_graph
from src.db.init_db import initialize_database
from src.tools.safety_guardrail import check_crisis
from src.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="EduPulse AI Backend", version="0.1.0")

session_cache = LRUCache(capacity=settings.LRU_CACHE_CAPACITY)
supervisor_graph = build_graph()
SESSION_LOG_FILE = "Session History.txt"


@app.on_event("startup")
def startup_event():
    initialize_database()
    logger.info("EduPulse backend startup complete: DB ready, graph compiled, cache initialized.")


@app.get("/")
def root():
    return {
        "service": "EduPulse AI — Distributed Multi-Agent System API",
        "status": "ONLINE",
        "version": "0.1.0",
        "documentation": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "HEALTHY"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    start = time.perf_counter()

    # 1. Tier-1 Deterministic Guardrail Check (Sub-5ms Bypass)
    crisis = check_crisis(request.query)
    if crisis:
        elapsed = (time.perf_counter() - start) * 1000
        helpline_text = "\n".join([f"- {k}: {v}" for k, v in crisis["helplines"].items()])
        crisis_content = f"{crisis['message']}\n\nImmediate Support:\n{helpline_text}"

        return ChatResponse(
            session_id=request.session_id,
            response=crisis_content,
            agent_used="CriticalGuardrailAgent",
            latency_ms=round(elapsed, 3),
        )

    # 2. Multi-Agent Supervisor Execution & Session Caching
    try:
        history = session_cache.get(request.session_id) or []

        result_state = supervisor_graph.invoke({
            "query": request.query,
            "roll_no": request.roll_no,
            "step_count": 0,
        })

        agent_used = result_state.get("agent_key", "unknown")
        response_text = result_state.get("response", "No response generated.")

        history.append({
            "query": request.query,
            "response": response_text,
            "agent_used": agent_used,
        })
        session_cache.put(request.session_id, history)

        elapsed = (time.perf_counter() - start) * 1000
        return ChatResponse(
            session_id=request.session_id,
            response=response_text,
            agent_used=agent_used,
            latency_ms=round(elapsed, 3),
        )
    except Exception as e:
        logger.error(f"/chat failed: {e}")
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")


@app.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str):
    history = session_cache.get(session_id) or []
    turns = [HistoryTurn(**h) for h in history]
    return HistoryResponse(session_id=session_id, turns=turns)


@app.delete("/reset/{session_id}", response_model=ResetResponse)
def reset_session(session_id: str):
    history = session_cache.get(session_id)
    if history:
        with open(SESSION_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n--- Session {session_id} reset at {datetime.now().isoformat()} ---\n")
            for turn in history:
                f.write(f"Q: {turn['query']}\nA: {turn['response']}\nAgent: {turn['agent_used']}\n\n")

    session_cache.map.pop(session_id, None)
    return ResetResponse(session_id=session_id, message="Session history cleared and archived.")
