# src/run_etl.py

from graph.etl_graph import build_etl_graph
import os

RAW_DIR = "data/raw"
PDF_FILES = [
    "20220714449_invoice_70449.pdf",
    "72682299427.pdf",
    "Energieausweis Allach (1).pdf",
    "Energieausweis Augsburg Karwendelstr. 167 germen.pdf",
    "license powerpoint ersatz_OCR 1.pdf"
]

if __name__ == "__main__":
    graph = build_etl_graph()

    for file in PDF_FILES:
        file_path = os.path.join(RAW_DIR, file)
        print(f"\n🚀 Running ETL on: {file}")
        result = graph.invoke({"file_path": file_path})

        print(f"✅ Finished {file} — Pages: {len(result['pages'])}, Chunks: {len(result['chunks'])}")
