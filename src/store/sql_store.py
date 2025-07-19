# src/store/sql_store.py
import sqlite3
import os
import json
from typing import List

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
