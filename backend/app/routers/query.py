from fastapi import APIRouter, HTTPException

from app.models import QueryRequest, QueryResponse, SourceChunk
from app.services.rag_service import query_rag, vector_store

router = APIRouter(prefix="/api", tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query_documents(payload: QueryRequest) -> QueryResponse:
    if not vector_store.is_ready():
        raise HTTPException(
            status_code=400,
            detail="No indexed documents found. Upload files or ingest a URL first.",
        )

    result = query_rag(payload.question, payload.top_k)
    return QueryResponse(
        answer=result["answer"],
        sources=[SourceChunk(**source) for source in result["sources"]],
        context_count=result["context_count"],
    )
