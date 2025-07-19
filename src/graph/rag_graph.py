# rag_graph.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from models.data_models import ContentChunk
from transform.language_detector import detect_language
from retrieve.hybrid_retriever import hybrid_search
from generate.response_generator import generate_answer

class RAGState(TypedDict):
    query: str
    language: str
    retrieved_chunks: List[ContentChunk]
    answer: str

def detect_query_language(state: RAGState) -> RAGState:
    lang = detect_language(state["query"])
    state["language"] = lang
    return state

def retrieve_chunks(state: RAGState) -> RAGState:
    chunks = hybrid_search(state["query"], k=5)
    state["retrieved_chunks"] = chunks
    return state

def answer_with_gpt(state: RAGState) -> RAGState:
    answer = generate_answer(state["query"], state["retrieved_chunks"])
    state["answer"] = answer
    return state

def build_rag_graph():
    builder = StateGraph(RAGState)
    builder.add_node("detect_language", detect_query_language)
    builder.add_node("retrieve_chunks", retrieve_chunks)
    builder.add_node("generate", answer_with_gpt)

    builder.set_entry_point("detect_language")
    builder.add_edge("detect_language", "retrieve_chunks")
    builder.add_edge("retrieve_chunks", "generate")
    builder.add_edge("generate", END)

    return builder.compile()
