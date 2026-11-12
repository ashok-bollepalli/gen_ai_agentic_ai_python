
# Read text from file
with open("data.txt", "r") as file:
    text = file.read()

# Convert text to lowercase
text = text.lower()

# Split text into words
tokens = text.split()

# Create vocabulary (Word -> ID)
unique_words = sorted(set(tokens))

vocab = {}

for i, word in enumerate(unique_words):
    vocab[word] = i

# Create reverse vocabulary (ID -> Word)
reverse_vocab = {i: word for word, i in vocab.items()}

# Convert words into numbers
encoded_tokens = [vocab[word] for word in tokens]

# Convert numbers back into words
decoded_tokens = [reverse_vocab[i] for i in encoded_tokens]

# Display results
print("Original Text:", text)
print("=" * 50)
print("Tokens:", tokens)
print("=" * 50)
print("Vocabulary:", vocab)
print("=" * 50)
print("Encoded Tokens:", encoded_tokens)
print("=" * 50)
print("Decoded Text:", " ".join(decoded_tokens))
