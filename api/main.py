# EN: FastAPI app entrypoint wiring routers
# FR: Point d'entrée FastAPI reliant les routes
from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging

from api.routes.health import router as health_router
from api.routes.orchestrate import router as orchestrate_router
from api.routes.embed import router as embed_router

setup_logging(settings.log_level)

app = FastAPI(title="Strata RAG Orchestrator", version="0.1.0")

# EN: Mount routers
# FR: Monter les routeurs
app.include_router(health_router, tags=["health"])
app.include_router(orchestrate_router, tags=["orchestrate"])
app.include_router(embed_router, tags=["embed"])