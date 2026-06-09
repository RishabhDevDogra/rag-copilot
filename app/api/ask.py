from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retriever import search_docs

router = APIRouter()

SESSION_STORE = {}


class AskRequest(BaseModel):
    session_id: str
    question: str


@router.post("/ask")
def ask(req: AskRequest):

    history = SESSION_STORE.get(req.session_id, [])
    history.append(req.question)
    SESSION_STORE[req.session_id] = history

    docs = search_docs(req.question)

    return {
        "session_id": req.session_id,
        "question": req.question,
        "history": history,
        "retrieved_docs": docs,
        "answer": docs[0]["text"] if docs else "No relevant docs found"
    }