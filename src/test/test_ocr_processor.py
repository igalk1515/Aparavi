# src/test/test_ocr_processor.py

from fitz import open as open_pdf
from ingest.ocr_processor import run_ocr_with_google

def test_google_ocr():
    # Open your test PDF
    doc = open_pdf("data/raw/license powerpoint ersatz_OCR 1.pdf")
    page = doc[0]  # First page

    # Render to image (for OCR)
    pix = page.get_pixmap(dpi=300)

    # Run OCR
    text = run_ocr_with_google(pix)

    print("✅ OCR Text Output:")
    print("=" * 60)
    print(text)

if __name__ == "__main__":
    test_google_ocr()
