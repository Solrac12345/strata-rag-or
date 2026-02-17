"""
EN: Abstract base class for all agents in the orchestrator.
FR: Classe abstraite de base pour tous les agents de l'orchestrateur.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    EN: Every agent must implement `run(query) -> dict`.
    FR: Chaque agent doit implémenter `run(query) -> dict`.
    """

    @abstractmethod
    def run(self, query: str) -> dict:
        ...