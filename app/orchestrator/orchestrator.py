"""
EN: Multi-agent orchestrator service with dependency injection.
FR: Service d'orchestration multi-agents avec injection de dépendances.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from app.core.config import settings
from app.agents.routing_agent import RoutingAgent
from app.agents.qa_agent import QAAgent
from app.rag.embeddings import EmbeddingFunction
from app.rag.document_store import Document, DocumentStore
from app.rag.retriever import Retriever
from app.services.llm_service import LLMService
from infrastructure.aws.bedrock_client import BedrockClient
from infrastructure.persistence.memory_vector_store import MemoryVectorStore


@dataclass
class Orchestrator:
    # EN: Agents wired into the orchestrator
    # FR: Agents connectés à l'orchestrateur
    router: RoutingAgent
    qa: QAAgent

    def orchestrate(self, query: str) -> dict:
        # EN: Route the query to an agent and run it
        # FR: Router la requête vers un agent et l'exécuter
        agent = self.router.route(query)
        if agent == "qa":
            result = self.qa.run(query)
            return {"routed_agent": agent, **result}
        # EN/FR: Default fallback if no agent matches
        return {"routed_agent": agent, "answer": "No handler", "sources": []}


# EN/FR: Simple process-wide singleton for the orchestrator instance
_ORCH: Optional[Orchestrator] = None


def get_orchestrator() -> Orchestrator:
    """
    EN: Build the orchestrator once (DI) and reuse it.
    FR: Construire l'orchestrateur une seule fois (DI) et le réutiliser.
    """
    global _ORCH
    if _ORCH is not None:
        return _ORCH

    # EN/FR: Build RAG stack (embedder + vector store + doc store + retriever)
    embedder = EmbeddingFunction(dim=settings.embedding_dim)
    vs = MemoryVectorStore(dim=settings.embedding_dim)
    store = DocumentStore()
    retriever = Retriever(embedder, vs, store, top_k=settings.retriever_top_k)

    # EN: Seed a tiny KB for the demo
    # FR: Amorcer une petite base de connaissances pour la démo
    seed_docs: List[Document] = [
        Document(
            id="kb_rag_intro",
            content="RAG combines retrieval with generation to ground LLMs.",
            metadata={"id": "kb_rag_intro"},
        ),
        Document(
            id="kb_multi_agents",
            content="Multi-agent orchestration routes tasks to specialized agents.",
            metadata={"id": "kb_multi_agents"},
        ),
    ]
    for d in seed_docs:
        retriever.index(d)

    # EN/FR: LLM service (Bedrock stub by default)
    llm_service = LLMService(BedrockClient())

    # EN/FR: Agents
    qa = QAAgent(retriever=retriever, llm=llm_service)
    router = RoutingAgent()

    _ORCH = Orchestrator(router=router, qa=qa)
    return _ORCH