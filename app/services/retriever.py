from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from app.models.schemas import Citation

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("localhost", port=6333)

COLLECTION = "stripe_docs"


def search_docs(query: str, top_k: int = 3) -> list[Citation]:
    vector = model.encode(query).tolist()
    try:
        results = client.query_points(
            collection_name=COLLECTION,
            query=vector,
            limit=top_k,
        )
    except Exception:
        return []

    points = getattr(results, "points", [])
    return [
        Citation(
            doc_id=(point.payload or {}).get("doc_id", "unknown_doc"),
            section_id=(point.payload or {}).get("section_id", "unknown_section"),
            text=(point.payload or {}).get("text", ""),
            score=float(point.score),
        )
        for point in points
        if point.payload and "text" in point.payload
    ]