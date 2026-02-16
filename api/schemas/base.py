# EN: Common Pydantic base model config
# FR: Configuration commune pour les modèles Pydantic
from pydantic import BaseModel, ConfigDict

class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")