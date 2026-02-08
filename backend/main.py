"""
Local Smart Doc - 后端主入口
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from app.core.config import settings
from app.api.v1.api import api_router

# 生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    # 启动时
    logger.info("🚀 Starting Local Smart Doc Backend")
    logger.info(f"📁 Data directory: {settings.DATA_DIR}")
    logger.info(f"🤖 Ollama URL: {settings.OLLAMA_BASE_URL}")
    
    # 创建必要目录
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
    
    yield
    
    # 关闭时
    logger.info("👋 Shutting down Local Smart Doc Backend")

# 创建FastAPI应用
app = FastAPI(
    title="Local Smart Doc API",
    description="本地智能文档问答系统后端API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    根端点 - 健康检查
    """
    return {
        "message": "Welcome to Local Smart Doc API",
        "version": "0.1.0",
        "docs": "/api/docs",
        "health": "/api/v1/health",
    }

@app.get("/health")
async def health_check():
    """
    健康检查端点
    """
    return {"status": "healthy", "service": "local-smart-doc"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
