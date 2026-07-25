from fastapi import APIRouter
from incident_assistant.api.routers.v1.health import router as health_router
from incident_assistant.api.routers.v1.incidents import (
    router as incident_router,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(incident_router)