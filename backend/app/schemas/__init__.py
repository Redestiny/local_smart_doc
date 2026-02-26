from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Document schemas
class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    file_path: Optional[str]
    is_processed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentChunkResponse(BaseModel):
    id: int
    chunk_index: int
    content: str
    
    class Config:
        from_attributes = True


class DocumentWithChunks(DocumentResponse):
    chunks: List[DocumentChunkResponse] = []
    
    class Config:
        from_attributes = True


# Conversation schemas
class ConversationCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=500)


class ConversationResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    sources: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True


# Q&A schemas
class QARequest(BaseModel):
    question: str = Field(..., min_length=1)
    conversation_id: Optional[int] = None
    top_k: int = Field(default=5, ge=1, le=20)


class SourceData(BaseModel):
    content: str
    metadata: dict


class QAResponse(BaseModel):
    answer: str
    sources: List[dict] = []
    conversation_id: int
    message_id: int


class SearchResult(BaseModel):
    content: str
    metadata: dict
