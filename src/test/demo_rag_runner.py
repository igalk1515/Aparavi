# src/test/demo_rag_runner.py

from graph.rag_graph import build_rag_graph

# Build the RAG graph once
rag = build_rag_graph()

# List of demo questions
demo_queries = [
    "What is the total amount due on the Guidde Inc invoice?",
    "Was ist das Ziel des DOORS-KI-Tools?",
    "What license period is specified in the Efficient Elements invoice?",
]

print("🚀 Running RAG demo...\n")

for query in demo_queries:
    input_state = {
        "query": query,
        "language": "",
        "retrieved_chunks": [],
        "answer": ""
    }

    print(f"🧠 Query: {query}")
    final_state = rag.invoke(input_state)

    print(f"✅ Answer:\n{final_state['answer']}\n")

    print("📄 Supporting Chunks:")
    for chunk in final_state["retrieved_chunks"]:
        print(f"- Doc: {chunk.doc_id}, Page: {chunk.page_num}, Lang: {chunk.language}")
        print(f"  {chunk.content[:200]}...\n")

    print("=" * 80 + "\n")
