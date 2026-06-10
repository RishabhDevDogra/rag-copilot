# RAG Copilot Service

A production-minded FastAPI backend that demonstrates retrieval-augmented support workflows with typed APIs, vector search, background job processing, and structured observability.

This project is intentionally scoped as a practical engineering baseline for AI-enabled backend roles (Java/Python, APIs, distributed patterns, secure coding, testing, and cloud-native readiness).

## What It Does

- Exposes a `POST /ask` API for multi-turn Q&A with retrieval-backed citations.
- Stores embeddings in Qdrant and retrieves relevant sections for each question.
- Exposes a `POST /webhooks/ticket-created` API to accept support events and enqueue async work.
- Runs a background worker that processes queued tickets through a simple agent decision flow.
- Emits structured JSON logs with request IDs for end-to-end traceability.
- Includes a one-command smoke test to validate core API flows.

## Current Architecture

- API layer: FastAPI + Pydantic models
- Retrieval layer: Sentence Transformers (`all-MiniLM-L6-v2`) + Qdrant
- Async processing: In-memory queue + background worker
- Logging: JSON logs with per-request correlation IDs
- Validation: Bash smoke test for health, ask, and webhook paths

## Project Structure

```text
app/
  main.py                 # app bootstrap, middleware, worker lifecycle
  api/
    ask.py                # /ask endpoint
    webhooks.py           # /webhooks/ticket-created endpoint
  core/
    logging.py            # structured JSON logger
    middleware.py         # request ID middleware
  models/
    schemas.py            # typed request/response models
  services/
    retriever.py          # Qdrant retrieval
    ticket_agent.py       # intent/action logic for ticket jobs
    ticket_worker.py      # async queue worker
    tools.py              # mock tool actions
scripts/
  ingest.py               # seed data -> vectors into Qdrant
  smoke_test.sh           # quick endpoint verification
docker-compose.yml        # local Qdrant service
```

## Quick Start

### 1) Start Qdrant

```bash
docker compose up -d
```

### 2) Seed vector data

```bash
./venv/bin/python scripts/ingest.py
```

### 3) Run the API

```bash
./venv/bin/uvicorn app.main:app --reload --port 8001
```

### 4) Run smoke tests

```bash
./scripts/smoke_test.sh
```

## Manual API Examples

### Health

```bash
curl -i http://127.0.0.1:8001/health
```

### Ask (RAG + citations)

```bash
curl -i -X POST http://127.0.0.1:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"session_id":"s1","question":"How does Stripe auth work?"}'
```

### Ticket webhook (enqueue async work)

```bash
curl -i -X POST http://127.0.0.1:8001/webhooks/ticket-created \
  -H "Content-Type: application/json" \
  -d '{"ticket_id":"t1","session_id":"s1","customer_email":"demo@example.com","subject":"Payment API auth error","body":"Invoice call failed with auth error","priority":"high"}'
```

## Engineering Qualities Demonstrated

- API engineering: typed contracts, validation, clean endpoint boundaries.
- Distributed systems fundamentals: asynchronous queue/worker processing pattern.
- AI application engineering: embeddings + vector retrieval + citation-aware response payloads.
- Operational readiness: structured logs, request correlation IDs, deterministic smoke checks.
- Security baseline: input validation via Pydantic models, explicit payload schemas, controlled tool calls.

## Current Limitations (Honest State)

- Agent logic is rule-based and does not call an external LLM yet.
- Queue is in-memory (good for dev/demo, not durable for production).
- Session memory is process-local.
- CI/CD, infra-as-code, and full test pyramid are next steps.

## Next Production Steps

- Replace in-memory queue with Redis/RabbitMQ.
- Add durable session/ticket state (PostgreSQL/Redis).
- Add unit + integration tests with coverage gates.
- Add retry/timeout/degraded-mode behavior for model and vector failures.
- Add latency metrics and dashboard integration.

## Why This Project Is Relevant to AI Cybersecurity Engineering

- Combines secure API design with AI retrieval workflows.
- Uses modern AI building blocks (embeddings, vector search, retrieval, agent actions).
- Demonstrates production engineering habits: observability, async workflows, validation, and runnable checks.
- Provides a practical base to extend into threat-intel retrieval, incident triage agents, and secure automation.
