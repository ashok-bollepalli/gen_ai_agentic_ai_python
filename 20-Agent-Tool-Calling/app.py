import streamlit as st

from customer_support_bot import customer_support


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖"
)


# ==========================================
# TITLE
# ==========================================

st.title("🤖 AI Customer Support Agent")

st.write(
    "Ask me about your order."
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Available Tools")

    st.write("📦 Get Order Status")
    st.write("❌ Cancel Order")

    st.divider()

    st.write("Try:")

    st.write("Where is my order ORD1001?")

    st.write("Cancel order ORD1003")


# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# DISPLAY MESSAGES
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ==========================================
# CHAT INPUT
# ==========================================

question = st.chat_input(
    "Ask about your order..."
)


# ==========================================
# PROCESS QUESTION
# ==========================================

if question:

    # Show customer message

    with st.chat_message("user"):

        st.write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    # Get AI response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                answer = customer_support(question)

                st.write(answer)

            except Exception as e:

                answer = "Something went wrong."

                st.error(e)


    # Save AI response

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
