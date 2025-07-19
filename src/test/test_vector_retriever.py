from retrieve.vector_retriever import search_vector

def test_search_vector():
    chunks = search_vector("What is the invoice amount?")
    assert chunks, "❌ No chunks returned from vector search."

    print("✅ Retrieved Chunks:")
    for i, c in enumerate(chunks):
        print(f"\n🔹 Chunk {i+1} (Page {c.page_num}, lang={c.language})")
        print(c.content[:300] + "...\n")

if __name__ == "__main__":
    test_search_vector()
