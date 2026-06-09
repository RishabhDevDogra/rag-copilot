from __future__ import annotations


def create_escalation(ticket_id: str, reason: str) -> str:
    return f"Escalation created for ticket {ticket_id}: {reason}"


def draft_reply(ticket_id: str, body: str) -> str:
    return f"Draft reply generated for ticket {ticket_id}: {body}"
