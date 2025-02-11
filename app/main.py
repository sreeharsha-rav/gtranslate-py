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

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Translation Service API with Text-to-Speech and Speech-to-Text capabilities",
)

# Set CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins
    allow_credentials=False,     # Allow credentials
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow specific methods
    allow_headers=["*"],        # Allow all headers
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

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    response = JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
