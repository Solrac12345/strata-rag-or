# EN: Orchestrate endpoint wired to the multi-agent orchestrator.
# FR: Endpoint Orchestrate connecté à l'orchestrateur multi-agents.
from fastapi import APIRouter
from api.schemas.orchestrate import OrchestrateRequest, OrchestrateResponse
from app.orchestrator.orchestrator import get_orchestrator

router = APIRouter()

@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(req: OrchestrateRequest):
    orch = get_orchestrator()
    return orch.orchestrate(req.query)