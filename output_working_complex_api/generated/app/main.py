from __future__ import annotations
import uvicorn
from fastapi import FastAPI
from app.api.fact_router import router as fact_router
from app.middleware import LoggingMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title="Facts Service",
        version="1.0.0",
        description="API exposing facts retrieved from an external service",
    )
    app.add_middleware(LoggingMiddleware)
    app.include_router(fact_router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)