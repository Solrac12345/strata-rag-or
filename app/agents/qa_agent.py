"""
EN: QA agent — retrieves context and generates an answer.
FR: Agent QA — récupère le contexte et génère une réponse.
"""
from __future__ import annotations

from typing import List

from app.rag.retriever import Retriever
from app.services.llm_service import LLMService


class QAAgent:
    def __init__(self, retriever: Retriever, llm: LLMService) -> None:
        self.retriever = retriever
        self.llm = llm

    def run(self, query: str) -> dict:
        docs = self.retriever.retrieve(query)
        context = "\n".join(d.content for d in docs)
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        answer = self.llm.generate(prompt)
        sources: List[str] = [d.id for d in docs]
        return {"answer": answer, "sources": sources}