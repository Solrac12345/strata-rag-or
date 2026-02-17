"""
EN: Knowledge base loader — reads documents from various sources and indexes them.
FR: Chargeur de base de connaissances — lit les documents et les indexe.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List

from app.rag.document_store import Document
from app.rag.retriever import Retriever


class KBLoader:
    """
    EN: Loads documents into the retriever from a JSON file or a list of dicts.
    FR: Charge des documents dans le retriever depuis un fichier JSON ou une liste de dicts.
    """

    def __init__(self, retriever: Retriever) -> None:
        self.retriever = retriever

    def load_from_list(self, items: List[dict]) -> int:
        """
        EN: Each item must have 'id' and 'content' keys (optional 'metadata').
        FR: Chaque élément doit avoir les clés 'id' et 'content' ('metadata' optionnel).
        """
        count = 0
        for item in items:
            doc = Document(
                id=item["id"],
                content=item["content"],
                metadata=item.get("metadata", {"id": item["id"]}),
            )
            self.retriever.index(doc)
            count += 1
        return count

    def load_from_json(self, path: str | Path) -> int:
        """
        EN: Load a JSON array of {id, content, metadata?} objects.
        FR: Charger un tableau JSON d'objets {id, content, metadata?}.
        """
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return self.load_from_list(data)