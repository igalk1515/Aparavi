# run_etl.py

from ingest.pdf_extractor import PDFTextExtractor
from transform.text_chunker import chunk_text
from transform.language_detector import detect_language
from models.data_models import ContentChunk
from ingest.table_extractor import extract_tables
from store.sql_store import store_table_rows

import uuid
import os

PDF_FILES = [
    # "data/raw/20220714449_invoice_70449.pdf",
    # "data/raw/license powerpoint ersatz_OCR 1.pdf",
    "data/raw/72682299427.pdf"
    
]

CHUNK_SIZE = 50  # words

def run_etl():
    for path in PDF_FILES:
        print(f"\n🚀 Running ETL on file: {path}")
        
        extractor = PDFTextExtractor()
        pages, metadata = extractor.extract_text(path)
        
        ocr_pages = extractor.ocr_pages
        tables = extract_tables(path)
        # Filter out OCR pages
        filtered_tables = [t for t in tables if t["page_num"] not in ocr_pages]
        # Add metadata
        for t in filtered_tables:
            t["doc_id"] = metadata.doc_id
        store_table_rows(filtered_tables)


        if filtered_tables:
            print(f"\n📊 Extracted {len(filtered_tables)} table rows from {metadata.filename}")
            for t in filtered_tables[:3]:  # Show a few samples
                print(f"📄 Table Page {t['page_num']}: {t['row']}")
        else:
            print("📭 No tables extracted or all skipped due to OCR.")

        all_chunks = []

        for page in pages:
            print("=" * 60)
            print(f"📄 Page {page.page_num} — Raw Length: {len(page.content.split())} words")

            chunks = chunk_text(page.content, max_tokens=CHUNK_SIZE)

            for i, chunk in enumerate(chunks):
                lang = detect_language(chunk)
                chunk_id = f"{metadata.doc_id}_p{page.page_num}_c{i}_{uuid.uuid4().hex[:6]}"

                chunk_obj = ContentChunk(
                    chunk_id=chunk_id,
                    doc_id=metadata.doc_id,
                    page_num=page.page_num,
                    content=chunk,
                    content_type="text",
                    language=lang,
                    metadata={"source": "run_etl"}
                )

                print(f"\n🔹 Chunk {i+1} (Page {page.page_num}, lang={lang})")
                print(chunk[:400])
                all_chunks.append(chunk_obj)

        print(f"\n✅ Total chunks created for {metadata.filename}: {len(all_chunks)}")

if __name__ == "__main__":
    run_etl()
