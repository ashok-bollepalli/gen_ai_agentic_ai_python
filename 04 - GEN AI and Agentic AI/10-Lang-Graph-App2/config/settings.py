from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DATABASE_NAME")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

OLLAMA_TEMPERATURE = os.getenv("OLLAMA_TEMPERATURE")

EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")