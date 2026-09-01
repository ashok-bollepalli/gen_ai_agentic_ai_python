import streamlit as st

from main import ask_gpt


# ============================================================
# Streamlit Page Configuration
# ============================================================

st.set_page_config(
    page_title="OpenAI GPT Chatbot",
    page_icon="🤖"
)


# ============================================================
# Application Title
# ============================================================

st.title("🤖 OpenAI GPT Chatbot")


# ============================================================
# Get Input from User
# ============================================================

input = st.chat_input("Enter your prompt...")


# ============================================================
# Call ask_gpt() Function
# ============================================================

if input:

    # Display User Input
    with st.chat_message("user"):

        st.write(input)


    # Call GPT
    with st.chat_message("assistant"):

        with st.spinner("Generating response..."):

            output = ask_gpt(input)


        # Display GPT Response
        st.write(output)