import os
from graph.etl_graph import build_etl_graph
from graph.rag_graph import build_rag_graph

ETL_PDFS = {
    "1": "72682299427.pdf",
    "2": "Energieausweis Allach.pdf"
}

RAW_DIR = "data/raw"

def run_etl(filename: str):
    graph = build_etl_graph()
    file_path = os.path.join(RAW_DIR, filename)
    print(f"\n🚀 Running ETL on: {filename}")
    result = graph.invoke({"file_path": file_path})
    print(f"✅ Finished — Pages: {len(result['pages'])}, Chunks: {len(result['chunks'])}")

def run_rag():
    rag = build_rag_graph()
    query = input("❓ Enter your question: ")

    input_state = {
        "query": query,
        "language": "",
        "retrieved_chunks": [],
        "answer": ""
    }

    print("\n🚀 Running RAG pipeline...")
    final_state = rag.invoke(input_state)

    print("\n✅ Final Answer:")
    print(final_state["answer"])

def main():
    while True:
        print("\n🧪 DEMO MENU")
        print("1: Run ETL on 72682299427.pdf")
        print("2: Run ETL on Energieausweis Allach.pdf")
        print("3: Ask a question")
        print("q: Quit")

        choice = input("👉 Choose an option: ").strip()

        if choice == "1":
            run_etl(ETL_PDFS["1"])
        elif choice == "2":
            run_etl(ETL_PDFS["2"])
        elif choice == "3":
            run_rag()
        elif choice.lower() == "q":
            print("👋 Exiting demo.")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
