"""
Speech-to-Text API Endpoints

This module provides the REST API endpoints for speech-to-text services.
It handles the conversion of audio content to text with support for
multiple languages and audio formats.

Dependencies:
    - FastAPI for REST API functionality
    - Speech-to-Text service for handling the transcription
    - Request/Response schemas for data validation
"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.requests import STTRequest
from app.schemas.responses import STTResponse
from app.services.stt_service import STTService

router = APIRouter()

async def get_stt_service():
    """
    Dependency injection for the speech-to-text service.
    
    Returns:
        STTService: An instance of the speech-to-text service
    """
    return STTService()

@router.post("/synthesize", response_model=STTResponse)
async def transcribe_speech(
    request: STTRequest,
    service: STTService = Depends(get_stt_service)
):
    """
    Convert speech to text using Google Cloud Speech-to-Text.
    
    Args:
        request (STTRequest): The transcription request containing:
            - audioContent: Base64 encoded audio data
            - languageCode: Language code for recognition
            - audioEncoding: Audio format (e.g., 'LINEAR16')
        service (STTService): Injected speech-to-text service
    
    Returns:
        STTResponse: The transcription response containing:
            - text: The transcribed text
            - confidence: Confidence score (0.0 to 1.0)
            - language_code: Language code used
    
    Raises:
        HTTPException: (400) For invalid parameters or (500) for internal errors.
    """
    try:
        result = await service.transcribe_audio(
            audio_content=request.audioContent,
            language_code=request.languageCode,
        )
        return STTResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Speech-to-Text service error") 