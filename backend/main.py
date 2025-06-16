"""Data Contracts Studio FastAPI Application.

This module serves as the main entry point for the Data Contracts Studio API,
configuring the FastAPI application with middleware, routers, and error handling.
"""

import logging
from app.api.contracts import router as contracts_router
from app.core.config import settings
from app.core.database import Base, engine
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise

    # Initialize FastAPI application
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="A production-ready API for managing data contracts and schema definitions",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Configure CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Include API routers
    application.include_router(contracts_router, prefix="/api/v1")

    # Add version endpoint to API v1
    @application.get("/api/v1/version", response_model=Dict[str, Any])
    async def get_api_version() -> Dict[str, Any]:
        """Get API version information.

        Returns:
            Dict[str, Any]: API version and metadata.
        """
        from app.__version__ import get_version_info

        version_info = get_version_info()

        return {
            "version": version_info["version"],
            "name": version_info["title"],
            "api_version": "v1",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "operational",
        }

    return application


# Create application instance
app = create_application()


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors.

    Args:
        request: The incoming request.
        exc: The validation exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")

    # Convert error details to JSON-serializable format
    serializable_errors = []
    for error in exc.errors():
        serializable_error = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "input": str(error.get("input")) if error.get("input") is not None else None,
        }
        serializable_errors.append(serializable_error)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation error", "details": serializable_errors, "status": "error"},
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle database errors.

    Args:
        request: The incoming request.
        exc: The database exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.error(f"Database error on {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Database operation failed", "status": "error"},
    )


# API endpoints
@app.get("/", response_model=Dict[str, Any])
async def root() -> Dict[str, Any]:
    """Root endpoint providing API information.

    Returns:
        Dict[str, Any]: API welcome message and metadata.
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else "Documentation disabled in production",
        "api_base": "/api/v1",
        "status": "running",
    }


@app.get("/health", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for monitoring and load balancers.

    Returns:
        Dict[str, Any]: Health status information.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "production" if not settings.debug else "development",
    }


@app.get("/version", response_model=Dict[str, Any])
async def get_version() -> Dict[str, Any]:
    """Get comprehensive application version information.

    Returns:
        Dict[str, Any]: Detailed version and build information.
    """
    from app.__version__ import get_version_info

    version_info = get_version_info()

    return {
        "version": version_info["version"],
        "name": version_info["title"],
        "description": version_info["description"],
        "build_date": datetime.utcnow().isoformat(),
        "environment": "production" if not settings.debug else "development",
        "api_version": "v1",
        "debug": settings.debug,
        "database": "connected",
        "author": version_info["author"],
        "license": version_info["license"],
    }
