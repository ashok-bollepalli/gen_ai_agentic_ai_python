from infrastructure.openai_service import create_embeddings, rewrite_query, rerank_chunks
from infrastructure.chroma_store import search_vectors
from infrastructure.document_loader import load_documents
from application.chunking import create_chunks
from infrastructure.bm25_search import search_bm25

def retrieve_documents(question, top_k=3):
    """Rewrite query, run vector + keyword search, combine and rerank."""

    # Step 1: Improve the user's question.
    rewritten_query = rewrite_query(question)

    # Step 2: Create an embedding for the rewritten question.
    query_embedding = create_embeddings([rewritten_query])[0]

    # Step 3: Semantic search in ChromaDB.
    vector_results = search_vectors(query_embedding, top_k=top_k * 3)

    # Step 4: Keyword search using BM25.
    documents = load_documents()
    all_chunks = create_chunks(documents)
    keyword_results = search_bm25(rewritten_query, all_chunks, top_k=top_k * 3)

    # Step 5: Combine both result lists using Reciprocal Rank Fusion.
    combined = {}

    for rank, chunk in enumerate(vector_results, start=1):
        combined[chunk["chunk_id"]] = dict(chunk)
        combined[chunk["chunk_id"]]["hybrid_score"] = 1 / (60 + rank)

    for rank, chunk in enumerate(keyword_results, start=1):
        chunk_id = chunk["chunk_id"]

        if chunk_id not in combined:
            combined[chunk_id] = dict(chunk)
            combined[chunk_id]["hybrid_score"] = 0

        combined[chunk_id]["hybrid_score"] += 1 / (60 + rank)

    candidates = sorted(
        combined.values(),
        key=lambda item: item["hybrid_score"],
        reverse=True
    )[:top_k * 3]

    # Step 6: LLM reranking.
    final_chunks = rerank_chunks(rewritten_query, candidates)[:top_k]

    return {
        "rewritten_query": rewritten_query,
        "chunks": final_chunks
    }
