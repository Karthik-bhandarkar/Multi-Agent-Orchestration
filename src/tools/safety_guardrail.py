"""
EduPulse AI — Safety & Crisis Intervention Guardrail Module
Tier-1 deterministic regex-based crisis detection system operating with sub-5ms latency.
Bypasses LLM execution when crisis/self-harm signals are detected to prevent hallucinated advice.
"""

import re
import time
from typing import Dict, Any, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Pre-compiled regex patterns with word boundaries to eliminate false positives
CRISIS_PATTERNS = {
    "suicide": re.compile(
        r"\b(suicide|suicidal|end my life|kill myself|want to die|take my life|no reason to live)\b",
        re.IGNORECASE,
    ),
    "self_harm": re.compile(
        r"\b(self harm|cut myself|harm myself|hurting myself|bleed out|overdose)\b",
        re.IGNORECASE,
    ),
    "hopelessness": re.compile(
        r"\b(can't go on|give up on life|everything is meaningless|better off dead|no hope left)\b",
        re.IGNORECASE,
    ),
    "severe_distress": re.compile(
        r"\b(extreme panic|unbearable pain|mental breakdown|can't take this anymore)\b",
        re.IGNORECASE,
    ),
}

EMERGENCY_HELPLINES = {
    "india_tele_manas": "14416 or 1800-891-4416 (24/7 Mental Health Helpline)",
    "vandrevala_foundation": "+91 9999 666 555 (24/7 Crisis Support)",
    "us_national_helpline": "988 (Suicide & Crisis Lifeline)",
    "kiran_mental_health": "1800-599-0019 (Govt of India Helpline)",
}


def check_crisis(text: str) -> Optional[Dict[str, Any]]:
    """
    Evaluates input text against pre-compiled crisis regex patterns.

    Args:
        text (str): Input text from user/student.

    Returns:
        Optional[Dict[str, Any]]: Crisis assessment dictionary if triggered, else None.
    """
    if not text or not isinstance(text, str):
        return None

    start_time = time.perf_counter()
    cleaned_text = text.strip()

    for category, pattern in CRISIS_PATTERNS.items():
        match = pattern.search(cleaned_text)
        if match:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            matched_phrase = match.group(0)

            logger.warning(
                f"CRISIS DETECTED [Category: {category}] [Trigger: '{matched_phrase}'] [Latency: {elapsed_ms:.3f}ms]"
            )

            return {
                "is_crisis": True,
                "risk_category": category,
                "matched_trigger": matched_phrase,
                "latency_ms": round(elapsed_ms, 3),
                "message": (
                    "⚠️ IMMEDIATE ASSISTANCE REQUIRED: We care about your well-being. "
                    "Please reach out to trusted emergency mental health services right away."
                ),
                "helplines": EMERGENCY_HELPLINES,
            }

    return None
