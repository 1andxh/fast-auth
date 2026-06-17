from fastapi import FastAPI
from src.core.config import settings
from src.api.router import router

version = settings.VERSION


app = FastAPI(title=settings.APP_NAME, version=version)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1")
