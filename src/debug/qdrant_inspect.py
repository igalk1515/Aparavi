from qdrant_client import QdrantClient
from pprint import pprint

client = QdrantClient(host="qdrant", port=6333)

COLLECTION_NAME = "content_chunks"

print("📚 Collection Info:")
collection_info = client.get_collection(COLLECTION_NAME)
pprint(collection_info.dict())

print("\n🔎 Sample Points:")
points = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=5,
    with_payload=True,
    with_vectors=False
)
for p in points[0]:
    pprint(p.payload)
