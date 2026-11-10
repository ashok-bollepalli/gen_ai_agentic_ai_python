import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_CLOUD = os.getenv("PINECONE_CLOUD")
PINECONE_REGION = os.getenv("PINECONE_REGION")

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME","customer-support-rag")

CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL","gpt-5.5")

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small")

EMBEDDING_DIMENSION = 1536

NAMESPACE = "customer-support"