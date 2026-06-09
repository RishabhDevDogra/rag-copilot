from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.ask import router as ask_router
from app.api.webhooks import router as webhooks_router
from app.core.logging import configure_logging
from app.core.middleware import RequestContextMiddleware
from app.services.ticket_worker import run_ticket_worker

configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    stop_event = asyncio.Event()
    worker_task = asyncio.create_task(run_ticket_worker(stop_event))
    try:
        yield
    finally:
        stop_event.set()
        await worker_task

app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestContextMiddleware)

app.include_router(ask_router)
app.include_router(webhooks_router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}