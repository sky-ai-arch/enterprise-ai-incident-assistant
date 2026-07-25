from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Incident Investigation Assistant",
    version="0.1.0",
    description="AI-powered platform for investigating production incidents.",
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "application": "Enterprise AI Incident Investigation Assistant",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
    }