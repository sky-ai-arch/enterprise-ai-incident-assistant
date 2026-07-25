from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    """Liveness probe.

    Indicates that the application process is running.
    """
    return {
        "status": "healthy",
    }


@router.get("/ready")
async def readiness():
    """Readiness probe.

    Indicates whether the application is ready to serve requests.
    Future versions will verify dependencies such as:
      - PostgreSQL
      - Redis
      - LLM Provider
      - Vector Database
    """
    return {
        "status": "ready",
    }