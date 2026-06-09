import logging

from fastapi import APIRouter, Request

from app.models.schemas import AskRequest, AskResponse, ConversationTurn
from app.services.retriever import search_docs

router = APIRouter()
logger = logging.getLogger("app.ask")

SESSION_STORE: dict[str, list[ConversationTurn]] = {}


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest, request: Request) -> AskResponse:
    request_id = request.state.request_id
    logger.info(
        "ask.received",
        extra={
            "request_id": request_id,
            "session_id": req.session_id,
        },
    )

    history = SESSION_STORE.get(req.session_id, [])
    history.append(ConversationTurn(role="user", content=req.question))
    SESSION_STORE[req.session_id] = history

    docs = search_docs(req.question)
    answer = docs[0].text if docs else "No relevant docs found"
    history.append(ConversationTurn(role="assistant", content=answer))

    response = AskResponse(
        request_id=request_id,
        session_id=req.session_id,
        question=req.question,
        answer=answer,
        citations=docs,
        history=history,
    )

    logger.info(
        "ask.completed",
        extra={
            "request_id": request_id,
            "session_id": req.session_id,
            "citation_count": len(docs),
        },
    )
    return response