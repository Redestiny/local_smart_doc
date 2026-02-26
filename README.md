# Local Smart Doc

EV Knowledge Q&A System with RAG (Retrieval Augmented Generation).

## Tech Stack

- **Frontend**: Next.js 14 + TypeScript + TailwindCSS
- **Backend**: FastAPI + Python 3.11
- **Database**: PostgreSQL + ChromaDB
- **Deployment**: Docker Compose

## Quick Start

```bash
# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env and set OPENAI_API_KEY

# Start all services
docker-compose up -d

# Access
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection | postgresql://postgres:postgres@db:5432/local_smart_doc |
| CHROMA_PERSIST_DIRECTORY | ChromaDB data dir | /data/chroma |
| OPENAI_API_KEY | OpenAI API key | - |

## API Endpoints

- `POST /api/v1/documents` - Create document
- `GET /api/v1/documents` - List documents
- `POST /api/v1/documents/{id}/process` - Process with RAG
- `POST /api/v1/qa` - Ask question
- `GET /api/v1/search` - Search documents

## Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
