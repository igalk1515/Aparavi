from ingest.pdf_extractor import PDFTextExtractor
from transform.text_chunker import chunk_text
from transform.language_detector import detect_language
from models.data_models import ContentChunk
import uuid

PDF_PATH = "data/raw/20220714449_invoice_70449.pdf"
CHUNK_SIZE = 50  # words

def run_etl():
    print(f"\n🚀 Running ETL on file: {PDF_PATH}")
    
    extractor = PDFTextExtractor()
    pages, metadata = extractor.extract_text(PDF_PATH)

    all_chunks = []

    for page in pages:
        print("=" * 60)
        print(f"📄 Page {page.page_num} — Raw Length: {len(page.content.split())} words")

        chunks = chunk_text(page.content, max_tokens=CHUNK_SIZE)

        for i, chunk_text in enumerate(chunks):
            lang = detect_language(chunk_text)
            chunk_id = f"{metadata.doc_id}_p{page.page_num}_c{i}_{uuid.uuid4().hex[:6]}"

            chunk = ContentChunk(
                chunk_id=chunk_id,
                doc_id=metadata.doc_id,
                page_num=page.page_num,
                content=chunk_text,
                content_type="text",
                language=lang,
                metadata={"source": "run_etl"}
            )

            print(f"\n🔹 Chunk {i+1} (Page {page.page_num}, lang={lang})")
            print(chunk_text[:400])  # Display start of chunk
            all_chunks.append(chunk)

    print(f"\n✅ Total chunks created: {len(all_chunks)}")

if __name__ == "__main__":
    run_etl()
