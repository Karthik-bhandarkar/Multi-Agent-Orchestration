"""
EduPulse AI — Groq API Connection Live Tester
Tests both GROQ_API_KEY and GROQ_API_KEY2 with ChatGroq model invocation.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.config import settings
from src.utils.logger import get_logger
from langchain_groq import ChatGroq

logger = get_logger(__name__)


def test_groq_key(key_name: str, key_val: str) -> dict:
    if not key_val or "your_" in key_val:
        return {"key": key_name, "status": "SKIP", "message": "Key not configured"}

    try:
        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            groq_api_key=key_val,
            temperature=0.2,
            max_tokens=50,
        )
        response = llm.invoke("Hello! Confirm system status in 1 sentence.")
        text = response.content.strip()
        logger.info(f"Groq API connection test [{key_name}] SUCCESS: {text}")
        return {
            "key": key_name,
            "status": "PASS",
            "model": settings.GROQ_MODEL,
            "response": text,
        }
    except Exception as e:
        logger.error(f"Groq API connection test [{key_name}] FAILED: {str(e)}")
        return {"key": key_name, "status": "FAIL", "error": str(e)}


if __name__ == "__main__":
    print("Testing Groq API Keys...")
    res1 = test_groq_key("GROQ_API_KEY", settings.GROQ_API_KEY)
    res2 = test_groq_key("GROQ_API_KEY2", settings.GROQ_API_KEY2)

    output = {"key1_status": res1, "key2_status": res2}
    print(json.dumps(output, indent=2))
