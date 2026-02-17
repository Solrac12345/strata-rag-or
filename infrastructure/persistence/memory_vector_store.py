"""
EN: In-memory vector store using brute-force cosine similarity.
FR: Magasin vectoriel en mémoire avec similarité cosinus par force brute.
"""
from __future__ import annotations

from typing import List, Tuple


class MemoryVectorStore:
    def __init__(self, dim: int = 256) -> None:
        self.dim = dim
        self._vectors: List[Tuple[str, List[float]]] = []

    def upsert(self, doc_id: str, vector: List[float]) -> None:
        self._vectors = [(did, v) for did, v in self._vectors if did != doc_id]
        self._vectors.append((doc_id, vector))

    def query(self, vector: List[float], top_k: int = 3) -> List[Tuple[str, float]]:
        scored: List[Tuple[str, float]] = []
        for doc_id, stored in self._vectors:
            score = self._cosine(vector, stored)
            scored.append((doc_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    @staticmethod
    def _cosine(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = max(sum(x * x for x in a) ** 0.5, 1e-9)
        nb = max(sum(x * x for x in b) ** 0.5, 1e-9)
        return dot / (na * nb)