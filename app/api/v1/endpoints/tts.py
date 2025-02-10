"""
Text-to-Speech API Endpoints

This module provides the REST API endpoints for text-to-speech services.
It handles the conversion of text to synthesized speech with customizable
voice parameters and proper error handling.

Dependencies:
    - FastAPI for REST API functionality
    - Text-to-Speech service for handling the speech synthesis
    - Request/Response schemas for data validation
"""

from fastapi import APIRouter, HTTPException, Depends, Response
from app.schemas.requests import TTSRequest
from app.services.tts_service import TTSService

router = APIRouter()

async def get_tts_service():
    """
    Dependency injection for the text-to-speech service.
    
    Returns:
        TTSService: An instance of the text-to-speech service
    """
    return TTSService()

@router.post("/synthesize")
async def synthesize_speech(
    request: TTSRequest,
    service: TTSService = Depends(get_tts_service)
):
    """
    Convert text to speech using Google Cloud Text-to-Speech and return MP3 audio.
    
    Args:
        request (TTSRequest): The synthesis request containing text to synthesize,
                              language code, and voice name.
        service (TTSService): Injected text-to-speech service.
    
    Returns:
        Response: The raw MP3 audio bytes with the appropriate media type.
    
    Raises:
        HTTPException: (400) For invalid parameters or (500) for internal errors.
    """
    try:
        result = await service.synthesize_speech(
            text=request.text,
            tts_language_code=request.ttsCode,
            voice_name=request.ttsName,
        )
        audio_content = result["audioContent"]
        return Response(
            content=audio_content,  # Raw MP3 audio bytes
            media_type="audio/mp3"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Text-to-Speech service error") 