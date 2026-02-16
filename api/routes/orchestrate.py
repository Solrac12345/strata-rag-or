# EN: Orchestrate endpoint (stub for now; real orchestration in next steps)
# FR: Endpoint Orchestrate (stub pour l'instant; orchestration réelle à venir)
from fastapi import APIRouter
from api.schemas.orchestrate import OrchestrateRequest, OrchestrateResponse

router = APIRouter()

@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(req: OrchestrateRequest):
    # EN: Placeholder response; will be replaced by multi-agent orchestrator
    # FR: Réponse provisoire; sera remplacée par l'orchestrateur multi-agents
    return {
        "answer": f"(stub) You asked: {req.query}",
        "routed_agent": "qa",
        "sources": [],
    }
