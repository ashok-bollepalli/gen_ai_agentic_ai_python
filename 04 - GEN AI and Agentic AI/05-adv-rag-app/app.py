import streamlit as st

from infrastructure.config import OPENAI_API_KEY, CHAT_MODEL
from infrastructure.document_loader import load_documents
from infrastructure.chroma_store import add_chunks, search_vectors, get_chunk_count, clear_database
from infrastructure.bm25_search import search_bm25
from infrastructure.openai_service import rewrite_query, rerank_chunks, generate_answer
from application.chunking import create_chunks
from application.ingest import ingest_documents
from application.retrieve import retrieve_documents

st.set_page_config(page_title="Beginner Advanced RAG", page_icon="🧠")
st.title("🧠 Advanced RAG - Beginner Project")
st.write("Query Rewriting + ChromaDB + BM25 + Hybrid Search + Reranking")

if not OPENAI_API_KEY:
    st.error("Set OPENAI_API_KEY in infrastructure/config.py first.")
    st.stop()

st.sidebar.header("Knowledge Base")
st.sidebar.write(f"Stored chunks in ChromaDB: {get_chunk_count()}")

if st.sidebar.button("Ingest / Rebuild Documents"):
    with st.spinner("Reading documents, splitting chunks and saving embeddings..."):
        total = ingest_documents()
    st.sidebar.success(f"Indexed {total} chunks.")
    st.rerun()

if get_chunk_count() == 0:
    st.info("Click 'Ingest / Rebuild Documents' in the sidebar before asking a question.")

question = st.text_input("Ask a question", placeholder="What topics are covered in the Gen AI course?")
top_k = st.slider("Number of final chunks", 1, 6, 3)

if st.button("Search and Generate Answer", type="primary") and question.strip():
    with st.spinner("Rewriting query and searching documents..."):
        result = retrieve_documents(question, top_k)

    st.subheader("1. Query Rewriting")
    st.write("**Original question:**", question)
    st.write("**Rewritten question:**", result["rewritten_query"])

    st.subheader("2. Retrieved and Reranked Chunks")
    for number, chunk in enumerate(result["chunks"], start=1):
        with st.expander(f"Result {number} - {chunk['metadata'].get('source', 'unknown')}"):
            st.write(chunk["text"])
            st.caption(
                f"Hybrid score: {chunk['hybrid_score']:.4f} | "
                f"Rerank score: {chunk.get('rerank_score', 0):.1f}"
            )

    with st.spinner("Generating answer from retrieved context..."):
        answer = generate_answer(question, result["chunks"])

    st.subheader("3. Final Answer")
    st.markdown(answer)

st.divider()
st.caption("Documents → Chunking → Embeddings → ChromaDB + BM25 → Query Rewrite → Hybrid Search → Reranking → Answer")
