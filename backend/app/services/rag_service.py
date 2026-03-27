from __future__ import annotations

import uuid
from typing import Dict, List

from app.config import get_settings
from app.services.document_loader import load_file, load_url
from app.services.llm_service import answer_question, embed_texts
from app.services.text_splitter import split_text
from app.services.vector_store import VectorStore


settings = get_settings()
vector_store = VectorStore()


def ingest_file_paths(file_paths: List[str]) -> Dict:
    source_names: List[str] = []
    chunk_records: List[Dict] = []

    for path_str in file_paths:
        loaded = load_file(__import__("pathlib").Path(path_str))
        chunks = split_text(
            loaded["text"],
            chunk_size=settings.max_chunk_size,
            overlap=settings.chunk_overlap,
        )
        embeddings = embed_texts(chunks) if chunks else []

        for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_records.append(
                {
                    "chunk_id": str(uuid.uuid4()),
                    "source": loaded["source"],
                    "text": chunk_text,
                    "embedding": embedding,
                    "position": idx,
                }
            )

        source_names.append(loaded["source"])

    if chunk_records:
        vector_store.add_chunks(chunk_records)

    return {
        "documents_ingested": len(source_names),
        "chunks_created": len(chunk_records),
        "sources": source_names,
    }


def ingest_single_url(url: str) -> Dict:
    title, text = load_url(url)
    chunks = split_text(
        text,
        chunk_size=settings.max_chunk_size,
        overlap=settings.chunk_overlap,
    )
    embeddings = embed_texts(chunks) if chunks else []
    chunk_records: List[Dict] = []

    for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_records.append(
            {
                "chunk_id": str(uuid.uuid4()),
                "source": title,
                "text": chunk_text,
                "embedding": embedding,
                "position": idx,
            }
        )

    if chunk_records:
        vector_store.add_chunks(chunk_records)

    return {
        "documents_ingested": 1,
        "chunks_created": len(chunk_records),
        "sources": [title],
    }


def query_rag(question: str, top_k: int) -> Dict:
    query_embedding = embed_texts([question])[0]
    hits = vector_store.search(query_embedding=query_embedding, top_k=top_k)
    answer = answer_question(question=question, context_chunks=hits)

    sources = [
        {
            "source": hit["source"],
            "chunk_id": hit["chunk_id"],
            "text": hit["text"],
            "score": round(hit["score"], 4),
        }
        for hit in hits
    ]

    return {
        "answer": answer,
        "sources": sources,
        "context_count": len(sources),
    }
