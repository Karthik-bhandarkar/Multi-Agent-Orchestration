import streamlit as st
import httpx
import uuid
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db.student_repository import StudentRepository

st.set_page_config(
    page_title="EduPulse AI — Enterprise Multi-Agent Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000"

AGENT_COLORS = {
    "DATA_RETRIEVAL": "🔵",
    "KNOWLEDGE_RAG": "🟢",
    "ANALYTICS": "🟡",
    "CriticalGuardrailAgent": "🔴",
    "unknown": "⚪",
}

# Custom Styling for Sleek Dark Glassmorphism Aesthetics
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 50%, #0F172A 100%);
        color: #F8FAFC;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        backdrop-filter: blur(12px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header Banner
st.title("🎓 EduPulse AI — Multi-Agent Governance Portal")
st.caption(f"Session Identifier: `{st.session_state.session_id}` | Environment: `Production / Cloud`")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Session Controls")
roll_no = st.sidebar.text_input("Active Student Roll Number", value="102")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Database Inspector")
inspect_roll = st.sidebar.text_input("Inspect Student Roll No", value="102", key="inspect")

if st.sidebar.button("Fetch Record", use_container_width=True):
    try:
        with StudentRepository() as repo:
            summary = repo.get_student_summary(inspect_roll)
        st.sidebar.json(summary)
    except Exception as e:
        st.sidebar.error(f"Error fetching record: {e}")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Reset Session", type="secondary", use_container_width=True):
    try:
        httpx.delete(f"{API_BASE}/reset/{st.session_state.session_id}", timeout=10)
    except Exception:
        pass
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())[:8]
    st.rerun()

# --- Chat History Display ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            agent = msg.get("agent_used", "unknown")
            badge = AGENT_COLORS.get(agent, "⚪")
            lat = msg.get("latency_ms", 0.0)
            if agent == "CriticalGuardrailAgent":
                st.error("⚠️ CRISIS INTERVENTION ACTIVATED — Emergency Helplines Dispatched.")
            st.caption(f"{badge} Specialist Agent: `{agent}` | Response Latency: `{lat:.1f} ms`")

query = st.chat_input("Ask about marks, academic policies, or performance summaries...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Orchestrating Multi-Agent Network..."):
        try:
            response = httpx.post(
                f"{API_BASE}/chat",
                json={
                    "session_id": st.session_state.session_id,
                    "query": query,
                    "roll_no": roll_no,
                },
                timeout=30,
            )
            data = response.json()
            response_text = data.get("response", "No response received.")
            agent_used = data.get("agent_used", "unknown")
            latency_ms = data.get("latency_ms", 0.0)

        except Exception as e:
            response_text = f"Error connecting to backend API at {API_BASE}: {str(e)}"
            agent_used = "system_error"
            latency_ms = 0.0

    agent_badge = AGENT_COLORS.get(agent_used, "⚪")

    with st.chat_message("assistant"):
        if agent_used == "CriticalGuardrailAgent":
            st.error("⚠️ CRISIS INTERVENTION ACTIVATED — Emergency Helplines Dispatched.")
        st.write(response_text)
        st.caption(f"{agent_badge} Specialist Agent: `{agent_used}` | Response Latency: `{latency_ms:.1f} ms`")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "agent_used": agent_used,
        "latency_ms": latency_ms,
    })
