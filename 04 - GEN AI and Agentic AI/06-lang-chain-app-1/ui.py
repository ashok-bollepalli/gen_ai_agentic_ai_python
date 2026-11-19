import streamlit as st
from backend import explain_topic

st.title("My First LangChain Application")

topic = st.text_input("Enter a Topic")

if st.button("Generate Explanation"):
    if topic:
        with st.spinner("Generating response..."):
            response = explain_topic(topic)
            st.write(response)
    else:
        st.warning("Please enter a topic")