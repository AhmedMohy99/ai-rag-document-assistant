# Step-by-step deployment

## A) Put the code on GitHub
1. Create a new GitHub repository named `ai-rag-document-assistant`
2. Upload all folders and files from this project
3. Commit and push

---

## B) Deploy the backend on Render

1. Open Render
2. Click **New +**
3. Choose **Web Service**
4. Connect your GitHub repo
5. Set the **Root Directory** to:
   `backend`
6. Build command:
   `pip install -r requirements.txt`
7. Start command:
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment variables
Add:
- `OPENAI_API_KEY` = your real OpenAI key
- `ALLOWED_ORIGINS` = your Vercel frontend URL later
- `DATA_DIR` = `./data`
- `MODEL_NAME` = `gpt-4.1-mini`
- `EMBEDDING_MODEL` = `text-embedding-3-small`

8. Deploy
9. After deploy, copy the backend URL
10. Test:
   - `/health`

Example:
`https://your-backend-name.onrender.com/health`

---

## C) Deploy the frontend on Vercel

1. Open `frontend/public/app.js`
2. Replace:
   `const API_BASE_URL = "http://127.0.0.1:8000";`
   with your real Render backend URL

Example:
`const API_BASE_URL = "https://your-backend-name.onrender.com";`

3. Save the file
4. Go to Vercel
5. Click **Add New Project**
6. Import the same GitHub repo
7. Set the **Root Directory** to:
   `frontend/public`
8. Deploy

9. Copy your Vercel URL

---

## D) Final CORS step
Go back to Render and update:
- `ALLOWED_ORIGINS`

Example:
`https://your-frontend.vercel.app`

If you want multiple origins:
`http://127.0.0.1:5500,http://localhost:5500,https://your-frontend.vercel.app`

Redeploy backend if needed.

---

## E) Test the live app
1. Open your Vercel frontend
2. Click **Check Health**
3. Upload a TXT, DOCX, or PDF
4. Ask a question
5. Verify answer and sources show up

---

## Important note
This is a real deployable starter project.
For large production use, replace the local JSON vector store with a managed vector database later.
