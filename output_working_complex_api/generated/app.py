import logging

from fastapi import FastAPI

from .config import settings
from .dependencies import get_http_client
from .middleware import LoggingMiddleware
from .routers.group_router import router as group_router

def configure_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="Group Service API",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.add_middleware(LoggingMiddleware)
    app.include_router(group_router)

    # Register HTTP client dependency globally
    app.dependency_overrides[get_http_client] = get_http_client

    return app

app = create_app()