"""
EN: AWS Lambda handler that wraps the FastAPI orchestrator for serverless deployment.
FR: Handler AWS Lambda qui encapsule l'orchestrateur FastAPI pour un déploiement serverless.
"""
from __future__ import annotations

import json
from typing import Any, Dict

from app.orchestrator.orchestrator import get_orchestrator


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    EN: Lambda entry-point. Expects API Gateway proxy integration format.
    FR: Point d'entrée Lambda. Attend le format d'intégration proxy API Gateway.
    """
    try:
        body = json.loads(event.get("body", "{}"))
        query = body.get("query", "")

        orch = get_orchestrator()
        result = orch.orchestrate(query)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result),
        }
    except Exception as exc:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(exc)}),
        }