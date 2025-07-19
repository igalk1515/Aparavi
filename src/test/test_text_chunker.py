from transform.text_chunker import chunk_text
from ingest.pdf_extractor import PDFTextExtractor

FILE_PATH = "data/raw/20220714449_invoice_70449.pdf"

extractor = PDFTextExtractor()
pages, _ = extractor.extract_text(FILE_PATH)

text = pages[0].content  # Use first chunk only

chunks = chunk_text(text, max_tokens=50)  # Small for testing

print(f"\n🔹 Original text length: {len(text.split())} words")
print(f"🔹 Generated {len(chunks)} chunks\n")

for i, chunk in enumerate(chunks):
    print("="*60)
    print(f"📄 Chunk {i+1}")
    print(chunk)
