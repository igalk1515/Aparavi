import os
import uuid

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from models.data_models import ContentChunk

# ✅ Correct: No arguments passed. Reads OPENAI_API_KEY from environment.
openai_client = OpenAI()

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = 6333
COLLECTION_NAME = "content_chunks"

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def ensure_collection():
    if COLLECTION_NAME not in [col.name for col in client.get_collections().collections]:
        print(f"🆕 Creating Qdrant collection: {COLLECTION_NAME}")
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

def embed_text(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def store_chunks(chunks: list[ContentChunk]):
    ensure_collection()

    points = []
    for chunk in chunks:
        embedding = embed_text(chunk.content)
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id))  # stable, UUID format

        points.append(PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "doc_id": chunk.doc_id,
                "page_num": chunk.page_num,
                "language": chunk.language,
                "content": chunk.content,
                "metadata": chunk.metadata,
            }
        ))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Stored {len(points)} chunks in Qdrant.")
