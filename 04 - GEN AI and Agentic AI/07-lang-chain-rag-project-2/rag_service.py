from langchain_core.output_parsers import StrOutputParser

from llm import llm
from vector_store import retriever
from prompts import RAG_PROMPT

# =====================================================
# CREATE Lang CHAIN Pipeline
# =====================================================

chain = RAG_PROMPT | llm | StrOutputParser()


# =====================================================
# EXPLAIN TOPIC
# =====================================================

def explain_topic(topic):
    # get docs from pinecone
    documents = retriever.invoke(topic)

    # check if docs found or not

    if not documents:
        return ("I don't have enough info abt this topic")

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # invoke lang chain pipeline
    answer = chain.invoke({
        "topic": topic,
        "context": context
    })

    return answer
