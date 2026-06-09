from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient("localhost", port=6333)

COLLECTION = "stripe_docs"


def search_docs(query: str, top_k: int = 3):
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
        {
            "text": (point.payload or {}).get("text", ""),
            "score": point.score,
        }
        for point in points
        if point.payload and "text" in point.payload
    ]