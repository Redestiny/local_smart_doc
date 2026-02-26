from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import tempfile
import os
import json

from app.core.database import get_db, init_db
from app.models.database import Document, DocumentChunk, Conversation, Message
from app.schemas import (
    DocumentCreate, DocumentResponse, DocumentWithChunks,
    ConversationCreate, ConversationResponse, ConversationWithMessages,
    QARequest, QAResponse
)
from app.services.rag import rag_service

router = APIRouter()


@router.on_event("startup")
def startup():
    init_db()


# Document endpoints
@router.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(title=doc.title, content=doc.content)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


@router.get("/documents", response_model=List[DocumentResponse])
def list_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Document).offset(skip).limit(limit).all()


@router.get("/documents/{doc_id}", response_model=DocumentWithChunks)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/documents/{doc_id}/process", response_model=DocumentResponse)
def process_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    chunks = rag_service.process_document(doc.content, doc.id)
    
    for i, chunk_content in enumerate(chunks):
        chunk = DocumentChunk(
            document_id=doc.id,
            chunk_index=i,
            content=chunk_content
        )
        db.add(chunk)
    
    doc.is_processed = True
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return None


@router.post("/documents/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        with open(tmp_path, "r", encoding="utf-8") as f:
            text_content = f.read()
        
        doc = Document(title=file.filename or "Untitled", content=text_content, file_path=tmp_path)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
    finally:
        os.unlink(tmp_path)


# Conversation endpoints
@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(conv: ConversationCreate, db: Session = Depends(get_db)):
    db_conv = Conversation(title=conv.title)
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv


@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Conversation).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()


@router.get("/conversations/{conv_id}", response_model=ConversationWithMessages)
def get_conversation(conv_id: int, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


# Q&A endpoint
@router.post("/qa", response_model=QAResponse)
def ask_question(qa_req: QARequest, db: Session = Depends(get_db)):
    if qa_req.conversation_id:
        conv = db.query(Conversation).filter(Conversation.id == qa_req.conversation_id).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        title = qa_req.question[:100] if len(qa_req.question) > 100 else qa_req.question
        conv = Conversation(title=title)
        db.add(conv)
        db.commit()
        db.refresh(conv)
    
    user_message = Message(conversation_id=conv.id, role="user", content=qa_req.question)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    answer, sources = rag_service.answer_question(qa_req.question, qa_req.top_k)
    
    assistant_message = Message(
        conversation_id=conv.id,
        role="assistant",
        content=answer,
        sources=json.dumps(sources)
    )
    db.add(assistant_message)
    db.commit()
    
    return QAResponse(
        answer=answer,
        sources=sources,
        conversation_id=conv.id,
        message_id=assistant_message.id
    )


# Search endpoint
@router.get("/search")
def search_documents(q: str, top_k: int = 5):
    results = rag_service.search(q, top_k)
    return {"results": results}


# Health check
@router.get("/health")
def health_check():
    return {"status": "healthy"}
