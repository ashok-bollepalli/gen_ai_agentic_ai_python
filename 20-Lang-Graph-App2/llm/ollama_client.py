from langchain_ollama import ChatOllama
from config.settings import OLLAMA_MODEL, OLLAMA_TEMPERATURE

def get_llm():
    client = ChatOllama(
        model = OLLAMA_MODEL,
        temperature = OLLAMA_TEMPERATURE
    )

    return client
