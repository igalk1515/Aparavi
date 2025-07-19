# src/retrieve/sql_retriever.py
import sqlite3
from models.data_models import ContentChunk
import os
import json

DB_PATH = os.getenv("SQLITE_DB_PATH", "data/sqlite/processed.db")

def search_sql_chunks(language: str = None, doc_id: str = None) -> list[ContentChunk]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT chunk_id, doc_id, page_num, content, language, content_type, metadata FROM content_chunks WHERE 1=1"
    params = []

    if language:
        query += " AND language = ?"
        params.append(language)
    if doc_id:
        query += " AND doc_id = ?"
        params.append(doc_id)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        metadata = json.loads(row[6]) if row[6] else {}
        chunk = ContentChunk(
            chunk_id=row[0],
            doc_id=row[1],
            page_num=row[2],
            content=row[3],
            language=row[4],
            content_type=row[5],
            metadata=metadata
        )
        results.append(chunk)

    return results
