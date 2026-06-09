from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Citation(BaseModel):
    doc_id: str
    section_id: str
    text: str
    score: float


class ConversationTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AskRequest(BaseModel):
    session_id: str = Field(min_length=1)
    question: str = Field(min_length=1)


class AskResponse(BaseModel):
    request_id: str
    session_id: str
    question: str
    answer: str
    citations: list[Citation]
    history: list[ConversationTurn]


class TicketCreatedPayload(BaseModel):
    ticket_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    customer_email: str = Field(min_length=3)
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)
    priority: Literal["low", "medium", "high", "urgent"] = "medium"


class TicketWebhookResponse(BaseModel):
    request_id: str
    job_id: str
    status: Literal["queued"]


class TicketJob(BaseModel):
    job_id: str
    request_id: str
    payload: TicketCreatedPayload


class AgentDecision(BaseModel):
    job_id: str
    ticket_id: str
    action: Literal["draft_reply", "escalate", "request_info"]
    rationale: str
    citations: list[Citation] = Field(default_factory=list)
    tool_output: str
    status: Literal["completed", "failed"]
