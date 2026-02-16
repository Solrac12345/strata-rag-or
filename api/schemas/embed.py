# EN: Schemas for /embed
# FR: Schémas pour /embed
from typing import List
from pydantic import Field
from .base import ApiModel

class EmbedRequest(ApiModel):
    text: str = Field(..., description="Text to embed / Texte à encoder")

class EmbedResponse(ApiModel):
    vector: List[float]
    dim: int