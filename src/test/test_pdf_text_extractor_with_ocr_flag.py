from ingest.pdf_extractor import PDFTextExtractor

FILE_PATH = "data/raw/Energieausweis Allach (1).pdf"  # Or any PDF you have

extractor = PDFTextExtractor()
chunks, metadata = extractor.extract_text(FILE_PATH)

print(f"\n📄 Extracted {len(chunks)} usable chunks from {metadata.filename}")

for i, chunk in enumerate(chunks):
    print("=" * 60)
    print(f"🔹 Chunk {i+1} — Page {chunk.page_num}")
    print(chunk.content[:300])
