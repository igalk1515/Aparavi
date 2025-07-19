# src/test/test_hybrid_retriever.py

from retrieve.hybrid_retriever import hybrid_search

results = hybrid_search("What is the invoice total?")

print(f"\n✅ Hybrid Result Chunks ({len(results)}):\n")
for chunk in results:
    print(f"- Doc: {chunk.doc_id} | Page {chunk.page_num} | Lang: {chunk.language} | Type: {chunk.content_type}")
    print(f"  {chunk.content[:300]}...\n")
