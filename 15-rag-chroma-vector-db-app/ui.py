import streamlit as st
from rag import ask_question

st.title("Company RAG Chatbot")

st.write("Ask questions about the company documents.")

question = st.text_input("ask your question")

if st.button("Submit"):
    if question:
        with st.spinner("Searching company docs..."):
            answer = ask_question(question)
        st.subheader("Answer : ")
        st.write(answer)
    else:
        st.warning("Enter your question")
