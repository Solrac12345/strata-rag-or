"""
EN: Routing agent — decides which specialist agent handles the query.
FR: Agent de routage — décide quel agent spécialisé traite la requête.
"""
from __future__ import annotations


class RoutingAgent:
    def route(self, query: str) -> str:
        """
        EN: For now, all queries are routed to the QA agent.
        FR: Pour l'instant, toutes les requêtes sont routées vers l'agent QA.
        """
        return "qa"