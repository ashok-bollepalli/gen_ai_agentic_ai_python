
import streamlit as st

from graph import banking_graph
from rag import ingest_policy_documents

# Streamlit UI
st.title("🏦 Banking AI Chatbot")

st.write("Ask questions about bank accounts, transactions and policies.")

# Policy Document Ingestion
if st.button("Load Banking Policies"):

    ingest_policy_documents()

    st.success("Banking policies loaded successfully!")


# Chatbot
question = st.chat_input("Enter your question")

if question:

    # Display user question
    st.chat_message("user").write(question)

    # Execute LangGraph workflow
    result = banking_graph.invoke({
        "question": question
    })

    # Display AI response
    st.chat_message("assistant").write(
        result["answer"]
    )