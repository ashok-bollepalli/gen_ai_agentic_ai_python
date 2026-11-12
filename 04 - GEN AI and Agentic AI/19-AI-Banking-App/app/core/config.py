"""
Central configuration.
All values come from environment variables (.env locally, ConfigMap + Secret in Kubernetes).
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    # MySQL (AWS RDS)
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "bankdb"
    db_user: str = "admin"
    db_password: str = ""

    # Service URLs
    mcp_server_url: str = "http://localhost:8001/mcp"
    api_url: str = "http://localhost:8000"

    # RAG
    chroma_dir: str = "./chroma_db"
    knowledge_base_dir: str = "./knowledge_base"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
