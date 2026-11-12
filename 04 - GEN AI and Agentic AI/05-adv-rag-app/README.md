# Beginner Advanced RAG - Clean Architecture

This version is designed for Python beginners. It uses simple functions and dictionaries. It does not use classes or custom OOP.

## Folder structure

```text
advanced_rag/
│
├── app.py
├── domain/
├── application/
│   ├── chunking.py
│   ├── ingest.py
│   └── retrieve.py
├── infrastructure/
│   ├── config.py
│   ├── document_loader.py
│   ├── openai_service.py
│   ├── chroma_store.py
│   └── bm25_search.py
├── data/
├── requirements.txt
└── README.md
```

`domain/` is intentionally empty in this first beginner version because the workflow uses simple dictionaries instead of custom model classes.

## Setup

1. Install Python 3.10 or later.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Open `infrastructure/config.py` and replace the placeholder with your OpenAI API key.
5. Run:

```bash
streamlit run app.py
```

6. Click **Ingest / Rebuild Documents** in the sidebar.
7. Ask a question.

## What students learn

| File | Concept |
|---|---|
| `document_loader.py` | Read TXT documents |
| `chunking.py` | Split documents into chunks |
| `openai_service.py` | Embeddings, query rewriting, reranking, answer |
| `chroma_store.py` | Store and search vectors |
| `bm25_search.py` | Keyword search |
| `ingest.py` | Document ingestion workflow |
| `retrieve.py` | Advanced retrieval workflow |
| `app.py` | User interface |

## Why ChromaDB?

ChromaDB is a persistent vector database. It saves embeddings, text and metadata in the local `chroma_db` folder. It is not necessary to regenerate document embeddings for every question. Re-ingest only when source documents change.

BM25 is rebuilt from the TXT files in memory when a question is asked. This keeps the demo easy to understand. For a larger application, persist the keyword index too.

## Advanced RAG techniques shown

1. Query rewriting
2. Chunking with overlap
3. OpenAI embeddings
4. ChromaDB semantic search
5. BM25 keyword search
6. Hybrid search using Reciprocal Rank Fusion (RRF)
7. LLM-based reranking
8. Grounded answer generation with source names

## Sample questions

- What topics are covered in the Gen AI course?
- Explain hybrid search.
- What is chunk overlap?
- Explain Spring Boot dependency injection.
- What is the difference between semantic search and keyword search?

## Teaching note

This is an educational demo. It uses simple character chunking and an LLM-based reranking prompt so learners can inspect the logic. A production system should use stronger document parsing, persistent keyword indexing, a dedicated reranker, evaluation, security controls and monitoring.
