from __future__ import annotations

from app.models.schemas import AgentDecision, Citation, TicketCreatedPayload
from app.services.retriever import search_docs
from app.services.tools import create_escalation, draft_reply


def _choose_action(payload: TicketCreatedPayload) -> tuple[str, str]:
    text = f"{payload.subject} {payload.body}".lower()

    if any(keyword in text for keyword in ("outage", "down", "incident", "urgent")):
        return "escalate", "Detected production-impacting language in the ticket."
    if any(keyword in text for keyword in ("payment", "billing", "invoice", "api")):
        return "draft_reply", "Detected known product-support topic that can be answered directly."
    return "request_info", "Missing specifics needed to resolve the issue confidently."


def process_ticket(job_id: str, payload: TicketCreatedPayload) -> AgentDecision:
    query = f"{payload.subject}\n{payload.body}"
    citations: list[Citation] = search_docs(query, top_k=3)
    action, rationale = _choose_action(payload)

    if action == "escalate":
        tool_output = create_escalation(payload.ticket_id, rationale)
    elif action == "draft_reply":
        context = citations[0].text if citations else "Thanks for reaching out. We are investigating this now."
        tool_output = draft_reply(payload.ticket_id, context)
    else:
        tool_output = draft_reply(
            payload.ticket_id,
            "Can you share your account ID, exact steps, and timestamp so we can investigate?",
        )

    return AgentDecision(
        job_id=job_id,
        ticket_id=payload.ticket_id,
        action=action,
        rationale=rationale,
        citations=citations,
        tool_output=tool_output,
        status="completed",
    )
