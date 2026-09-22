import streamlit as st

from database.db import intialize_database
from graph.student_support_graph import graph


st.set_page_config(
    page_title="Student Support Chatbot",
    page_icon="🎓",
    layout="centered",
)

intialize_database()

st.title("🎓 Student Support Chatbot")
st.caption("LangGraph + Ollama + SQLite")

student_id = st.number_input(
    "Student ID",
    min_value=0,
    value=101,
    step=1,
)

question = st.text_input(
    "Ask your question",
    placeholder="Example: How much fee is pending?",
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            state = {
                "question": question.strip(),
                "student_id": int(student_id),
            }

            result = graph.invoke(state)

        st.subheader("Answer")
        st.write(result["answer"])

        with st.expander("Debug Information"):
            st.write("Category:", result.get("category"))
            st.write("Context:", result.get("context"))
