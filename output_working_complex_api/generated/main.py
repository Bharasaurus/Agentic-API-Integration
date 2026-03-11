import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.pet_router import router as pet_router
from app.api.breeds import router as breeds_router
from app.api.fact_router import router as fact_router
from middleware import LoggingMiddleware
from dependencies import get_async_http_client

# Load environment variables (e.g., from a .env file)
from dotenv import load_dotenv
load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Dog API Service",
        version="1.0.0",
        description="API providing dog breeds and facts information",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Global middlewares
    app.add_middleware(LoggingMiddleware)

    # Example CORS configuration (adjust as needed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(breeds_router, tags=["Breeds"])
    app.include_router(fact_router, tags=["Facts"])
    app.include_router(pet_router, prefix="/pets", tags=["Pets"])

    return app


app = create_app()
