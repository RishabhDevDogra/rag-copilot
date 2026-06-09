from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# simple in-memory memory store
SESSION_STORE = {}


class AskRequest(BaseModel):
    session_id: str
    question: str


@router.post("/ask")
def ask(req: AskRequest):

    history = SESSION_STORE.get(req.session_id, [])
    history.append(req.question)
    SESSION_STORE[req.session_id] = history

    return {
        "session_id": req.session_id,
        "question": req.question,
        "history": history,
        "answer": f"You asked {len(history)} question(s). This is a dummy response."
    }