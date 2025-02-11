"""
Text-to-Speech Service Module

This module provides text-to-speech synthesis capabilities using Google Cloud Text-to-Speech API.
It converts text input into natural-sounding speech with customizable voice parameters.

Dependencies:
    - google-cloud-texttospeech: Google Cloud Text-to-Speech API client library
"""

from google.cloud import texttospeech

class TTSService:
    """
    Text-to-Speech Service Class
    
    This class provides an interface to the Google Cloud Text-to-Speech API,
    allowing conversion of text to synthesized speech with various voice options
    and parameters.
    
    Attributes:
        client: An instance of the Google Cloud Text-to-Speech client
    """
    
    def __init__(self):
        """
        Initialize the Text-to-Speech Service with Google Cloud TTS client.
        """
        self.client = texttospeech.TextToSpeechClient()
    
    async def synthesize_speech(
        self,
        text: str,
        tts_language_code: str,
        voice_name: str,
    ) -> dict:
        """
        Synthesize text into speech with customizable voice parameters.
        
        Args:
            text (str): The text to convert to speech
            tts_language_code (str): The language code for the voice (e.g., 'en-US')
            voice_name (str): The name of the voice to use
        Returns:
            dict: A dictionary containing:
                - audio_content: audio content in MP3 format
                - duration_seconds: Approximate duration of the audio in seconds
        
        Raises:
            Exception: For any text-to-speech API errors
        """
        try:
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code=tts_language_code,
                name=voice_name,
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )

            # Select the type of audio file
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return {
                "audioContent": response.audio_content,
            }

        except Exception as e:
            print(f"TTS error: {str(e)}")
            raise 