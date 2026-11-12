import streamlit as st
import torch

from tokenizer import vocab
from model import MiniLLM

st.title("🧠 Mini LLM")

# Model configuration
VOCAB_SIZE = len(vocab)
EMBEDDING_DIM = 16

id_to_word = {i: word for word, i in vocab.items()}

# Load model
@st.cache_resource
def load_model():
    model = MiniLLM(VOCAB_SIZE, EMBEDDING_DIM)

    model.load_state_dict(
        torch.load("mini_model.pth", map_location="cpu", weights_only=True)
    )

    model.eval()
    return model

try:
    model = load_model()
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# Generate text
def generate_text(prompt, max_words=10):
    words = prompt.lower().strip().split()

    if not words:
        return "Please enter a prompt."

    if any(word not in vocab for word in words):
        return "Prompt contains words not found in vocabulary."

    with torch.no_grad():
        for _ in range(max_words):
            token_ids = [vocab[word] for word in words]
            x = torch.tensor([token_ids], dtype=torch.long)

            prediction = model(x)
            next_id = prediction.argmax(dim=-1).item()

            next_word = id_to_word[next_id]
            words.append(next_word)

    return " ".join(words)

# Streamlit UI
prompt = st.text_input(
    "Enter your prompt",
    placeholder="Example: india capital is"
)

max_words = st.slider(
    "Number of words to generate",
    1, 20, 5
)

if st.button("Generate"):
    if prompt.strip():
        result = generate_text(prompt, max_words)
        st.write("### Generated Text")
        st.write(result)
    else:
        st.warning("Please enter a prompt.")
