# EN: Centralized settings via Pydantic BaseSettings (env-driven)
# FR: Paramètres centralisés via Pydantic BaseSettings (pilotés par l'env)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "local"
    log_level: str = "info"
    aws_region: str = "us-east-1"
    bedrock_use_real: bool = False
    use_in_memory_db: bool = True
    embedding_dim: int = 256
    retriever_top_k: int = 3

    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()