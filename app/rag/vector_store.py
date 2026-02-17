"""
EN: Abstract vector store interface.
    Concrete implementations live in infrastructure/persistence/.
FR: Interface abstraite du magasin vectoriel.
    Les implémentations concrètes vivent dans infrastructure/persistence/.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple


class VectorStore(ABC):
    """
    EN: Contract that any vector store backend must satisfy.
    FR: Contrat que tout backend de magasin vectoriel doit respecter.
    """

    @abstractmethod
    def upsert(self, doc_id: str, vector: List[float]) -> None:
        ...

    @abstractmethod
    def query(self, vector: List[float], top_k: int = 3) -> List[Tuple[str, float]]:
        ...