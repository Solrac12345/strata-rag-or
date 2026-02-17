"""
EN: API endpoint tests using FastAPI TestClient.
FR: Tests des endpoints API avec FastAPI TestClient.
"""
from __future__ import annotations
from fastapi.testclient import TestClient

from api.main import app


def test_health():
    client = TestClient(app)
    r = client.get('/health')
    assert r.status_code == 200
    data = r.json()
    assert data.get('status') == 'ok'


def test_orchestrate_returns_answer_and_sources():
    client = TestClient(app)
    r = client.post('/orchestrate', json={"query": "What is RAG?"})
    assert r.status_code == 200
    data = r.json()
    assert data.get('routed_agent') == 'qa'
    assert 'answer' in data
    assert isinstance(data.get('sources'), list)


def test_embed_vector_shape():
    client = TestClient(app)
    r = client.post('/embed', json={"text": "hello world"})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data.get('vector'), list)
    assert data.get('dim') == len(data['vector'])