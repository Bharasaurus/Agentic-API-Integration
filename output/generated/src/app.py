from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from src.api.facts_router import router as facts_router
from src.middleware import LoggingMiddleware
from src.dependencies import get_http_client
from src.clients.fact_client import FactClient
from src.services.fact_service import FactService

# Dependency overrides for the request‑scoped http client
def configure_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[get_http_client] = get_http_client
    # FactClient depends on Settings only, no override needed.
    # FactService depends on FactClient and http client, both resolved via DI.


def create_app() -> FastAPI:
    app = FastAPI(
        title="Facts API",
        version="1.0.0",
        description="Provides factual statements retrieved from an external service.",
    )
    app.add_middleware(LoggingMiddleware)
    app.include_router(facts_router)

    configure_dependencies(app)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)