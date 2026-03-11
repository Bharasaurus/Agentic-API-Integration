import logging
from fastapi import FastAPI
from app.routers.breeds import router as breeds_router
from app.middleware import LoggingMiddleware
from app.config import get_settings

def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level.upper())
    app = FastAPI(
        title="Dog Breeds API Proxy",
        version="1.0.0",
        description="Proxy service exposing /breeds endpoint with validation",
    )
    app.add_middleware(LoggingMiddleware)
    app.include_router(breeds_router)
    return app


app = create_app()
---