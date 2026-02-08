"""
配置管理
"""
import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator

class Settings(BaseSettings):
    """应用配置"""
    
    # 基础配置
    APP_NAME: str = "Local Smart Doc"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据目录
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = DATA_DIR / "uploads"
    VECTOR_DB_DIR: Path = DATA_DIR / "vector_db"
    
    # 文档处理
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx"]
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # 向量数据库
    VECTOR_DB_PROVIDER: str = "chroma"  # chroma | qdrant
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Ollama配置
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    
    # RAG配置
    SIMILARITY_TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[Path] = DATA_DIR / "logs" / "app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @validator("DATA_DIR", "UPLOAD_DIR", "VECTOR_DB_DIR", pre=True)
    def create_dirs(cls, v: Path) -> Path:
        """确保目录存在"""
        v.mkdir(parents=True, exist_ok=True)
        return v

# 全局配置实例
settings = Settings()
