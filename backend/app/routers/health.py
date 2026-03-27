from fastapi import APIRouter

from app.models import HealthResponse
from app.services.rag_service import vector_store

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        vector_index_ready=vector_store.is_ready(),
        chunk_count=vector_store.chunk_count(),
    )
