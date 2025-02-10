"""
Request Schema Models

This module defines the Pydantic models for API request validation.
It includes models for translation, text-to-speech, and speech-to-text requests
with field validation and descriptive metadata.

All models inherit from Pydantic's BaseModel for automatic validation
and serialization/deserialization functionality.
"""

from pydantic import BaseModel, Field

class TranslateRequest(BaseModel):
    """
    Translation Request Model
    
    Validates and structures requests for the translation endpoint.
    Ensures proper formatting of text and language codes.
    
    Attributes:
        text (str): The text to be translated (must not be empty)
        sourceLanguage (str, optional): The source language code (auto-detected if not provided)
        targetLanguage (str): The language code to translate to (e.g., 'es' for Spanish)
    """
    text: str = Field(..., min_length=1, description="Text to translate")
    sourceLanguage: str | None = Field(None, description="Source language code (auto-detect if not provided)")
    targetLanguage: str = Field(..., description="Target language code (e.g., 'es' for Spanish)")

class TTSRequest(BaseModel):
    """
    Text-to-Speech Request Model
    
    Validates and structures requests for the text-to-speech endpoint.
    Includes voice configuration options for customized speech synthesis.
    
    Attributes:
        text (str): The text to convert to speech (must not be empty)
        ttsCode (str): The language code of the text (e.g., 'en-US')
        ttsName (str): The name of the voice to use
    """
    text: str = Field(..., min_length=1, description="Text to convert to speech")
    ttsCode: str = Field(..., description="Language code of the text (e.g., 'en-US')")
    ttsName: str = Field(..., description="Name of the voice to use")

class STTRequest(BaseModel):
    """
    Speech-to-Text Request Model
    
    Validates and structures requests for the speech-to-text endpoint.
    Handles audio content and configuration for speech recognition.
    
    Attributes:
        audioContent (str): Base64 encoded audio data
        languageCode (str): The language code for speech recognition (e.g., 'en-US')
    
    Note:
        The audioContent must be properly base64 encoded and in the specified
        encoding format for successful transcription.
    """
    audioContent: str = Field(..., description="Base64 encoded audio content")
    languageCode: str = Field(..., description="Language code of the audio (e.g., 'en-US')")

class DetectLanguageRequest(BaseModel):
    """
    Language Detection Request Model
    
    Validates and structures requests for the language detection endpoint.
    
    Attributes:
        text (str): The text to detect language from (must not be empty)
    """
    text: str = Field(..., min_length=1, description="Text to detect language from")
