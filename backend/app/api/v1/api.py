"""
API路由定义
"""
from fastapi import APIRouter

from app.api.v1.endpoints import documents, chat, health

api_router = APIRouter()

# 注册路由
api_router.include_router(health.router, tags=["health"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
