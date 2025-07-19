# src/graph/etl_graph.py
import uuid

from langgraph.graph import StateGraph, END
from ingest.pdf_extractor import PDFTextExtractor
from ingest.table_extractor import extract_tables
from store.sql_store import store_table_rows
from store.vector_store import store_chunks
from transform.text_chunker import chunk_text
from transform.language_detector import detect_language
from models.data_models import ContentChunk
from store.sql_store import store_content_chunks  # at top

from typing import TypedDict, List
from models.data_models import ContentChunk, DocumentMetadata, PageText

class ETLState(TypedDict):
    file_path: str
    pages: List[PageText]
    metadata: DocumentMetadata
    ocr_pages: List[int]
    tables: list
    chunks: List[ContentChunk]

def extract_pages(state):
    path = state["file_path"]
    extractor = PDFTextExtractor()
    pages, metadata = extractor.extract_text(path)

    # Store OCR page info in state
    state["pages"] = pages
    state["metadata"] = metadata
    state["ocr_pages"] = extractor.ocr_pages
    return state

def extract_tables_and_store(state):
    path = state["file_path"]
    tables = extract_tables(path)

    # Filter OCR pages (bad for Camelot)
    ocr_pages = state.get("ocr_pages", [])
    filtered_tables = [t for t in tables if t["page_num"] not in ocr_pages]

    for t in filtered_tables:
        t["doc_id"] = state["metadata"].doc_id

    store_table_rows(filtered_tables)

    print(f"\n📊 Stored {len(filtered_tables)} table rows")
    state["tables"] = filtered_tables
    return state

def chunk_and_store(state):
    chunks = []
    metadata = state["metadata"]
    CHUNK_SIZE = 50

    for page in state["pages"]:
        print("=" * 60)
        print(f"📄 Page {page.page_num} — Raw Length: {len(page.content.split())} words")

        page_chunks = chunk_text(page.content, max_tokens=CHUNK_SIZE)

        for i, chunk in enumerate(page_chunks):
            lang = detect_language(chunk)
            chunk_id = f"{metadata.doc_id}_p{page.page_num}_c{i}_{uuid.uuid4().hex[:6]}"

            chunk_obj = ContentChunk(
                chunk_id=chunk_id,
                doc_id=metadata.doc_id,
                page_num=page.page_num,
                content=chunk,
                content_type="text",
                language=lang,
                metadata={"source": "etl_graph"}
            )

            print(f"\n🔹 Chunk {i+1} (Page {page.page_num}, lang={lang})")
            print(chunk[:400])
            chunks.append(chunk_obj)

    store_chunks(chunks)
    store_content_chunks(chunks)  # after store_chunks()
    print(f"\n✅ Stored {len(chunks)} chunks for {metadata.filename}")
    state["chunks"] = chunks
    return state

# Graph builder
def build_etl_graph():
    builder = StateGraph(ETLState)

    builder.add_node("extract", extract_pages)
    builder.add_node("extract_tables", extract_tables_and_store)
    builder.add_node("chunk", chunk_and_store)

    builder.set_entry_point("extract")
    builder.add_edge("extract", "extract_tables")
    builder.add_edge("extract_tables", "chunk")
    builder.add_edge("chunk", END)

    return builder.compile()

