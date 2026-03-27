from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import get_settings
from app.models import IngestResponse, URLIngestRequest
from app.services.rag_service import ingest_file_paths, ingest_single_url

router = APIRouter(prefix="/api/ingest", tags=["ingest"])

settings = get_settings()
data_dir = Path(settings.data_dir)
uploads_dir = data_dir / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


@router.post("/files", response_model=IngestResponse)
async def ingest_files(files: List[UploadFile] = File(...)) -> IngestResponse:
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    saved_paths: List[str] = []

    for upload in files:
        suffix = Path(upload.filename or "").suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {suffix}. Allowed: PDF, DOCX, TXT.",
            )

        target_path = uploads_dir / (upload.filename or "uploaded_file")
        content = await upload.read()
        target_path.write_bytes(content)
        saved_paths.append(str(target_path))

    result = ingest_file_paths(saved_paths)
    return IngestResponse(
        message="Files ingested successfully.",
        documents_ingested=result["documents_ingested"],
        chunks_created=result["chunks_created"],
        sources=result["sources"],
    )


@router.post("/url", response_model=IngestResponse)
def ingest_url(payload: URLIngestRequest) -> IngestResponse:
    result = ingest_single_url(payload.url)
    return IngestResponse(
        message="URL ingested successfully.",
        documents_ingested=result["documents_ingested"],
        chunks_created=result["chunks_created"],
        sources=result["sources"],
    )
