from graph.rag_graph import retrieve_chunks

def test_retrieve_chunks_node():
    state = {"query": "What is the total amount?"}
    result = retrieve_chunks(state)
    chunks = result.get("retrieved_chunks", [])
    
    assert chunks, "❌ No chunks retrieved."
    print(f"✅ Retrieved {len(chunks)} chunks:")
    for c in chunks:
        print(f"- Page {c.page_num} | Lang: {c.language}")
        print(c.content[:200])
        print("—" * 40)

if __name__ == "__main__":
    test_retrieve_chunks_node()
