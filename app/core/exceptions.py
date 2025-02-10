"""
Custom Exception Classes

This module defines custom exceptions used throughout the application.
These exceptions provide specific error types for different failure scenarios,
allowing for better error handling and more informative error messages.

Each exception type corresponds to a specific service or validation error,
making it easier to handle errors appropriately at different layers of the application.
"""

class TranslationError(Exception):
    """
    Translation Service Exception
    
    Raised when there is an error in the translation service.
    This could be due to:
    - Invalid language codes
    - API quota exceeded
    - Network connectivity issues
    - Invalid input text format
    """
    pass

class TTSError(Exception):
    """
    Text-to-Speech Service Exception
    
    Raised when there is an error in the text-to-speech service.
    This could be due to:
    - Invalid voice configuration
    - Unsupported language
    - API quota exceeded
    - Audio synthesis failure
    """
    pass

class STTError(Exception):
    """
    Speech-to-Text Service Exception
    
    Raised when there is an error in the speech-to-text service.
    This could be due to:
    - Invalid audio format
    - Corrupted audio data
    - Unsupported language
    - Transcription processing failure
    """
    pass

class ValidationError(Exception):
    """
    Data Validation Exception
    
    Raised when there is a validation error in the request data.
    This could be due to:
    - Missing required fields
    - Invalid data types
    - Value range violations
    - Format violations
    """
    pass
