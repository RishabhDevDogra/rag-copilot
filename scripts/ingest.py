from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

import uuid

model = SentenceTransformer("all-MiniLM-L6-v2")

client = QdrantClient("localhost", port=6333)

COLLECTION = "stripe_docs"

client.recreate_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

docs = [
    {
        "doc_id": "stripe_basics",
        "section_id": "intro",
        "text": "Stripe is a payment processing platform.",
    },
    {
        "doc_id": "stripe_auth",
        "section_id": "api_keys",
        "text": "Stripe uses API keys for authentication.",
    },
    {
        "doc_id": "stripe_events",
        "section_id": "webhooks",
        "text": "Stripe supports webhooks for event-driven systems.",
    },
    {
        "doc_id": "stripe_objects",
        "section_id": "customers_invoices_payments",
        "text": "Stripe allows creating customers, invoices, and payments.",
    },
    {
        "doc_id": "stripe_sdks",
        "section_id": "language_support",
        "text": "Stripe provides SDKs for Python, JavaScript, and Go.",
    },
]

points = []

for doc in docs:
    vector = model.encode(doc["text"]).tolist()

    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "doc_id": doc["doc_id"],
                "section_id": doc["section_id"],
                "text": doc["text"],
            },
        )
    )

client.upsert(collection_name=COLLECTION, points=points)

print("Stripe docs ingested successfully")