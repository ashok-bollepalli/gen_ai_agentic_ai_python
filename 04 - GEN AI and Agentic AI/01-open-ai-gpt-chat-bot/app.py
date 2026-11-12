import streamlit as st
from main import ask_gpt

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="GPT Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main container */
    .main {
        max-width: 850px;
        margin: auto;
    }

    /* Header */
    .header {
        text-align: center;
        padding: 20px 0 10px 0;
    }

    .header h1 {
        font-size: 32px;
        margin-bottom: 5px;
    }

    .header p {
        color: #777;
        font-size: 15px;
    }

    /* Response box */
    .response-box {
        background-color: #f7f7f8;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid #e5e5e5;
        line-height: 1.6;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #888;
        font-size: 12px;
        margin-top: 30px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header">
    <h1>🤖 GPT Chatbot</h1>
    <p>Ask anything and get a response from an OpenAI GPT model</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# GPT MODEL SELECTION
# ============================================================

models = [
    "gpt-5",
    "gpt-5-mini",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4o",
    "gpt-4o-mini"
]

selected_model = st.selectbox(
    "Select GPT Model",
    models
)


# ============================================================
# USER INPUT
# ============================================================

user_input = st.text_area(
    "Enter your question",
    placeholder="Ask something...",
    height=150
)


# ============================================================
# ASK BUTTON
# ============================================================

if st.button("Send 🚀", use_container_width=True):

    if user_input.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            try:

                response = ask_gpt(
                    selected_model,
                    user_input
                )

                # ============================================
                # DISPLAY RESPONSE
                # ============================================

                st.markdown(
                    f"""
                    <div class="response-box">
                        <b>🤖 GPT Response</b>
                        <br><br>
                        {response}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(f"Error: {e}")


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Powered by OpenAI GPT
</div>
""", unsafe_allow_html=True)
