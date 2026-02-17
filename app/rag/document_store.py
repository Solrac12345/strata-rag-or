"""
EN: In-memory document store keyed by document ID.
FR: Magasin de documents en mémoire indexé par identifiant.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Document:
    id: str
    content: str
    metadata: Dict[str, str] = field(default_factory=dict)


class DocumentStore:
    def __init__(self) -> None:
        self._docs: Dict[str, Document] = {}

    def put(self, doc: Document) -> None:
        self._docs[doc.id] = doc

    def get(self, doc_id: str) -> Optional[Document]:
        return self._docs.get(doc_id)

    def list_all(self) -> List[Document]:
        return list(self._docs.values())
