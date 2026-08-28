import os
import chromadb
from sentence_transformers import SentenceTransformer


# Step 1: Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Step 2: Read text file
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Step 3: Split text into chunks
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks


# Step 4: Create embeddings
def create_embedding(text):
    embedding = embedding_model.encode(text)
    return embedding.tolist()


# Step 5: Store chunks in ChromaDB
def store_in_chromadb(chunks):
    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_or_create_collection(name="course_notes")

    for index, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{index}"]
        )

    print("Data stored successfully in ChromaDB")


# Main execution
if __name__ == "__main__":
    file_path = os.path.join("data", "course_notes.txt")

    text = read_file(file_path)

    chunks = split_text(text)

    store_in_chromadb(chunks)

    print("Ingestion completed successfully")