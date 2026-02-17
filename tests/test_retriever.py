"""
EN: Unit tests for the retriever pipeline.
FR: Tests unitaires pour le pipeline de récupération.
"""
from __future__ import annotations
from app.rag.embeddings import EmbeddingFunction
from infrastructure.persistence.memory_vector_store import MemoryVectorStore
from app.rag.document_store import DocumentStore, Document
from app.rag.retriever import Retriever


essay = "RAG grounds LLMs with retrieved context and improves factuality."


def test_retriever_finds_relevant_document():
    embedder = EmbeddingFunction(dim=64)
    vs = MemoryVectorStore(dim=64)
    store = DocumentStore()
    retriever = Retriever(embedder, vs, store, top_k=2)

    retriever.index(Document(id="d1", content=essay, metadata={"id": "d1"}))
    retriever.index(Document(id="d2", content="Cooking pasta al dente.", metadata={"id": "d2"}))

    docs = retriever.retrieve("What is RAG?")
    assert docs
    assert any("RAG" in d.content for d in docs)