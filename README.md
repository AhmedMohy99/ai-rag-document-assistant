# AI RAG Document Assistant

A recruiter-friendly, real deployable AI project with:

- **FastAPI backend**
- **Static frontend** that can be deployed on **Vercel**
- **Local persistent vector index** on the backend
- Support for:
  - PDF
  - DOCX
  - TXT
  - Web URLs
- Retrieval-Augmented Generation using **OpenAI**

## Architecture

- `frontend/` → static HTML/CSS/JS frontend for Vercel
- `backend/` → FastAPI API for ingestion + query
- `backend/data/` → persisted vector store and uploaded files

## Features

- Upload multiple documents
- Ingest URLs
- Chunk and index content
- Ask questions against indexed content
- Return answer with source chunks
- Health check endpoint
- CORS enabled for frontend domain

---

## 1) Backend setup (local)

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add:

```env
OPENAI_API_KEY=your_key_here
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend starts at:

```text
http://127.0.0.1:8000
```

---

## 2) Frontend setup (local)

Just open `frontend/public/index.html` in a browser for a quick preview.

For a local static server, you can run:

```bash
cd frontend/public
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

---

## 3) API endpoints

### Health
- `GET /health`

### Ingest files
- `POST /api/ingest/files`

Form field:
- `files`

### Ingest URL
- `POST /api/ingest/url`

JSON body:
```json
{
  "url": "https://example.com"
}
```

### Ask question
- `POST /api/query`

JSON body:
```json
{
  "question": "What is the refund policy?",
  "top_k": 4
}
```

---

## 4) Deploy plan

### Frontend
Deploy `frontend/public` to **Vercel**.

### Backend
Deploy `backend` to **Render**.

Set these environment variables on the backend:
- `OPENAI_API_KEY`
- `ALLOWED_ORIGINS`
- `DATA_DIR`

On the frontend, update the API base URL in:
- `frontend/public/app.js`

---

## 5) Suggested GitHub repo name

```text
ai-rag-document-assistant
```

---

## 6) What makes this portfolio-worthy?

- Real API architecture
- Real document ingestion
- Real retrieval pipeline
- Real deployment split
- Clean project structure
- Recruiter-friendly README
