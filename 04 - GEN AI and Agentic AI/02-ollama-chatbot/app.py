import streamlit as st
from ollama_service import ask_ollama


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Ollama Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# Page Header
# ============================================================

st.title("🤖 Ollama Chatbot")
st.caption("Powered by Llama 3.2")


# ============================================================
# Chat Input
# ============================================================

question = st.chat_input("Ask me anything...")


# ============================================================
# Process Question
# ============================================================

if question:

    # User message
    with st.chat_message("user"):
        st.write(question)

    # Assistant message
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = ask_ollama(question)

        st.write(answer)
