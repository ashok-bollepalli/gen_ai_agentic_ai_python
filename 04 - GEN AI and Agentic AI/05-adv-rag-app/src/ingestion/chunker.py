def split_into_chunks(documents, chunk_size=800, overlap=120):
    """Split page text into small overlapping pieces."""
    chunks = []

    for document in documents:
        text = document["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            piece = text[start:end].strip()

            if piece:
                chunks.append({
                    "text": piece,
                    "source": document["source"],
                    "page": document["page"]
                })

            start += chunk_size - overlap

    return chunks
