import os
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_INDEX_NAME = "ashok-it-knowledge"

LLM_MODEL = "gpt-5.6"

EMBEDDING_MODEL = "text-embedding-3-small"