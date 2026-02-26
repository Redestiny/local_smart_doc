import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
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
        "content": "This is test content."
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Document"
    assert data["is_processed"] == False


def test_create_document_validation():
    response = client.post("/api/v1/documents", json={
        "title": "",
        "content": ""
    })
    assert response.status_code == 422


@patch('app.api.documents.rag_service')
def test_process_document(mock_rag):
    mock_rag.process_document.return_value = ["chunk1", "chunk2"]
    
    create_resp = client.post("/api/v1/documents", json={"title": "Test", "content": "Test content"})
    doc_id = create_resp.json()["id"]
    
    response = client.post(f"/api/v1/documents/{doc_id}/process")
    assert response.status_code == 200
    assert response.json()["is_processed"] == True


@patch('app.api.documents.rag_service')
def test_qa_endpoint(mock_rag):
    mock_rag.answer_question.return_value = ("Test answer", [{"content": "Source 1"}])
    
    response = client.post("/api/v1/qa", json={"question": "What is EV?"})
    assert response.status_code == 200
    assert "answer" in response.json()
