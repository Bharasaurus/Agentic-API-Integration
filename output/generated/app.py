import logging
import sys
from fastapi import FastAPI
from routers.group_router import router as group_router
from middleware.logging_middleware import LoggingMiddleware
from config import get_settings

def configure_logging() -> None:
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Dog Group Service", version="1.0.0")
    app.add_middleware(LoggingMiddleware)
    app.include_router(group_router)
    return app

app = create_app()

# To run:
# uvicorn app:app --host 0.0.0.0 --port 8000