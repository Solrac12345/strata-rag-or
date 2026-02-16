# EN: Embed endpoint (stub deterministic embedding)
# FR: Endpoint Embed (plongement déterministe stub)
from fastapi import APIRouter
from api.schemas.embed import EmbedRequest, EmbedResponse

router = APIRouter()

@router.post("/embed", response_model=EmbedResponse)
def embed(req: EmbedRequest):
    # Simple fixed-length vector: length of text mod 10 one-hot (demo only)
    length = len(req.text)
    dim = 10
    vec = [0.0] * dim
    vec[length % dim] = 1.0
    return {"vector": vec, "dim": dim}