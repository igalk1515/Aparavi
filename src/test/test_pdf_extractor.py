from ingest.pdf_extractor import PDFTextExtractor

extractor = PDFTextExtractor()
chunks, metadata = extractor.extract_text("data/raw/20220714449_invoice_70449.pdf")

print(f"\n📄 Extracted {len(chunks)} chunks from {metadata.filename}")
print(f"📎 Document Metadata:\n  - ID: {metadata.doc_id}\n  - Type: {metadata.doc_type}\n  - Pages: {metadata.num_pages}\n")

for i, chunk in enumerate(chunks):
    print("=" * 60)
    print(f"🔹 Chunk {i+1}")
    print(f"  - Page: {chunk.page_num}")
    print(f"  - Chunk ID: {chunk.chunk_id}")
    print(f"  - Language: {getattr(chunk, 'language', 'N/A')}")
    print(f"  - Content Type: {chunk.content_type}")
    print(f"  - Metadata: {chunk.metadata}")
    print(f"  - Content Preview:\n{chunk.content[:400]}...\n")
