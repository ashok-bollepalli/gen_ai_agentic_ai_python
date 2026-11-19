import streamlit as st
from src.ingestion.pdf_loader import load_pdf_folder
from src.ingestion.chunker import split_into_chunks
from src.vector_store.chroma_store import create_vector_store
from src.rag.corrective_rag import answer_customer_question

st.set_page_config(page_title="Customer Support - Corrective RAG", page_icon="📄")
st.title("📄 Customer Support Assistant")
st.caption("Ask questions using your PDF documentation. Powered by Corrective RAG.")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

with st.sidebar:
    st.header("1. Load PDF documents")
    if st.button("Index PDFs", use_container_width=True):
        with st.spinner("Reading PDFs and creating the vector database..."):
            documents = load_pdf_folder("data")
            if not documents:
                st.error("Add at least one PDF file to the data/ folder.")
            else:
                chunks = split_into_chunks(documents)
                st.session_state.vector_store = create_vector_store(chunks)
                st.success(f"Indexed {len(chunks)} text chunks.")
    st.info("Put your customer manuals, FAQs, policies, and product PDFs inside the data/ folder.")

st.header("2. Ask a customer question")
question = st.text_input("Customer question", placeholder="What is your refund policy?")
if st.button("Get answer", type="primary") and question.strip():
    if st.session_state.vector_store is None:
        st.warning("First click 'Index PDFs' in the sidebar.")
    else:
        with st.spinner("Checking document relevance and preparing an answer..."):
            result = answer_customer_question(question, st.session_state.vector_store)
        st.subheader("Answer")
        st.write(result["answer"])
        st.caption(f"Retrieval status: {result['status']}")
        if result["sources"]:
            with st.expander("View source chunks"):
                for i, source in enumerate(result["sources"], 1):
                    st.markdown(f"**Source {i}**")
                    st.write(source)
