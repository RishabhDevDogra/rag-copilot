#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8001}"

pass() {
  echo "PASS: $1"
}

fail() {
  echo "FAIL: $1"
  exit 1
}

echo "Running smoke tests against ${BASE_URL}"

health_response=$(curl -sS -o /tmp/rag_health.json -w "%{http_code}" "${BASE_URL}/health")
[[ "${health_response}" == "200" ]] || fail "GET /health returned ${health_response}"
grep -q '"status":"ok"' /tmp/rag_health.json || fail "GET /health payload missing status=ok"
pass "GET /health"

ask_payload='{"session_id":"smoke-session","question":"How does Stripe auth work?"}'
ask_response=$(curl -sS -o /tmp/rag_ask.json -w "%{http_code}" -X POST "${BASE_URL}/ask" -H "Content-Type: application/json" -d "${ask_payload}")
[[ "${ask_response}" == "200" ]] || fail "POST /ask returned ${ask_response}"
grep -q '"answer":' /tmp/rag_ask.json || fail "POST /ask payload missing answer"
grep -q '"citations":' /tmp/rag_ask.json || fail "POST /ask payload missing citations"
pass "POST /ask"

webhook_payload='{"ticket_id":"smoke-ticket-1","session_id":"smoke-session","customer_email":"demo@example.com","subject":"Payment API auth error","body":"Invoice call failed with auth error","priority":"high"}'
webhook_response=$(curl -sS -o /tmp/rag_webhook.json -w "%{http_code}" -X POST "${BASE_URL}/webhooks/ticket-created" -H "Content-Type: application/json" -d "${webhook_payload}")
[[ "${webhook_response}" == "200" ]] || fail "POST /webhooks/ticket-created returned ${webhook_response}"
grep -q '"status":"queued"' /tmp/rag_webhook.json || fail "Webhook payload missing status=queued"
grep -q '"job_id":' /tmp/rag_webhook.json || fail "Webhook payload missing job_id"
pass "POST /webhooks/ticket-created"

echo "All smoke tests passed."
