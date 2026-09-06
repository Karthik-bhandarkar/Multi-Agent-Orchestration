import time
import sys
from typing import Any, Dict, Optional
from src.agents.base_agent import BaseAgent, AgentResult
from src.agents.agent_factory import AgentFactory
from src.tools.marks_tool import student_marks_tool
from src.rag.vector_store import VectorStore
from src.db.student_repository import StudentRepository
from src.tools.safe_calculator import SafeMathParser
from src.tools.safety_guardrail import check_crisis
from src.utils.exception import CustomException
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Vector Store Singleton
_vector_store_singleton = None


def get_vector_store() -> VectorStore:
    global _vector_store_singleton
    if _vector_store_singleton is None:
        _vector_store_singleton = VectorStore()
        _vector_store_singleton.load_index()
    return _vector_store_singleton


# ==================== SPECIALIST 1: DATA RETRIEVAL ====================
class DataRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="DataRetrievalAgent", domain="student_records")

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        start = time.perf_counter()
        try:
            roll_no = (context or {}).get("roll_no")
            if not roll_no:
                return AgentResult(
                    agent_name=self.name,
                    status="FAILURE",
                    content="No roll number provided in context.",
                    latency_ms=(time.perf_counter() - start) * 1000,
                )

            result_text = student_marks_tool.invoke({"roll_no": roll_no})
            return AgentResult(
                agent_name=self.name,
                status="SUCCESS",
                content=result_text,
                metadata={"roll_no": roll_no},
                latency_ms=(time.perf_counter() - start) * 1000,
            )
        except Exception as e:
            logger.error(f"DataRetrievalAgent failed: {e}")
            raise CustomException(e, sys) from e


# ==================== SPECIALIST 2: KNOWLEDGE RAG ====================
class KnowledgeRAGAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="KnowledgeRAGAgent", domain="policy_knowledge")

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        start = time.perf_counter()
        try:
            vs = get_vector_store()
            results = vs.search(query, top_k=2)

            if not results or results[0]["score"] < 0.4:
                content = "I couldn't find a confident answer in the academic policy documents."
                status = "FAILURE"
            else:
                content = results[0]["text"]
                status = "SUCCESS"

            return AgentResult(
                agent_name=self.name,
                status=status,
                content=content,
                metadata={"top_score": results[0]["score"] if results else 0.0},
                latency_ms=(time.perf_counter() - start) * 1000,
            )
        except Exception as e:
            raise CustomException(e, sys) from e


# ==================== SPECIALIST 3: ANALYTICS REPORT ====================
class AnalyticsReportAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AnalyticsReportAgent", domain="performance_analytics")
        self.calculator = SafeMathParser()

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        start = time.perf_counter()
        try:
            roll_no = (context or {}).get("roll_no")
            if not roll_no:
                return AgentResult(
                    agent_name=self.name,
                    status="FAILURE",
                    content="No roll number provided for analytics.",
                    latency_ms=(time.perf_counter() - start) * 1000,
                )

            with StudentRepository() as repo:
                summary = repo.get_student_summary(roll_no)

            if "error" in summary:
                return AgentResult(
                    agent_name=self.name,
                    status="FAILURE",
                    content=summary["error"],
                    latency_ms=(time.perf_counter() - start) * 1000,
                )

            content = (
                f"Performance Report for {summary['student_name']}:\n"
                f"Average Score: {summary['avg_score']:.2f}\n"
                f"Average Attendance: {summary['avg_attendance']:.2f}%\n"
                f"Academic Standing: {summary['status']}"
            )

            return AgentResult(
                agent_name=self.name,
                status="SUCCESS",
                content=content,
                metadata=summary,
                latency_ms=(time.perf_counter() - start) * 1000,
            )
        except Exception as e:
            raise CustomException(e, sys) from e


# ==================== SPECIALIST 4: CRITICAL GUARDRAIL ====================
class CriticalGuardrailAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="CriticalGuardrailAgent", domain="safety")

    def execute(self, query: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        start = time.perf_counter()
        crisis_result = check_crisis(query)

        if crisis_result:
            helpline_text = "\n".join([f"- {k}: {v}" for k, v in crisis_result["helplines"].items()])
            content = f"{crisis_result['message']}\n\nImmediate Support:\n{helpline_text}"
            status = "ESCALATED"
        else:
            content = "No crisis indicators detected."
            status = "SUCCESS"

        return AgentResult(
            agent_name=self.name,
            status=status,
            content=content,
            latency_ms=(time.perf_counter() - start) * 1000,
        )


# ============ FACTORY REGISTRATION (module load time) ============
AgentFactory.register("DATA_RETRIEVAL", DataRetrievalAgent)
AgentFactory.register("KNOWLEDGE_RAG", KnowledgeRAGAgent)
AgentFactory.register("ANALYTICS", AnalyticsReportAgent)
AgentFactory.register("GUARDRAIL", CriticalGuardrailAgent)
