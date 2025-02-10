"""
FastAPI Application Entry Point

This module serves as the main entry point for the Translation Service API. It initializes the FastAPI
application, configures middleware, and sets up routing for all API endpoints. The service provides
translation capabilities along with Text-to-Speech (TTS) and Speech-to-Text (STT) functionalities.

The application is configured with CORS middleware to handle cross-origin requests and provides
OpenAPI documentation at the /docs endpoint.

Environment Variables:
    All configuration is handled through the settings module (see core.config)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Translation Service API with Text-to-Speech and Speech-to-Text capabilities",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
)

# Set CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    """
    Health Check Endpoint
    
    Returns:
        dict: A simple response indicating the service is healthy
        
    Example:
        Response: {"status": "healthy"}
    """
    return {"status": "healthy"}
