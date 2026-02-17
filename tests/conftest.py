"""
EN: Pytest fixtures for FastAPI TestClient and orchestrator.
FR: Fixtures Pytest pour FastAPI TestClient et orchestrateur.
"""
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient

from api.main import app
from app.orchestrator.orchestrator import get_orchestrator


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def orchestrator():
    # EN/FR: Provide orchestrator instance for tests
    return get_orchestrator()