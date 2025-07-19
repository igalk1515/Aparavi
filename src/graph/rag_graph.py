from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from models.data_models import ContentChunk
from transform.language_detector import detect_language
from retrieve.vector_retriever import search_vector
# from generate.response_generator import generate_answer  # you'll build this soon

class RAGState(TypedDict):
    query: str
    language: str
    retrieved_chunks: List[ContentChunk]
    answer: str

# Node: detect_language
def detect_query_language(state: RAGState) -> RAGState:
    lang = detect_language(state["query"])
    print(f"🌐 Detected language: {lang}")
    state["language"] = lang
    return state

# Node: retrieve_chunks
def retrieve_chunks(state: RAGState) -> RAGState:
    chunks = search_vector(state["query"], top_k=5)
    state["retrieved_chunks"] = chunks
    return state

# Node: generate_answer (you’ll build next)
# def answer_with_gpt(state: RAGState) -> RAGState:
#     chunks = state["retrieved_chunks"]
#     query = state["query"]
#     answer = generate_answer(query, chunks)
#     state["answer"] = answer
#     return state

# Build the graph
def build_rag_graph():
    builder = StateGraph(RAGState)
    # builder.add_node("detect_language", detect_query_language)
    # builder.add_node("retrieve_chunks", retrieve_chunks)
    # builder.add_node("generate", answer_with_gpt)

    builder.set_entry_point("detect_language")
    builder.add_edge("detect_language", "retrieve_chunks")
    builder.add_edge("retrieve_chunks", "generate")
    builder.add_edge("generate", END)

    return builder.compile()
