# EN: Centralized settings via Pydantic BaseSettings (env-driven)
# FR: Paramètres centralisés via Pydantic BaseSettings (pilotés par l'environnement)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # EN: General
    # FR: Général
    app_env: str = "local"
    log_level: str = "info"

    # EN: AWS
    # FR: AWS
    aws_region: str = "us-east-1"
    bedrock_use_real: bool = False

    # EN: Storage / RAG params
    # FR: Stockage / paramètres RAG
    use_in_memory_db: bool = True
    embedding_dim: int = 256
    retriever_top_k: int = 3

    # EN: v2 config style (replaces class Config)
    # FR: Style de config v2 (remplace class Config)
    model_config = SettingsConfigDict(
        env_prefix="",          # read plain env vars / lire les vars d'env sans préfixe
        case_sensitive=False    # case-insensitive / insensible à la casse
    )

settings = Settings()