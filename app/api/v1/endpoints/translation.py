"""
Translation API Endpoints

This module provides the REST API endpoints for text translation services.
It handles translation requests and responses, with proper error handling
and input validation.

Dependencies:
    - FastAPI for REST API functionality
    - Translation service for handling the actual translation
    - Request/Response schemas for data validation
"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.requests import TranslateRequest, DetectLanguageRequest
from app.schemas.responses import TranslateResponse, SupportedLanguagesResponse, DetectLanguageResponse
from app.services.translation_service import TranslationService

router = APIRouter()

async def get_translation_service():
    """
    Dependency injection for the translation service.
    
    Returns:
        TranslationService: An instance of the translation service
    """
    return TranslationService()

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(
    request: TranslateRequest,
    service: TranslationService = Depends(get_translation_service)
):
    """
    Translate text from one language to another.
    
    Args:
        request (TranslateRequest): The translation request containing:
            - text: Text to translate
            - target_language: Language code to translate to
            - source_language: Optional source language code
        service (TranslationService): Injected translation service
    
    Returns:
        TranslateResponse: The translation response containing:
            - translated_text: The translated text
            - source_language: Detected or provided source language
            - target_language: Target language code
    
    Raises:
        HTTPException(400): If the target language is not supported
        HTTPException(500): If there's an internal translation service error
    
    """
    try:
        result = await service.translate_text(
            text=request.text,
            target_language=request.targetLanguage,
            source_language=request.sourceLanguage
        )
        return TranslateResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Translation service error")

@router.post("/detect-language", response_model=DetectLanguageResponse)
async def detect_language(
    request: DetectLanguageRequest,
    service: TranslationService = Depends(get_translation_service)
):
    """
    Detect the language of the provided text.
    
    Args:
        request (DetectLanguageRequest): The request containing:
            - text: Text to detect language from
        service (TranslationService): Injected translation service
    
    Returns:
        DetectLanguageResponse: The detected language information containing:
            - language_code: Detected language code
            - confidence: Confidence score of the detection
    
    Raises:
        HTTPException(400): If the text is invalid
        HTTPException(500): If there's an internal service error
    """
    try:
        result = await service.detect_language(text=request.text)
        return DetectLanguageResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Language detection failed") 