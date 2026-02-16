# EN: Schemas for /orchestrate
# FR: Schémas pour /orchestrate
from typing import List
from pydantic import Field
from .base import ApiModel

class OrchestrateRequest(ApiModel):
    query: str = Field(..., description="User natural language query / Requête utilisateur")

class OrchestrateResponse(ApiModel):
    answer: str
    routed_agent: str
    sources: List[str]