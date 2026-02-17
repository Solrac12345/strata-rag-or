"""
EN: Deterministic embedding function (demo / offline stub).
FR: Fonction d'embedding déterministe (démo / stub hors ligne).
"""
from __future__ import annotations

import hashlib
import struct
from typing import List


class EmbeddingFunction:
    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def embed(self, text: str) -> List[float]:
        """
        EN: Produce a deterministic float vector from text using SHA-256.
        FR: Produire un vecteur flottant déterministe à partir du texte via SHA-256.
        """
        h = hashlib.sha256(text.encode()).digest()
        # Repeat hash bytes to fill the requested dimension
        raw = (h * ((self.dim * 4 // len(h)) + 1))[: self.dim * 4]
        vec = list(struct.unpack(f"<{self.dim}f", raw))
        # Normalize
        norm = max(sum(v * v for v in vec) ** 0.5, 1e-9)
        return [v / norm for v in vec]
