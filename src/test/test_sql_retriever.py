from retrieve.sql_retriever import search_sql_chunks

def test_sql_retriever_by_language():
    chunks = search_sql_chunks(language="en")  # or try "de" if your test docs are German
    assert chunks, "❌ No chunks found in SQLite for language='en'"

    print(f"✅ Retrieved {len(chunks)} chunks from SQLite:")
    for c in chunks[:3]:
        print(f"- {c.doc_id} | Page {c.page_num} | Lang: {c.language}")
        print(c.content[:150])
        print("—" * 40)

if __name__ == "__main__":
    test_sql_retriever_by_language()
