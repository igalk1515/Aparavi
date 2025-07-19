from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchAny, Match
import os

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = 6333
COLLECTION_NAME = "content_chunks"

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

if COLLECTION_NAME in [c.name for c in client.get_collections().collections]:
    print(f"🧹 Deleting all points in '{COLLECTION_NAME}'...")
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(must=[]),  # ✅ correct format
        wait=True
    )
    print("✅ Qdrant collection cleared.")
else:
    print("❌ Collection not found.")
