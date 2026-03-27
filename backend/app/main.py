from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers.health import router as health_router
from app.routers.ingest import router as ingest_router
from app.routers.query import router as query_router

settings = get_settings()

app = FastAPI(
    title="AI RAG Document Assistant API",
    version="1.0.0",
    description="Upload documents or URLs, index them, and ask questions against the content.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(query_router)
