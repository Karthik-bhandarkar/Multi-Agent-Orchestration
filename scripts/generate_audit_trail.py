"""
EduPulse AI — Session Audit Trail Generator & Verifier
Invokes /chat endpoints for multiple agent domains and resets the session to archive the audit log.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

SESSION_ID = "demo1"


def generate_demo_audit_trail():
    print(f"Generating session audit trail for session_id='{SESSION_ID}'...")

    queries = [
        {"session_id": SESSION_ID, "query": "what are my marks", "roll_no": "102"},
        {"session_id": SESSION_ID, "query": "what is the minimum attendance policy", "roll_no": "102"},
        {"session_id": SESSION_ID, "query": "am I passing this semester", "roll_no": "102"},
        {"session_id": SESSION_ID, "query": "I feel hopeless and want to end my life", "roll_no": "102"},
    ]

    for q in queries:
        resp = client.post("/chat", json=q)
        data = resp.json()
        clean_resp = data['response'][:60].encode('ascii', errors='ignore').decode('ascii')
        print(f"[CHAT] Agent: {data['agent_used']} | Latency: {data['latency_ms']:.2f}ms | Response: {clean_resp}...")

    # Fetch History
    hist_resp = client.get(f"/history/{SESSION_ID}")
    print(f"[HISTORY] Total turns recorded in LRU Cache: {len(hist_resp.json()['turns'])}")

    # Reset Session -> Archives to Session History.txt
    reset_resp = client.delete(f"/reset/{SESSION_ID}")
    print(f"[RESET] {reset_resp.json()['message']}")

    # Inspect Session History.txt
    if os.path.exists("Session History.txt"):
        with open("Session History.txt", "r", encoding="utf-8") as f:
            content = f.read()
        print("\n=== Session History.txt Content Preview ===")
        print(content[-500:])


if __name__ == "__main__":
    generate_demo_audit_trail()
