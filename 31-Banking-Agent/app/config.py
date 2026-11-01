"""All settings in one place. Values come from the .env file."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
POLICY_DIR = DATA_DIR / "policies"
SCHEMA_FILE = DATA_DIR / "schema.sql"
CHROMA_DIR = BASE_DIR / "chroma_db"

# MySQL connection:  mysql+pymysql://<user>:<password>@<host>:<port>/<database>
DATABASE_URL = os.getenv("DATABASE_URL",
                         "mysql+pymysql://bank_user:bank_pass@localhost:3306/bank_db")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

API_URL = os.getenv("API_URL", "http://localhost:8000")
