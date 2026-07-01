"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging import request_logging_middleware

# Create FastAPI app
app = FastAPI(
    title="LMS API",
    version="1.0.0",
    description="Learning Management System API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
register_exception_handlers(app)

# Add logging middleware
app.middleware("http")(request_logging_middleware)

# Include API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "LMS API is running",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
