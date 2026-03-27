from __future__ import annotations

from typing import List

from openai import OpenAI

from app.config import get_settings


settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


def embed_texts(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []

    response = client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]


def answer_question(question: str, context_chunks: List[dict]) -> str:
    context_text = "\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}" for chunk in context_chunks
    )

    system_prompt = (
        "You are a helpful AI assistant answering questions strictly from the provided context. "
        "If the context is insufficient, say so clearly. Keep answers concise and practical."
    )

    user_prompt = f"""Question:
{question}

Context:
{context_text}

Instructions:
- Answer using only the context above.
- If context is not enough, say that clearly.
- Mention source names naturally when useful.
"""

    response = client.responses.create(
        model=settings.model_name,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.output_text.strip()
