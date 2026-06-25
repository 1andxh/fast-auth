from fastapi import FastAPI
from src.core.config import settings
from src.api.router import router
from src.core.middleware import RequestIDMiddleware
from src.core.logging.context import request_id_ctx

version = settings.VERSION


app = FastAPI(title=settings.APP_NAME, version=version)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1")

# middleware
app.add_middleware(RequestIDMiddleware)
