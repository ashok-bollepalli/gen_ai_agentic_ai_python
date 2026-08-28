import streamlit as st
from ollama_service import ask_ollama


st.set_page_config(
    page_title="Ollama Gen AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Gen AI Chatbot using Ollama")
st.write("Ask anything. This chatbot runs using a local Ollama model.")


# Store chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Explain clearly and simply."
        }
    ]


# Display previous messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])


# Take user input
user_question = st.chat_input("Ask your question here...")


if user_question:
    # Display user message
    with st.chat_message("user"):
        st.write(user_question)

    # Add user message to history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_response = ask_ollama(st.session_state.messages)
            st.write(ai_response)

    # Add assistant response to history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )