"""
聊天问答端点
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

router = APIRouter()

class ChatRequest(BaseModel):
    """聊天请求"""
    question: str
    document_ids: list[str] = []
    history: list[dict] = []

class ChatResponse(BaseModel):
    """聊天响应"""
    answer: str
    sources: list[dict]
    processing_time: float

@router.post("/ask")
async def ask_question(request: ChatRequest):
    """
    提问问题
    """
    logger.info(f"Question received: {request.question}")
    
    # 占位实现
    return ChatResponse(
        answer=f"This is a placeholder response for: {request.question}",
        sources=[
            {"document": "example.pdf", "page": 1, "score": 0.95}
        ],
        processing_time=0.1
    )

@router.get("/history")
async def get_chat_history():
    """
    获取聊天历史
    """
    return {
        "message": "Get chat history",
        "history": [],
        "status": "not_implemented"
    }

@router.delete("/history")
async def clear_chat_history():
    """
    清空聊天历史
    """
    return {
        "message": "Chat history cleared",
        "status": "not_implemented"
    }
