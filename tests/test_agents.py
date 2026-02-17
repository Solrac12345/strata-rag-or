"""
EN: Unit tests for routing and QA agent behavior.
FR: Tests unitaires pour le routage et le comportement de l'agent QA.
"""
from __future__ import annotations
from app.orchestrator.orchestrator import get_orchestrator


def test_routing_agent_routes_to_qa():
    orch = get_orchestrator()
    res = orch.orchestrate("What is RAG?")
    assert res['routed_agent'] == 'qa'


def test_qa_agent_returns_sources():
    orch = get_orchestrator()
    res = orch.orchestrate("Explain multi-agent orchestration")
    assert isinstance(res.get('sources'), list)
    assert len(res['sources']) >= 1
    assert 'answer' in res