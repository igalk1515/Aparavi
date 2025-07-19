from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, SearchRequest, PointStruct
from openai import OpenAI
from models.data_models import ContentChunk
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "content_chunks")
EMBED_MODEL = "text-embedding-3-small"

client = QdrantClient(QDRANT_URL)
openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def embed_text(text: str) -> list[float]:
    response = openai.embeddings.create(
        input=text,
        model=EMBED_MODEL
    )
    return response.data[0].embedding

def search_vector(query: str, k: int = 5) -> list[ContentChunk]:
    query_vec = embed_text(query)

    hits = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vec,
        limit=k
    )

    chunks = []
    for hit in hits:
        payload = hit.payload
        chunk = ContentChunk(
            chunk_id=payload["chunk_id"],
            doc_id=payload["doc_id"],
            page_num=payload["page_num"],
            content=payload["content"],
            language=payload.get("language"),
            content_type=payload.get("content_type", "text"),
            metadata=payload.get("metadata", {})
        )
        chunks.append(chunk)

    return chunks
