from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np

from app.config import get_settings


class VectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.data_dir = Path(settings.data_dir)
        self.index_path = self.data_dir / "vector_store.json"

        self.records: List[Dict] = []
        if self.index_path.exists():
            self._load()

    def _load(self) -> None:
        payload = json.loads(self.index_path.read_text(encoding="utf-8"))
        self.records = payload.get("records", [])

    def _save(self) -> None:
        payload = {"records": self.records}
        self.index_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)

        denom = (np.linalg.norm(a) * np.linalg.norm(b))
        if denom == 0:
            return 0.0
        return float(np.dot(a, b) / denom)

    def add_chunks(self, chunks: List[Dict]) -> None:
        self.records.extend(chunks)
        self._save()

    def search(self, query_embedding: List[float], top_k: int = 4) -> List[Dict]:
        scored = []
        for record in self.records:
            score = self._cosine_similarity(query_embedding, record["embedding"])
            scored.append({**record, "score": score})

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def is_ready(self) -> bool:
        return len(self.records) > 0

    def chunk_count(self) -> int:
        return len(self.records)
