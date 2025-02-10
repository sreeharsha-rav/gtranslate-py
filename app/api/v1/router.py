"""
API Router Configuration

This module configures the main API router for the application, combining all endpoint routers
with their respective prefixes and tags. It serves as the central routing configuration
for the v1 version of the API.

The router includes endpoints for:
- Translation services (/translate)
- Text-to-Speech services (/tts)
- Speech-to-Text services (/stt)

Each endpoint group is tagged appropriately for OpenAPI documentation organization.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import translation, tts, stt

api_router = APIRouter()

api_router.include_router(translation.router, tags=["translation"])
api_router.include_router(tts.router, prefix="/tts", tags=["text-to-speech"])
api_router.include_router(stt.router, prefix="/stt", tags=["speech-to-text"]) 