def create_chunks(documents, chunk_size=700, overlap=100):
    """Split each document into small overlapping text pieces."""
    all_chunks = []

    for document in documents:
        text = document["text"]
        start = 0
        chunk_number = 1

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                all_chunks.append({
                    "chunk_id": f"{document['source']}-{chunk_number}",
                    "text": chunk_text,
                    "metadata": {
                        "source": document["source"],
                        "chunk_number": str(chunk_number)
                    }
                })

            if end >= len(text):
                break

            start = end - overlap
            chunk_number += 1

    return all_chunks
