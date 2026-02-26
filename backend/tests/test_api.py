import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Local Smart Doc" in response.json()["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_documents():
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_document():
    response = client.post("/api/v1/documents", json={
        "title": "Test Document",
        "content": "This is a test document content."
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Document"
    assert data["content"] == "This is a test document content."
    assert data["is_processed"] == False


def test_create_document_validation():
    response = client.post("/api/v1/documents", json={
        "title": "",
        "content": ""
    })
    assert response.status_code == 422


@patch('app.api.v1.endpoints.documents.rag_service')
def test_process_document(mock_rag_service):
    mock_rag_service.process_document.return_value = ["chunk1", "chunk2"]
    
    # First create a document
    create_resp = client.post("/api/v1/documents", json={
        "title": "Test",
        "content": "Test content"
    })
    doc_id = create_resp.json()["id"]
    
    # Then process it
    response = client.post(f"/api/v1/documents/{doc_id}/process")
    assert response.status_code == 200
    assert response.json()["is_processed"] == True


@patch('app.api.v1.endpoints.documents.rag_service')
def test_qa_endpoint(mock_rag_service):
    mock_rag_service.answer_question.return_value = (
        "Test answer",
        [{"content": "Source 1", "metadata": {"doc_id": 1}}]
    )
    
    response = client.post("/api/v1/qa", json={
        "question": "What is EV?",
        "top_k": 3
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "conversation_id" in data


@patch('app.api.v1.endpoints.documents.rag_service')
def test_search(mock_rag_service):
    mock_rag_service.search.return_value = [
        {"content": "Result 1", "metadata": {"doc_id": 1}}
    ]
    
    response = client.get("/api/v1/search", params={"q": "test", "top_k": 5})
    assert response.status_code == 200
    assert "results" in response.json()
