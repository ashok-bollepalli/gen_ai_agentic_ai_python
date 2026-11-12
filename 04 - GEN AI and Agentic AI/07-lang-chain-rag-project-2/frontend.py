import streamlit as st

from rag_service import explain_topic


st.title("GEN AI Student Assistant")


topic = st.text_input(
    "Enter your question"
)


if st.button("Ask"):

    answer = explain_topic(topic)

    st.write(answer)