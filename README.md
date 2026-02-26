# Local Smart Doc - EV Knowledge Q&A System

A production-ready RAG application for Expected Value knowledge question answering.

## Tech Stack

- **Frontend**: Next.js 14 + TypeScript + TailwindCSS
- **Backend**: FastAPI + Python 3.11
- **RAG**: LangChain + ChromaDB
- **Database**: PostgreSQL
- **Deployment**: Docker + Docker Compose

## Quick Start

```bash
# Clone and start
cp env.example .env
# Edit .env with your settings

docker-compose up -d

# Access the app
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://postgres:postgres@db:5432/local_smart_doc |
| CHROMA_PERSIST_DIRECTORY | ChromaDB data directory | /data/chroma |
| OPENAI_API_KEY | OpenAI API key for embeddings | - |
| EMBEDDING_MODEL | Embedding model to use | text-embedding-ada-002 |

## API Endpoints

- `POST /api/v1/documents` - Create document
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{id}` - Get document
- `POST /api/v1/documents/{id}/process` - Process document (RAG)
- `DELETE /api/v1/documents/{id}` - Delete document
- `POST /api/v1/conversations` - Create conversation
- `GET /api/v1/conversations` - List conversations
- `POST /api/v1/qa` - Ask question (RAG Q&A)
- `GET /api/v1/search` - Search documents

## Development

```bash
# Backend only
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend only
cd frontend
npm install
npm run dev
```

## License

MIT
