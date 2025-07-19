import sqlite3
import os

DB_PATH = "data/sqlite/processed.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("🧹 Deleted SQLite database.")
else:
    print("ℹ️ No existing SQLite DB to delete.")
