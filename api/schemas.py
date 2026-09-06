from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    query: str = Field(..., min_length=1, description="Student's natural language query")
    roll_no: Optional[str] = Field(None, description="Student roll number, if applicable")


class ChatResponse(BaseModel):
    session_id: str
    response: str
    agent_used: str
    latency_ms: float


class HistoryTurn(BaseModel):
    query: str
    response: str
    agent_used: str


class HistoryResponse(BaseModel):
    session_id: str
    turns: List[HistoryTurn]


class ResetResponse(BaseModel):
    session_id: str
    message: str
