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
    "Stripe is a payment processing platform.",
    "Stripe uses API keys for authentication.",
    "Stripe supports webhooks for event-driven systems.",
    "Stripe allows creating customers, invoices, and payments.",
    "Stripe provides SDKs for Python, JavaScript, and Go."
]

points = []

for text in docs:
    vector = model.encode(text).tolist()

    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": text}
        )
    )

client.upsert(collection_name=COLLECTION, points=points)

print("Stripe docs ingested successfully")