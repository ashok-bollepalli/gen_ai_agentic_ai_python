
import streamlit as st
from backend import ask_bot

st.title("🤖 AWS Bedrock AI Chatbot")

question = st.text_input("Enter your question")

if st.button("Ask AI"):

    if question.strip():

        with st.spinner("Generating answer..."):
            try:
                answer = ask_bot(question)

                st.subheader("AI Response")
                st.write(answer)

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning("Please enter a question.")
