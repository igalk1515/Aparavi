from graph.rag_graph import build_rag_graph
from pprint import pprint

rag = build_rag_graph()

# Define the query you want to test
input_state = {
    "query": "What is the invoice total?",
    "language": "",
    "retrieved_chunks": [],
    "answer": ""
}

print("🚀 Running RAG graph...")
final_state = rag.invoke(input_state)

print("\n✅ Final Answer:")
print(final_state["answer"])

print("\n📄 Supporting Chunks:")
for chunk in final_state["retrieved_chunks"]:
    print(f"- Doc: {chunk.doc_id}, Page: {chunk.page_num}, Lang: {chunk.language}")
    print(f"  {chunk.content[:200]}...\n")
