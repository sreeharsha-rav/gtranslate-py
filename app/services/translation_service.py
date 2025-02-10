"""
Translation Service Module

This module provides translation capabilities using Google Cloud Translation API.
It handles text translation between different languages while providing error handling
and logging functionality.

Dependencies:
    - google-cloud-translate: Google Cloud Translation API client library
    - Settings from core.config for supported language configuration
"""

import logging
from google.cloud import translate_v3
from app.core.config import settings

logger = logging.getLogger(__name__)

class TranslationService:
    """
    Translation Service Class
    
    This class provides an interface to the Google Cloud Translation API,
    handling text translation between different languages.
    
    Attributes:
        client: An instance of the Google Cloud Translation client
    """
    
    def __init__(self):
        """
        Initialize the Translation Service with Google Cloud Translation client.
        """
        self.client = translate_v3.TranslationServiceClient()
        self.parent = f"projects/{settings.GOOGLE_PROJECT_ID}/locations/global"
    
    async def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None
    ) -> dict:
        """
        Translate text from source language to target language.
        
        Args:
            text (str): The text to translate
            target_language (str): The language code to translate to (e.g., 'es' for Spanish)
            source_language (str, optional): The language code of the source text.
                                          If None, the API will attempt to detect the language.
        
        Returns:
            dict: A dictionary containing:
                - translated_text: The translated text
                - source_language: The detected or provided source language
                - target_language: The target language code
        
        Raises:
            ValueError: If the target language is not supported
            Exception: For any translation API errors
        """
        try:
            
            response = self.client.translate_text(
                contents=[text],
                target_language_code=target_language,
                parent=self.parent,
                mime_type="text/plain",
                source_language_code=source_language
            )

            if response.translations[0].translated_text:
                return {
                    "translatedText": response.translations[0].translated_text,
                    "detectedSourceLanguage": response.translations[0].detected_language_code or source_language,
                    "targetLanguage": target_language
                }
            else:
                raise Exception("No translation result")
        
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise

    async def detect_language(self, text: str) -> dict:
        """
        Detect the language of the given text.
        """
        try:
            response = self.client.detect_language(
                contents=text,
                parent=self.parent,
                mime_type="text/plain"
            )

            if response.languages[0].language_code:
                return {
                    "languageCode": response.languages[0].language_code,
                    "confidence": response.languages[0].confidence
                }
            else:
                raise Exception("No language detection result")
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")
            raise