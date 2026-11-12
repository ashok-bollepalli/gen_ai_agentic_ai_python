import re
from rank_bm25 import BM25Okapi

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9]+", text.lower())

def search_bm25(question, chunks, top_k=10):
    """Find chunks using keyword matching."""
    if not chunks:
        return []

    tokenized_chunks = [tokenize(chunk["text"]) for chunk in chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    scores = bm25.get_scores(tokenize(question))

    indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    results = []
    for index in indexes:
        item = dict(chunks[index])
        item["bm25_score"] = float(scores[index])
        results.append(item)

    return results
