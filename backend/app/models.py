from typing import List, Optional

from pydantic import BaseModel, Field


class URLIngestRequest(BaseModel):
    url: str


class QueryRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=4, ge=1, le=10)


class SourceChunk(BaseModel):
    source: str
    chunk_id: str
    text: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    context_count: int


class IngestResponse(BaseModel):
    message: str
    documents_ingested: int
    chunks_created: int
    sources: List[str]


class HealthResponse(BaseModel):
    status: str
    vector_index_ready: bool
    chunk_count: int
