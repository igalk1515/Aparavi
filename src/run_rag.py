# src/run_rag.py

from graph.rag_graph import build_rag_graph

def main():
    rag = build_rag_graph()

    query = input("❓ Enter your question: ")
    state = {
        "query": query,
        "language": "",
        "retrieved_chunks": [],
        "answer": ""
    }

    print("\n🚀 Running RAG pipeline...")
    final = rag.invoke(state)

    print("\n✅ Final Answer:")
    print(final["answer"])

    # print("\n📄 Supporting Chunks:")
    # for chunk in final["retrieved_chunks"]:
    #     print(f"- Doc: {chunk.doc_id}, Page: {chunk.page_num}, Lang: {chunk.language}")
    #     print(f"  {chunk.content[:200]}...\n")

if __name__ == "__main__":
    main()
