from openai import OpenAI
from infrastructure.config import OPENAI_API_KEY, CHAT_MODEL, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def create_embeddings(text_list):
    """Convert a list of text chunks into vectors."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text_list
    )
    return [item.embedding for item in response.data]

def rewrite_query(question):
    """Rewrite an unclear question into a better search query."""
    prompt = f"""
Rewrite this question as a clear search query.
Do not answer the question. Return only the rewritten query.

Question: {question}
"""
    response = client.responses.create(
        model=CHAT_MODEL,
        input=prompt
    )
    return response.output_text.strip()

def rerank_chunks(question, chunks):
    """Ask the LLM to rank retrieved chunks by relevance."""
    if not chunks:
        return []

    passages = ""
    for i, chunk in enumerate(chunks):
        passages += f"\nCHUNK {i}: {chunk['text'][:1000]}\n"

    prompt = f"""
Rank these chunks based on how well they answer the question.
Return ONLY the chunk numbers in best-to-worst order, separated by commas.
Example: 2,0,1

Question: {question}
Chunks:
{passages}
"""
    response = client.responses.create(
        model=CHAT_MODEL,
        input=prompt
    )

    try:
        order = [int(value.strip()) for value in response.output_text.split(",")]
        ranked = []
        for index in order:
            if 0 <= index < len(chunks) and chunks[index] not in ranked:
                item = dict(chunks[index])
                item["rerank_score"] = len(order) - len(ranked)
                ranked.append(item)

        for chunk in chunks:
            if chunk["chunk_id"] not in [item["chunk_id"] for item in ranked]:
                item = dict(chunk)
                item["rerank_score"] = 0
                ranked.append(item)

        return ranked
    except (ValueError, TypeError):
        return chunks

def generate_answer(question, chunks):
    """Generate an answer using only the retrieved chunks."""
    context = ""

    for chunk in chunks:
        source = chunk["metadata"].get("source", "unknown")
        context += f"\nSOURCE: {source}\n{chunk['text']}\n"

    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present, say:
"I could not find this information in the knowledge base."
Do not make up facts. Mention source filenames in your answer.

Question: {question}

Context:
{context}

Answer:
"""
    response = client.responses.create(
        model=CHAT_MODEL,
        input=prompt
    )
    return response.output_text.strip()
