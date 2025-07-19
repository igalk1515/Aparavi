from retrieve.sql_retriever import search_sql_chunks

chunks = search_sql_chunks(language="en")

print(f"\n✅ Retrieved {len(chunks)} table rows:\n")
for chunk in chunks:
    print(f"- Page {chunk.page_num} | Doc: {chunk.doc_id}")
    print(f"  {chunk.content[:300]}...\n")
