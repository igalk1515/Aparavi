# src/ingest/pdf_extractor.py
import fitz
import os

from models.data_models import DocumentMetadata
from ingest.ocr_processor import run_ocr_with_google
from models.data_models import PageText

class PDFTextExtractor:
    def __init__(self):
        self.ocr_pages = []

    def extract_text(self, file_path):
        doc = fitz.open(file_path)
        pages = []

        doc_id = os.path.basename(file_path).replace(".", "_")
        metadata = DocumentMetadata(
            doc_id=doc_id,
            filename=os.path.basename(file_path),
            file_path=file_path,
            doc_type="PDF",
            num_pages=len(doc)
        )

        for i, page in enumerate(doc):
            text = page.get_text()

            if self._needs_ocr(text):
                print(f"⚠️ Page {i + 1} likely needs OCR")
                pix = page.get_pixmap(dpi=300)
                text = run_ocr_with_google(pix)
                self.ocr_pages.append(i + 1)

            if text.strip():
                pages.append(PageText(page_num=i + 1, content=text))

        return pages, metadata

    def _needs_ocr(self, text: str) -> bool:
        if len(text.strip()) < 20:
            return True
        non_ascii_ratio = sum(1 for c in text if ord(c) > 127) / max(len(text), 1)
        return non_ascii_ratio > 0.6
