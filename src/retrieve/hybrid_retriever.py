# src/retrieve/hybrid_retriever.py

from typing import List
from models.data_models import ContentChunk
from retrieve.vector_retriever import search_vector
from retrieve.sql_retriever import search_sql_chunks
from transform.language_detector import detect_language

def hybrid_search(query: str, k: int = 5) -> List[ContentChunk]:
    print(f"🧠 Running hybrid search for: '{query}'")

    lang = detect_language(query)
    print(f"🌐 Detected query language: {lang}")

    vector_chunks = search_vector(query, k=k)
    sql_chunks = search_sql_chunks(language=lang, limit=5)

    print(f"Retrieved {len(vector_chunks)} vector chunks")
    print(f"Retrieved {len(sql_chunks)} SQL chunks")

    return vector_chunks + sql_chunks
