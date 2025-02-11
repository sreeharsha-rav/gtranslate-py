"""
Speech-to-Text Service Module

This module provides speech-to-text transcription capabilities using Google Cloud Speech-to-Text API.
It converts audio input into text with support for multiple languages and audio formats.

Dependencies:
    - google-cloud-speech: Google Cloud Speech-to-Text API client library
    - base64: For decoding audio content
"""

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from app.core.config import settings
from app.services.auth_service import AuthService

class STTService:
    """
    Speech-to-Text Service Class
    
    This class provides an interface to the Google Cloud Speech-to-Text API,
    allowing conversion of audio content to text with various configuration options.
    
    Attributes:
        client: An instance of the Google Cloud Speech-to-Text client
    """
    
    def __init__(self):
        """
        Initialize the Speech-to-Text Service with Google Cloud STT client.
        """
        # Use AuthService to obtain credentials
        credentials = AuthService.get_credentials()
        self.client = SpeechClient(credentials=credentials)

    async def transcribe_audio(
        self,
        audio_content: str,
        language_code: str,
    ) -> dict:
        """
        Transcribe audio content to text with specified language and encoding.
        
        Args:
            audio_content (str): Base64 encoded audio data
            language_code (str): The language code for transcription (e.g., 'en-US')
            audio_encoding (str, optional): Audio encoding format (default: 'LINEAR16')
                                        Supported formats: LINEAR16, FLAC, MULAW, AMR, AMR_WB
        
        Returns:
            dict: A dictionary containing:
                - text: The transcribed text
                - confidence: Confidence score of the transcription (0.0 to 1.0)
                - language_code: The language code used for transcription
        
        Raises:
            Exception: For any speech-to-text API errors
        
        Note:
            The audio is expected to be 16kHz sample rate. For best results,
            ensure the audio is in the correct format and sample rate before sending.
        """
        try:
            
            # Configure the recognition settings
            config = cloud_speech.RecognitionConfig(
                auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                language_codes=[language_code],
                model="long",
            )

            # build the request
            request = cloud_speech.RecognizeRequest(
                recognizer=f"projects/{settings.GOOGLE_PROJECT_ID}/locations/global/recognizers/_",
                config=config, 
                content=audio_content
                )
            
            # Perform the transcription
            response = self.client.recognize(request=request)
            
            if not response.results:
                return {
                    "text": "",
                    "confidence": 0.0,
                    "language_code": language_code
                }
            
            result = response.results[0]
            alternative = result.alternatives[0]
            
            return {
                "text": alternative.transcript,
                "confidence": alternative.confidence,
                "languageCode": language_code
            }
            
        except Exception as e:
            print(f"STT error: {str(e)}")
            raise 

    async def transcibe_streaming(
        self,
        stream_file: str,
        language_code: str,
        audio_encoding: str = "LINEAR16"
    ) -> dict:
        """
        Transcribes audio from a audio file stream using Google Cloud STT.

        Args:
            stream_file (str): The path to the audio file to transcribe
            language_code (str): The language code for transcription (e.g., 'en-US')
            audio_encoding (str, optional): Audio encoding format (default: 'LINEAR16')
                                        Supported formats: LINEAR16, FLAC, MULAW, AMR, AMR_WB
        
        Returns:
            dict: A dictionary containing:
                - text: The transcribed text
        """
        try:
            # create the audio input object
            audio = cloud_speech.RecognitionAudio(uri=stream_file)
            
            # configure the recognition settings
            config = cloud_speech.RecognitionConfig(
                encoding=getattr(cloud_speech.RecognitionConfig.AudioEncoding, audio_encoding),
                sample_rate_hertz=16000,
                language_code=language_code,
                enable_automatic_punctuation=True
            )
            
            # build the request
            request = cloud_speech.StreamingRecognizeRequest(config=config, audio=audio)
            
            # create the streaming client
            client = self.client.streaming_recognize()
            
            # send the request
            client.send_message(request)
            
            # get the response
            response = client.receive_message()
            
            return {
                "text": response.results[0].alternatives[0].transcript
            }
        
        except Exception as e:
            print(f"Speech-to-Text streaming error: {str(e)}")
            raise 