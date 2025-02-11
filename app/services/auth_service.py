import json
from google.oauth2.service_account import Credentials
from app.core.config import settings

class AuthService:
    """
    AuthService is a centralized helper for obtaining Google Cloud credentials.
    
    It checks the GOOGLE_APPLICATION_CREDENTIALS value from settings. If it 
    contains a JSON string, it parses the credentials and returns a Credentials object.
    Otherwise, it assumes the value is a file path and lets the Google Cloud client libraries
    load it using Application Default Credentials.
    """
    _cached_credentials = None

    @staticmethod
    def get_credentials():
        # Return the cached credentials if already loaded
        if AuthService._cached_credentials is not None:
            print("Using cached credentials")
            return AuthService._cached_credentials

        credentials_str = settings.GOOGLE_APPLICATION_CREDENTIALS.strip()

        if credentials_str.startswith("{"):
            try:
                credentials_info = json.loads(credentials_str)
                AuthService._cached_credentials = Credentials.from_service_account_info(credentials_info)
                print("Loaded credentials from JSON")
                return AuthService._cached_credentials
            except Exception as e:
                print(f"Error parsing credentials JSON: {e}")
                raise
        else:
            # If you're using a file path, returning None makes the client libraries fallback to ADC
            AuthService._cached_credentials = None
            return None 