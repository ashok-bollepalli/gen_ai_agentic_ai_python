
import streamlit as st
from rag import ask_question

# Page configuration
st.set_page_config(page_title="Customer Support AI")

st.title("💬 Customer Support AI")
st.write("Ask questions about our PDF documents.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get customer question
question = st.chat_input("Ask your question...")

if question:

    # Display user question
    st.chat_message("user").write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Generate AI answer
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = ask_question(question)

            st.write(answer)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
