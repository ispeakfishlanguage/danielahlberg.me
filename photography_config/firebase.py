import firebase_admin
from firebase_admin import credentials
import os
import json
from pathlib import Path

# Initialize Firebase Admin SDK
def initialize_firebase():
    """
    Initialize Firebase Admin SDK with service account credentials.
    Credentials can be provided via:
    1. FIREBASE_CREDENTIALS environment variable (JSON string)
    2. FIREBASE_CREDENTIALS_FILE environment variable (path to JSON file)
    """
    if firebase_admin._apps:
        # Already initialized
        return

    cred = None

    # Try to get credentials from environment variable (JSON string)
    firebase_creds_json = os.environ.get('FIREBASE_CREDENTIALS')
    if firebase_creds_json:
        try:
            cred_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(cred_dict)
        except json.JSONDecodeError:
            print("Error: FIREBASE_CREDENTIALS is not valid JSON")

    # Try to get credentials from file path
    if not cred:
        firebase_creds_file = os.environ.get('FIREBASE_CREDENTIALS_FILE')
        if firebase_creds_file and Path(firebase_creds_file).exists():
            cred = credentials.Certificate(firebase_creds_file)

    # Initialize with credentials or use default (for local development with gcloud)
    if cred:
        firebase_admin.initialize_app(cred)
    else:
        # For local development with Application Default Credentials
        firebase_admin.initialize_app()
