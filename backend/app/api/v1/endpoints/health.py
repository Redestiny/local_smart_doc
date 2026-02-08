"""
健康检查端点
"""
from fastapi import APIRouter
from loguru import logger

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    健康检查
    """
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "service": "local-smart-doc",
        "version": "0.1.0"
    }

@router.get("/ready")
async def readiness_check():
    """
    就绪检查
    """
    # 这里可以添加依赖服务检查（数据库、向量库等）
    return {
        "status": "ready",
        "dependencies": {
            "vector_db": "not_implemented",
            "ollama": "not_implemented"
        }
    }
