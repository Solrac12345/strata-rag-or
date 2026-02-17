"""
EN: Retriever: indexes documents and retrieves the most relevant ones.
FR: Retriever : indexe les documents et récupère les plus pertinents.
"""
from __future__ import annotations

from typing import List

from app.rag.embeddings import EmbeddingFunction
from app.rag.document_store import Document, DocumentStore
from infrastructure.persistence.memory_vector_store import MemoryVectorStore


class Retriever:
    def __init__(
        self,
        embedder: EmbeddingFunction,
        vector_store: MemoryVectorStore,
        doc_store: DocumentStore,
        top_k: int = 3,
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store
        self.doc_store = doc_store
        self.top_k = top_k

    def index(self, doc: Document) -> None:
        self.doc_store.put(doc)
        vec = self.embedder.embed(doc.content)
        self.vector_store.upsert(doc.id, vec)

    def retrieve(self, query: str) -> List[Document]:
        q_vec = self.embedder.embed(query)
        results = self.vector_store.query(q_vec, top_k=self.top_k)
        docs: List[Document] = []
        for doc_id, _score in results:
            doc = self.doc_store.get(doc_id)
            if doc is not None:
                docs.append(doc)
        return docs
