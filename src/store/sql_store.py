# src/store/sql_store.py
import sqlite3
import os
import json

from typing import List
from models.data_models import ContentChunk

DB_PATH = "data/sqlite/processed.db"

def create_tables():
    """
    Create the table_rows table if it doesn't exist.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS table_rows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT NOT NULL,
                page_num INTEGER NOT NULL,
                table_index INTEGER NOT NULL,
                row_json TEXT NOT NULL
            );
        """)
        conn.commit()

def create_content_chunks_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_chunks (
                chunk_id TEXT PRIMARY KEY,
                doc_id TEXT NOT NULL,
                page_num INTEGER,
                content TEXT,
                language TEXT,
                content_type TEXT,
                metadata TEXT
            );
        """)
        conn.commit()


def store_content_chunks(chunks: List[ContentChunk]):
    create_content_chunks_table()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for chunk in chunks:
            cursor.execute("""
                INSERT OR REPLACE INTO content_chunks (
                    chunk_id, doc_id, page_num, content, language, content_type, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                chunk.chunk_id,
                chunk.doc_id,
                chunk.page_num,
                chunk.content,
                chunk.language,
                chunk.content_type,
                json.dumps(chunk.metadata or {}, ensure_ascii=False)
            ))
        conn.commit()


def store_table_rows(rows: List[dict]):
    """
    Store table rows in SQLite.
    Each row must have: doc_id, page_num, table_index, and row.
    """
    create_tables()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for row in rows:
            cursor.execute("""
                INSERT INTO table_rows (doc_id, page_num, table_index, row_json)
                VALUES (?, ?, ?, ?);
            """, (
                row.get("doc_id"),
                row.get("page_num"),
                row.get("table_index"),
                json.dumps(row.get("row"), ensure_ascii=False)
            ))
        conn.commit()
