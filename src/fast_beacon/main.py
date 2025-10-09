"""Main FastAPI application for Beacon v2 API."""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from fast_beacon import __version__
from fast_beacon.api import (
    analyses_router,
    biosamples_router,
    cohorts_router,
    datasets_router,
    g_variations_router,
    individuals_router,
    info_router,
    runs_router,
)
from fast_beacon.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler.

    Use this to initialize and cleanup resources like database connections.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup: Initialize resources here
    # Example: await database.connect()
    yield
    # Shutdown: Cleanup resources here
    # Example: await database.disconnect()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    settings = get_settings()

    app = FastAPI(
        title="Beacon v2 API",
        description="A skeleton implementation of the GA4GH Beacon v2 API specification",
        version=__version__,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # Include routers
    app.include_router(info_router, prefix="/api")
    app.include_router(individuals_router, prefix="/api")
    app.include_router(biosamples_router, prefix="/api")
    app.include_router(g_variations_router, prefix="/api")
    app.include_router(analyses_router, prefix="/api")
    app.include_router(cohorts_router, prefix="/api")
    app.include_router(datasets_router, prefix="/api")
    app.include_router(runs_router, prefix="/api")

    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, Any]:
        """Root endpoint redirecting to API info."""
        return {
            "message": "Beacon v2 API",
            "version": __version__,
            "docs": "/docs",
            "info": "/api/info",
        }

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        """
        Health check endpoint.

        Returns:
            Health status
        """
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "fast_beacon.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level,
    )
