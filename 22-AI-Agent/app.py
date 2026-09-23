import streamlit as st

from customer_agent import customer_support

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="centered"
)

# ==========================================
# HEADER
# ==========================================

st.title("🤖 AI Customer Support")

st.write(
    "Ask questions about your order, check order status, "
    "or cancel an order."
)

# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# DISPLAY PREVIOUS MESSAGES
# ==========================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# USER INPUT
# ==========================================

question = st.chat_input(
    "Ask something about your order..."
)

# ==========================================
# PROCESS QUESTION
# ==========================================

if question:

    # -------------------------------
    # Display user message
    # -------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # -------------------------------
    # AI response
    # -------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                answer = customer_support(question)

                st.write(answer)

                # Save response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )
