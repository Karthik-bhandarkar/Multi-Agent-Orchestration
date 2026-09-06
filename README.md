# 🎓 EduPulse AI — Enterprise Distributed Multi-Agent Governance & Crisis Intervention System

[![EduPulse CI Pipeline](https://github.com/Karthik-bhandarkar/Multi-Agent-Orchestration/actions/workflows/ci.yml/badge.svg)](https://github.com/Karthik-bhandarkar/Multi-Agent-Orchestration/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![LangChain / LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![Render](https://img.shields.io/badge/Deployment-Render%20Cloud-success.svg)](https://render.com)

**Infosys Springboard Internship 6.0 Project**  
*Developer*: Karthik Bhandarkar ([@Karthik-bhandarkar](https://github.com/Karthik-bhandarkar))

---

## 📌 Executive Summary

EduPulse AI resolves common LLM prototype failure modes (such as raw `eval()` Remote Code Execution, bypassable crisis keyword detection, routing deadlocks, and silent failure green status) through a production-grade **Two-Tier Governance Architecture**:

1. **Tier-1 Deterministic Security Guardrails**: Pre-compiled regex crisis detection running with **sub-5ms latency** that bypasses LLM execution during distress/self-harm signals to eliminate hallucinated safety advice, and AST-based arithmetic parsing preventing arbitrary code execution.
2. **Tier-2 OOP Multi-Agent Orchestration**: A LangGraph supervisor graph with structured Pydantic LLM routing (Groq Cloud LLM), Factory Pattern decoupling, $O(1)$ Doubly Linked List LRU Cache, thread-safe ACID SQLite persistence, and dynamic PORT containerization on Render Cloud.

---

## 🏗️ System Architecture

```text
                               +---------------------------------------+
                               |        Client / Streamlit UI          |
                               +---------------------------------------+
                                                   |
                                                   v
                               +---------------------------------------+
                               |     FastAPI Service Layer (/chat)      |
                               +---------------------------------------+
                                                   |
                   +-------------------------------+-------------------------------+
                   |                                                               |
                   v (Crisis Input Detected)                                       v (Academic Input)
   +-------------------------------+                               +-------------------------------+
   |  Tier-1 Regex Guardrail Check  |                               |    LangGraph Supervisor Router|
   | (Sub-5ms Emergency Helpline)  |                               | (Structured Output / Factory) |
   +-------------------------------+                               +-------------------------------+
                                                                                   |
                                  +-------------------+--------------------+-------+--------------------+
                                  |                   |                    |                            |
                                  v                   v                    v                            v
                        +------------------+ +------------------+ +-------------------+ +-------------------+
                        | DataRetrieval    | | KnowledgeRAG     | | AnalyticsReport   | | CriticalGuardrail |
                        | Specialist Agent | | Specialist Agent | | Specialist Agent  | | Specialist Agent  |
                        +------------------+ +------------------+ +-------------------+ +-------------------+
                                  |                   |                    |                            |
                                  v                   v                    v                            v
                        +------------------+ +------------------+ +-------------------+ +-------------------+
                        | StudentRepository| | FAISS VectorStore| | SafeMathParser    | | Emergency Helpline|
                        | (SQLite DB)      | | (SentenceTransf) | | (AST Evaluator)   | | Dispatcher      |
                        +------------------+ +------------------+ +-------------------+ +-------------------+
```

---

## 🛡️ Audit Defect Remediation Matrix

| Bug ID | Severity | Original Audit Defect | EduPulse AI Fix & Architectural Pattern |
|---|---|---|---|
| **BUG-01** | CRITICAL | Calculator executed raw `eval(expr)` causing arbitrary code execution (RCE) | `SafeMathParser` using Python's `ast` module whitelisting only arithmetic operators (`+`, `-`, `*`, `/`, `**`, `%`) |
| **BUG-02** | HIGH | Router failed 40% of queries due to fragile string parsing | Structured Pydantic output schemas (`RouteDecision`) via LangGraph + Groq Cloud LLM |
| **ARCH-03** | HIGH | Infinite routing loops and router-agent conflicts | Enforced hard reasoning execution cap (`MAX_STEPS = 8`) + Factory Pattern decoupling (`AgentFactory`) |
| **ARCH-05** | HIGH | Postman screenshots proved FastAPI existed, but source code was missing | Full asynchronous FastAPI backend (`api/app.py`) providing `/health`, `/chat`, `/history`, and `/reset` |

---

## ⚡ Empirical Benchmark Ledger (System-Wide Verified)

| Metric / Benchmark | Operational Target | Measured Value | Verification Test Suite | Status |
|---|---|---|---|---|
| **Tier-1 Guardrail Intercept** | `< 15.0 ms` | **`0.010 ms`** | `tests/test_security_tools.py` | ✅ **PASSED** |
| **LRU Cache Get/Put** | `< 0.05 ms` | **`0.00028 ms`** | `tests/test_dsa_cache.py` | ✅ **PASSED** |
| **SQL Query Latency** | `< 5.0 ms` | **`0.282 ms`** | `tests/test_sql_engine.py` | ✅ **PASSED** |
| **/history Endpoint Latency** | `~ 55.0 ms` | **`4.16 ms`** | `tests/test_api_endpoints.py` | ✅ **PASSED** |
| **RAG Cosine Retrieval Score** | `> 0.50` | **`0.544`** | `tests/test_rag.py` | ✅ **PASSED** |
| **Supervisor Router Accuracy** | `100%` | **`20/20 (100.0%)`** | `scripts/verify_supervisor_routing.py` | ✅ **PASSED** |
| **Pytest Suite Pass Rate** | `100%` | **`50/50 (100.0%)`** | `pytest tests/ -v` | ✅ **PASSED** |
| **CI/CD Pipeline Status** | `GREEN` | **`BUILD SUCCESS`** | `.github/workflows/ci.yml` | ✅ **PASSED** |
| **Render Cloud Deployment** | `200 OK` | **`LIVE`** | `https://multi-agent-orchestration.onrender.com/health` | ✅ **PASSED** |

---

## 🔌 API Endpoint Documentation

### 1. `GET /health`
- **Description**: Returns cloud container health status for Render port scanning and Docker probes.
- **Response**:
```json
{
  "status": "HEALTHY"
}
```

### 2. `POST /chat`
- **Description**: Submits student query to the multi-agent system.
- **Request Body**:
```json
{
  "session_id": "session_102",
  "query": "What are my marks?",
  "roll_no": "102"
}
```
- **Response**:
```json
{
  "session_id": "session_102",
  "response": "Student Summary for Roll No 102:\n• Name: Aarav Sharma\n• Average Score: 79.00\n• Average Attendance: 88.25%\n• Overall Status: PASS",
  "agent_used": "DATA_RETRIEVAL",
  "latency_ms": 1253.25
}
```

### 3. `GET /history/{session_id}`
- **Description**: Fetches past conversation turns stored in the $O(1)$ LRU Cache.
- **Response**:
```json
{
  "session_id": "session_102",
  "turns": [
    {
      "query": "What are my marks?",
      "response": "Student Summary for Roll No 102...",
      "agent_used": "DATA_RETRIEVAL"
    }
  ]
}
```

### 4. `DELETE /reset/{session_id}`
- **Description**: Clears session history from in-memory LRU Cache and archives conversation records into `Session History.txt`.
- **Response**:
```json
{
  "session_id": "session_102",
  "message": "Session history cleared and archived."
}
```

---

## 💻 Local Setup & Execution Guide

### 1. Clone & Environment Setup
```bash
git clone https://github.com/Karthik-bhandarkar/Multi-Agent-Orchestration.git
cd Multi-Agent-Orchestration

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies in editable mode
pip install -r requirements.txt
pip install -e .
```

### 2. Configure Environment Variables
Create a `.env` file at the root of the project:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
ENV=development
DB_PATH=./data/edupulse.db
LOG_LEVEL=INFO
```

### 3. Initialize Database & Build FAISS Vector Index
```bash
python -m src.db.init_db
python -m src.rag.vector_store
```

### 4. Launch FastAPI Backend Service
```bash
uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Launch Streamlit Web UI
In a second terminal window:
```bash
streamlit run ui/streamlit_app.py
```

---

## 🧪 Testing & Quality Control

Run the complete 50-test automated pytest battery:
```bash
pytest tests/ -v
```

Run code formatting and flake8 linter checks:
```bash
flake8 src/ api/ tests/ --max-line-length=120 --extend-ignore=E203,W503
```

---

## 📄 License
This project is developed under the **Infosys Springboard Internship 6.0** program and licensed under the MIT License.
