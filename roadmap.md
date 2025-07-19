Perfect — here's a clear **ETL-to-RAG roadmap** for implementing your full Hybrid Multi-Modal RAG pipeline, in **recommended order**.

---

## 🧭 Full Project Implementation Roadmap

---

### ✅ PHASE 1: Ingestion & Extraction (Done ✅ or In Progress 🟡)

| Step | Component               | File                                 | Status  | Purpose                                 |
| ---- | ----------------------- | ------------------------------------ | ------- | --------------------------------------- |
| 1    | PyMuPDF Text Extraction | `pdf_extractor.py`                   | ✅ Done | Extract machine-readable text per page  |
| 2    | Detect unreadable pages | `_needs_ocr()` in `pdf_extractor.py` | ✅ Done | Decide if page needs OCR                |
| 3    | OCR Placeholder (stub)  | `TODO` inside extractor              | ✅ Done | Plan for Google Vision OCR integration  |
| 4    | Chunking                | `text_chunker.py`                    | ✅ Done | Split text into embedding-ready chunks  |
| 5    | Language Detection      | `language_detector.py`               | ✅ Done | Tag each chunk as "en" or "de"          |
| 6    | Metadata + Chunk IDs    | `metadata.py` or inside extractor    | ✅ Done | Add doc ID, page number, chunk ID, etc. |

---

### 🏗 PHASE 2: Transformation & Storage

| Step | Component                  | File                 | Status  | Purpose                                       |
| ---- | -------------------------- | -------------------- | ------- | --------------------------------------------- |
| 7    | Store Chunks in Qdrant     | `vector_store.py`    | ✅ Done | Push chunks with embeddings                   |
| 8    | Store Table Rows in SQLite | `sql_store.py`       | ✅ Done | Save extracted tables from invoices, etc.     |
| 9    | Table Extraction (Camelot) | `table_extractor.py` | ✅ Done | Extract structured rows from PDFs with tables |

---

### 🧠 PHASE 3: Retrieval & Generation (RAG)

| Step | Component             | File                    | Status  | Purpose                                      |
| ---- | --------------------- | ----------------------- | ------- | -------------------------------------------- |
| 10   | Vector Retrieval      | `vector_retriever.py`   | ✅ Done | Fetch top-k chunks from Qdrant               |
| 11   | SQL Table Retrieval   | `sql_retriever.py`      | ✅ Done | Fetch relevant rows from structured data     |
| 12   | Hybrid Retriever      | `hybrid_retriever.py`   | ✅ Done | Combine vector + SQL retrieval               |
| 13   | GPT Answer Generation | `response_generator.py` | ✅ Done | Generate final response with source citation |

---

### 🤖 PHASE 4: Agentic Orchestration

| Step | Component             | File           | Status  | Purpose                                          |
| ---- | --------------------- | -------------- | ------- | ------------------------------------------------ |
| 14   | ETL Agent (LangGraph) | `etl_graph.py` | ✅ Done | Automate ingest → OCR → chunk → store            |
| 15   | RAG Agent (LangGraph) | `rag_graph.py` | ✅ Done | Automate retrieval → generation → source linking |

---

### 📊 PHASE 5: Evaluation

| Step | Component                 | File                    | Status  | Purpose                                   |
| ---- | ------------------------- | ----------------------- | ------- | ----------------------------------------- |
| 16   | Arize Phoenix Integration | `phoenix_evaluator.py`  | ✅ Done | Trace and evaluate answers                |
| 17   | Compute F1 / Precision    | `metrics_calculator.py` | ✅ Done | Reach ≥0.85 F1 score from challenge sheet |

---

## 🔁 Support Scripts

| Script       | Purpose                          |
| ------------ | -------------------------------- |
| `run_etl.py` | Runs manual ETL before LangGraph |
| `run_rag.py` | Runs QA pipeline manually        |
| `test/*.py`  | Individual unit tests            |

---

## 🧠 Bonus (Optional Enhancements)

| Feature            | Why Useful                        |
| ------------------ | --------------------------------- |
| Knowledge Graph    | Bonus points for entity-aware RAG |
| OCR page rendering | More accurate OCR from images     |
| LangChain tools    | Could simplify LangGraph flows    |
