"""
Response Schema Models

This module defines the Pydantic models for API response formatting.
It includes models for translation, text-to-speech, and speech-to-text responses,
ensuring consistent and well-structured API responses.

All models inherit from Pydantic's BaseModel for automatic validation
and serialization/deserialization functionality.
"""

from pydantic import BaseModel, Field

class TranslateResponse(BaseModel):
    """
    Translation Response Model
    
    Structures the response from the translation endpoint.
    Includes the translated text and language information.
    
    Attributes:
        translatedText (str): The resulting translated text
        detectedSourceLanguage (str): The language code of the original text (detected or provided)
        targetLanguage (str): The language code the text was translated to
    """
    translatedText: str = Field(..., description="Translated text")
    detectedSourceLanguage: str = Field(..., description="Detected or provided source language")
    targetLanguage: str = Field(..., description="Target language")

class STTResponse(BaseModel):
    """
    Speech-to-Text Response Model
    
    Structures the response from the speech-to-text endpoint.
    Includes the transcribed text and confidence metrics.
    
    Attributes:
        text (str): The transcribed text from the audio
        confidence (float): Confidence score of the transcription (0.0 to 1.0)
        languageCode (str): The language code of the transcribed text
    
    Note:
        The confidence score indicates how certain the model is about the
        transcription accuracy. Higher values indicate greater confidence.
    """
    text: str = Field(..., description="Transcribed text")
    confidence: float = Field(..., description="Confidence score of the transcription")
    languageCode: str = Field(..., description="Detected language code")

class SupportedLanguagesResponse(BaseModel):
    """
    Supported Languages Response Model
    
    Lists all supported languages for translation.
    
    Attributes:
        languages (dict[str, str]): Dictionary of language codes and names
    """
    languages: dict[str, str] = Field(..., description="Dictionary of language codes and names")

class DetectLanguageResponse(BaseModel):
    """
    Language Detection Response Model
    
    Contains the detected language information.
    
    Attributes:
        languageCode (str): Detected language code
        confidence (float): Confidence score of the detection (0.0 to 1.0)
    """
    languageCode: str = Field(..., description="Detected language code")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the detection")
