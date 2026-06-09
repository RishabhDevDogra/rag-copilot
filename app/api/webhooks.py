from __future__ import annotations

import logging
from uuid import uuid4

from fastapi import APIRouter, Request

from app.models.schemas import (
    TicketCreatedPayload,
    TicketJob,
    TicketWebhookResponse,
)
from app.services.ticket_worker import enqueue_ticket_job

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger("app.webhooks")


@router.post("/ticket-created", response_model=TicketWebhookResponse)
async def ticket_created(payload: TicketCreatedPayload, request: Request) -> TicketWebhookResponse:
    request_id = request.state.request_id
    job = TicketJob(
        job_id=str(uuid4()),
        request_id=request_id,
        payload=payload,
    )
    await enqueue_ticket_job(job)

    logger.info(
        "webhook.ticket_created.queued",
        extra={
            "request_id": request_id,
            "job_id": job.job_id,
            "ticket_id": payload.ticket_id,
            "session_id": payload.session_id,
        },
    )

    return TicketWebhookResponse(
        request_id=request_id,
        job_id=job.job_id,
        status="queued",
    )
