from fastapi import FastAPI
from src.core.config import settings

version = settings.VERSION

app = FastAPI(title=settings.APP_NAME, version=version)


@app.get("/health")
async def health():
    return {"status": "ok"}
