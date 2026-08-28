import streamlit as st
import chromadb
import requests
from sentence_transformers import SentenceTransformer


# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="course_notes")


# Convert question into embedding
def create_embedding(text):
    embedding = embedding_model.encode(text)
    return embedding.tolist()


# Search relevant chunks from vector database
def retrieve_context(question, top_k=3):
    question_embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context


# Send prompt to Ollama
def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Error: Unable to get response from Ollama"


# Generate final answer using RAG
def generate_answer(question):
    context = retrieve_context(question)

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using only the given context.
If the answer is not available in the context, say:
"I don't have enough information in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = ask_ollama(prompt)

    return answer, context


# Streamlit UI
st.set_page_config(
    page_title="RAG Chatbot with Vector DB",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RAG Chatbot with ChromaDB")
st.write("Ask questions from your course notes.")

question = st.text_input("Enter your question:")

if st.button("Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching documents and generating answer..."):
            answer, context = generate_answer(question)

        st.subheader("AI Answer")
        st.write(answer)

        with st.expander("Retrieved Context"):
            st.write(context)