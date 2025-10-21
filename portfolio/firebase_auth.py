"""
Firebase Authentication utilities for Django integration.
Handles Firebase token verification and Django user management.
"""
from firebase_admin import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class FirebaseAuthenticationBackend(BaseBackend):
    """
    Django authentication backend that validates Firebase ID tokens.
    """

    def authenticate(self, request, firebase_token=None, **kwargs):
        """
        Authenticate user using Firebase ID token.

        Args:
            request: Django request object
            firebase_token: Firebase ID token string

        Returns:
            User object if authentication successful, None otherwise
        """
        if not firebase_token:
            return None

        try:
            # Verify the Firebase ID token
            decoded_token = auth.verify_id_token(firebase_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email', '')
            name = decoded_token.get('name', '')

            # Get or create Django user
            user, created = User.objects.get_or_create(
                username=uid,
                defaults={
                    'email': email,
                    'first_name': name.split()[0] if name else '',
                    'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                }
            )

            # Update email if changed
            if user.email != email:
                user.email = email
                user.save()

            logger.info(f"Firebase authentication successful for user: {uid}")
            return user

        except auth.InvalidIdTokenError:
            logger.warning("Invalid Firebase ID token")
            return None
        except auth.ExpiredIdTokenError:
            logger.warning("Expired Firebase ID token")
            return None
        except Exception as e:
            logger.error(f"Firebase authentication error: {str(e)}")
            return None

    def get_user(self, user_id):
        """
        Get user by ID.

        Args:
            user_id: Django user ID

        Returns:
            User object if found, None otherwise
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def verify_firebase_token(id_token):
    """
    Verify a Firebase ID token and return the decoded token.

    Args:
        id_token: Firebase ID token string

    Returns:
        Decoded token dict if valid, None otherwise
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except auth.InvalidIdTokenError:
        logger.warning("Invalid Firebase ID token")
        return None
    except auth.ExpiredIdTokenError:
        logger.warning("Expired Firebase ID token")
        return None
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return None
