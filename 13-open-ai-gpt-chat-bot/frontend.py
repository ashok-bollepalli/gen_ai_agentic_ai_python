import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask-ai"

st.set_page_config(
    page_title="GEN AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 GEN AI Chatbot")
st.write("Simple chatbot using Streamlit, FastAPI and OpenAI GPT.")

# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_question = st.chat_input("Ask your question...")

if user_question:
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    # Call backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": user_question
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]

                    st.write(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                else:
                    st.error("Error from backend API.")

            except Exception as e:
                st.error("FastAPI backend is not running.")
                st.exception(e)
