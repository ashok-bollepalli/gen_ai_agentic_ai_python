from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    EMBEDDING_MODEL
)


# =====================================================
# OPENAI LLM
# =====================================================

llm = ChatOpenAI(
    model=LLM_MODEL,
    api_key=OPENAI_API_KEY
)


# =====================================================
# OPENAI EMBEDDINGS
# =====================================================

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=OPENAI_API_KEY
)