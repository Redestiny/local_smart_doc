from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    app_name: str = "Local Smart Doc"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://postgres:postgres@db:5432/local_smart_doc"
    
    # ChromaDB
    chroma_persist_directory: str = "/data/chroma"
    
    # OpenAI
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-ada-002"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
