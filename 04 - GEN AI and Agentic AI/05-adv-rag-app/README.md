# Customer Support Assistant using Corrective RAG

A beginner-friendly Python project that answers customer questions from PDF documents using:
- PDF text extraction
- Simple text chunking
- OpenAI embeddings
- ChromaDB vector database
- Corrective RAG (relevance grading + query rewriting + second retrieval)
- OpenAI chat model
- Streamlit user interface

## 1. Architecture

```text
PDF files
   |
   v
PDF Loader -> Text Chunker -> OpenAI Embeddings -> ChromaDB
                                                   ^
                                                   |
Customer Question -> Initial Retrieval ------------+
                         |
                         v
                 Relevance Checker
                   /          \
             Relevant       Not relevant
                |                |
                |          Rewrite Question
                |                |
                |          Second Retrieval
                |                |
                |          Relevance Checker
                |             /       \
                |        Relevant   Not relevant
                |            |          |
                +------------+          v
                     |          Safe "not found" response
                     v
              Answer Generator
                     |
                     v
             Customer Answer
```

## 2. Clean architecture (simple version)

```text
project/
|-- app.py
|-- data/
|-- chroma_db/                 # created automatically
|-- src/
    |-- config.py              # API and model configuration
    |-- ingestion/
    |   |-- pdf_loader.py      # reads PDF files
    |   |-- chunker.py         # splits text into chunks
    |-- vector_store/
    |   |-- chroma_store.py    # embeddings and vector search
    |-- rag/
        |-- corrective_rag.py  # retrieval correction and answer generation
```

Each folder has one responsibility. The code uses simple functions instead of classes so beginners can follow the flow.

## 3. Setup

Use Python 3.10 or later.

### Windows

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

### Configure API key

Copy `.env.example` to `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_real_api_key
CHAT_MODEL=gpt-4.1-mini
EMBEDDING_MODEL=text-embedding-3-small
```

## 4. Add PDFs

Copy your customer documents into the `data/` folder. For example:
- product_manual.pdf
- refund_policy.pdf
- shipping_policy.pdf
- customer_faq.pdf

The PDFs should contain selectable text. Scanned PDFs need OCR before ingestion.

## 5. Run

```bash
streamlit run app.py
```

1. Click **Index PDFs** in the sidebar.
2. Enter a customer question.
3. Click **Get answer**.
4. Expand **View source chunks** to inspect the retrieved text.

## 6. Corrective RAG explained

Basic RAG retrieves chunks and immediately generates an answer.

Corrective RAG adds a quality check:

1. Retrieve the top matching chunks from ChromaDB.
2. Ask the LLM to grade whether those chunks are useful for the question.
3. If relevant, generate an answer from those chunks.
4. If not relevant, rewrite the question into a better search query.
5. Search ChromaDB again using the rewritten query.
6. Grade the second retrieval.
7. If the second retrieval is still weak, do not guess. Return a safe "not found" message.

This demo uses a second retrieval as its correction strategy. It does not search the public web because customer support answers should stay grounded in the supplied company documents.

## 7. Teaching example

Question: "Can I return a product after 20 days?"

- First retrieval may return general product information.
- Relevance checker decides that the chunks do not explain the return period.
- Query rewriter may produce: "product return eligibility return window number of days".
- ChromaDB performs a second search.
- If the refund policy PDF contains the answer, the assistant responds using that policy.
- If no useful policy is found, the assistant says it cannot find the information.

## 8. Important beginner notes

- **Chunking:** splits long PDF pages into smaller pieces for search.
- **Embedding:** converts text into number vectors that represent meaning.
- **Vector database:** stores vectors and finds semantically similar chunks.
- **Relevance grading:** checks whether retrieved chunks can answer the question.
- **Query rewriting:** improves the search phrase when the first search is poor.
- **Grounded generation:** tells the LLM to answer only from retrieved PDF content.

## 9. Demo limitations / production improvements

This is a classroom demo, not a production support system. For production:
- Add OCR for scanned PDFs.
- Use stronger chunking that respects headings and paragraphs.
- Keep document IDs and versions; update only changed documents instead of deleting the collection.
- Add metadata filters for product, language, and document version.
- Add citations with exact page numbers in the final answer.
- Add authentication, logging, rate limits, evaluation datasets, and human handoff.
- Consider hybrid search and a reranker for larger document collections.
- Do not expose API keys in frontend code.
