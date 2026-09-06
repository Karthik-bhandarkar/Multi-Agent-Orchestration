"""
EduPulse AI — Interactive Command Line Chat Runner
Allows direct interactive chatting with the multi-agent system from your terminal.
"""

import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def start_cli_chat():
    session_id = str(uuid.uuid4())[:8]
    roll_no = "102"

    print("==========================================================")
    print("🎓 EDUPULSE AI — INTERACTIVE TERMINAL CHAT")
    print(f"Session ID: {session_id} | Default Roll No: {roll_no}")
    print("Type your questions below. Type 'exit' or 'quit' to stop.")
    print("Type 'reset' to clear session history.")
    print("==========================================================\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye! Session terminated.")
                break

            if user_input.lower() == "reset":
                resp = client.delete(f"/reset/{session_id}")
                session_id = str(uuid.uuid4())[:8]
                print(f"system: {resp.json()['message']} New Session ID: {session_id}\n")
                continue

            resp = client.post(
                "/chat",
                json={
                    "session_id": session_id,
                    "query": user_input,
                    "roll_no": roll_no,
                },
            )
            data = resp.json()

            agent = data.get("agent_used", "unknown")
            latency = data.get("latency_ms", 0.0)
            response = data.get("response", "")

            print(f"\n[Agent: {agent} | Latency: {latency:.1f}ms]")
            print(f"EduPulse: {response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat CLI...")
            break


if __name__ == "__main__":
    start_cli_chat()
