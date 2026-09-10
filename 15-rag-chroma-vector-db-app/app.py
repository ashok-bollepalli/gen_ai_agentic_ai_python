import streamlit as st
from rag import ask_question

st.title("Company RAG Chatbot")

st.write(
    "Ask questions about the company documents."
)


question = st.text_input(
    "Enter your question:"
)

if st.button("Ask question"):
    if question:
      answer = ask_question(question)
      st.subheader("Answer")
      st.write(answer)
    else:
        st.warning("Please enter a question")