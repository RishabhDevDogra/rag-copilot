from __future__ import annotations

import asyncio
import logging

from app.models.schemas import TicketJob
from app.services.ticket_agent import process_ticket

logger = logging.getLogger("app.ticket_worker")

TICKET_QUEUE: asyncio.Queue[TicketJob] = asyncio.Queue()


async def enqueue_ticket_job(job: TicketJob) -> None:
    await TICKET_QUEUE.put(job)


async def run_ticket_worker(stop_event: asyncio.Event) -> None:
    logger.info("ticket_worker.started")

    while not stop_event.is_set():
        try:
            job = await asyncio.wait_for(TICKET_QUEUE.get(), timeout=0.5)
        except asyncio.TimeoutError:
            continue

        try:
            logger.info(
                "ticket_worker.job_started",
                extra={
                    "request_id": job.request_id,
                    "job_id": job.job_id,
                    "ticket_id": job.payload.ticket_id,
                },
            )
            decision = process_ticket(job.job_id, job.payload)
            logger.info(
                "ticket_worker.job_completed",
                extra={
                    "request_id": job.request_id,
                    "job_id": job.job_id,
                    "ticket_id": job.payload.ticket_id,
                    "action": decision.action,
                },
            )
        except Exception as exc:  # pragma: no cover - defensive branch
            logger.exception(
                "ticket_worker.job_failed",
                extra={
                    "request_id": job.request_id,
                    "job_id": job.job_id,
                    "ticket_id": job.payload.ticket_id,
                    "error": str(exc),
                },
            )
        finally:
            TICKET_QUEUE.task_done()

    logger.info("ticket_worker.stopped")
