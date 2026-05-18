# EN: Health endpoint
# FR: Endpoint de santé
import json

from fastapi import APIRouter
from fastapi.responses import Response

from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health():
    body = json.dumps({"status": "ok", "env": settings.app_env})
    return Response(content=body + "\n", media_type="application/json")