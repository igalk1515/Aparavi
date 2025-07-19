# 🧠 Hybrid Multi-Modal RAG Pipeline — Aparavi Coding Challenge

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline capable of processing **multi-modal, multilingual PDF documents** — including invoices, tables, scanned files, and text in **English and German** — and answering questions with **document-grounded citations**.

---

## 🚀 Features

- ✅ **Multi-modal document ingestion** (scanned PDFs, machine-readable, tables)
- ✅ **Agentic OCR routing** (Google Vision API + Tesseract fallback)
- ✅ **Table extraction** (Camelot)
- ✅ **Hybrid retrieval** (vector + SQL)
- ✅ **Multilingual support** (English + German)
- ✅ **Source-cited answers** using GPT-4o
- ✅ **RAG evaluation** (F1, precision, recall)

---

## 🗂️ Architecture

```text
       ┌────────────┐
       │  PDF File  │
       └────┬───────┘
            │
     ┌──────▼──────┐
     │ OCR Agent   │──Google Vision / Tesseract
     └────┬───────┘
          │
 ┌────────▼────────┐
 │   Text + Tables │ ← Camelot + PyMuPDF
 └────────┬────────┘
          │
 ┌────────▼────────┐
 │ Chunking + Lang │ ← Text split + langdetect
 └────────┬────────┘
          │
 ┌────────▼─────────────┐
 │ Vector DB (Qdrant)   │ ← `store_chunks`
 │ SQL DB (SQLite)      │ ← `store_table_rows`
 └────────┬─────────────┘
          │
 ┌────────▼─────────────┐
 │ Hybrid Retriever      │ ← vector + SQL union
 └────────┬─────────────┘
          │
 ┌────────▼─────────────┐
 │ Answer Generator      │ ← GPT-4o with citations
 └──────────────────────┘
```

---

## 🧱 Tech Stack

| Component           | Tool / Lib                      |
| ------------------- | ------------------------------- |
| PDF Parsing         | PyMuPDF                         |
| OCR (fallback)      | Tesseract OCR                   |
| OCR (commercial)    | Google Vision API               |
| Table Extraction    | Camelot                         |
| Vector Store        | Qdrant                          |
| SQL Store           | SQLite                          |
| Embedding Model     | OpenAI `text-embedding-3-small` |
| RAG + QA            | GPT-4o                          |
| Graph Orchestration | LangGraph                       |
| Evaluation          | Arize Phoenix (planned)         |

---

## 🧪 Running the Project

### 1. 🐳 Prerequisites

- Docker + Docker Compose
- OpenAI API key (`OPENAI_API_KEY`)
- Google Vision credentials (optional, for full OCR agent)

### 2. 🏗️ ETL Pipeline

```bash
docker-compose run app python src/test/test_etl_graph.py
```

### 3. 🔍 RAG Inference

```bash
docker-compose run app python src/test/test_rag_graph_run.py
```

### 4. 🧪 Evaluation (Optional)

```bash
docker-compose run app python src/eval/evaluate_rag.py
```

---

## 🤖 OCR Decision Logic

The **OCR agent** runs only on pages with no extractable text:

- ✅ If PyMuPDF returns empty → run **Google Vision API**
- 🔁 If API quota fails → fallback to **Tesseract**

This saves cost and speeds up processing.

---

## 🧠 Hybrid Retrieval

```python
vector_chunks = search_vector(query, k=5)
sql_chunks = search_sql_chunks(language=detected_lang, limit=5)
```

The results are merged and passed to GPT-4o, ensuring both fuzzy and symbolic matches (especially from tables) are included.

---

## 🧾 Example Output

> **Question**: What is the invoice total?  
> **Answer**: The total is 101,63 EUR. _(doc: 72682299427_pdf, page: 1)_

---

## 🛠️ Evaluation Strategy

- Compare answers from GPT to ground-truth from the Q&A Excel
- Use precision, recall, and F1 metrics
- Evaluate both exact and partial match support

---

## 📁 Project Structure

```
├── ingest/
│   ├── pdf_extractor.py
│   ├── table_extractor.py
├── transform/
│   ├── text_chunker.py
│   ├── language_detector.py
├── store/
│   ├── vector_store.py
│   ├── sql_store.py
├── retrieve/
│   ├── sql_retriever.py
│   ├── vector_retriever.py
│   ├── hybrid_retriever.py
├── generate/
│   └── response_generator.py
├── graph/
│   ├── etl_graph.py
│   └── rag_graph.py
├── test/
│   ├── test_etl_graph.py
│   ├── test_rag_graph_run.py
│   ├── test_generate_answer.py
│   └── ...
```

---
