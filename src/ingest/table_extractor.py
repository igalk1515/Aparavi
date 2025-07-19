# src/ingest/table_extractor.py

import camelot

def extract_tables(file_path: str, pages: str = "all") -> list[dict]:
    """
    Extract tables from a PDF using Camelot (stream flavor).
    Returns a list of dicts with row data and metadata.
    """
    try:
        tables = camelot.read_pdf(file_path, pages=pages, flavor="stream", strip_text="\n")
    except Exception as e:
        print(f"⚠️ Camelot error on file {file_path}: {e}")
        return []

    extracted = []

    for idx, table in enumerate(tables):
        print(f"📄 Table {idx} on page {table.page}, shape={table.df.shape}")
        df = table.df
        headers = df.iloc[0].tolist()

        for i in range(1, len(df)):
            row_data = dict(zip(headers, df.iloc[i].tolist()))
            extracted.append({
                "table_index": idx,
                "page_num": table.page,
                "row": row_data
            })

    return extracted
