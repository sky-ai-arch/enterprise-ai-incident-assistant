from fastapi import FastAPI

from incident_assistant.api.router import api_router
from incident_assistant.shared.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered platform for investigating production incidents.",
)

app.include_router(api_router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }