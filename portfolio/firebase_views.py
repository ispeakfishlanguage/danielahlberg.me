"""
Django views for Firebase Authentication integration.
Handles Firebase ID token verification and Django session management.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import logging

logger = logging.getLogger(__name__)


@require_POST
def firebase_login(request):
    """
    Authenticate user with Firebase ID token and create Django session.

    Expected POST data:
    {
        "idToken": "firebase-id-token-string"
    }

    Returns:
        JSON response with success/error message and user data
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        id_token = data.get('idToken')

        if not id_token:
            return JsonResponse({
                'error': 'No Firebase ID token provided'
            }, status=400)

        # Authenticate with Firebase backend
        user = authenticate(request, firebase_token=id_token)

        if user:
            # Create Django session
            login(request, user)

            return JsonResponse({
                'success': True,
                'message': 'Authentication successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return JsonResponse({
                'error': 'Authentication failed'
            }, status=401)

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Firebase login error: {str(e)}")
        return JsonResponse({
            'error': 'An error occurred during authentication'
        }, status=500)


@require_POST
def firebase_logout(request):
    """
    Log out the current user and clear Django session.

    Returns:
        JSON response confirming logout
    """
    try:
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logged out successfully'
        })
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return JsonResponse({
            'error': 'An error occurred during logout'
        }, status=500)


@require_http_methods(["GET"])
def firebase_register_view(request):
    """
    Render the Firebase registration page.
    """
    # Redirect to client gallery if already authenticated
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('portfolio:client_gallery')

    return render(request, 'portfolio/register.html')


@require_http_methods(["GET", "POST"])
def firebase_login_view(request):
    """
    Render the Firebase login page.
    """
    # Redirect to client gallery if already authenticated
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('portfolio:client_gallery')

    return render(request, 'portfolio/login.html')


def verify_token(request):
    """
    Verify Firebase ID token (for AJAX requests).

    Expected POST data:
    {
        "idToken": "firebase-id-token-string"
    }

    Returns:
        JSON response with token verification status and user data
    """
    if request.method != 'POST':
        return JsonResponse({
            'error': 'POST request required'
        }, status=405)

    try:
        from .firebase_auth import verify_firebase_token

        data = json.loads(request.body)
        id_token = data.get('idToken')

        if not id_token:
            return JsonResponse({
                'error': 'No Firebase ID token provided'
            }, status=400)

        # Verify the token
        decoded_token = verify_firebase_token(id_token)

        if decoded_token:
            return JsonResponse({
                'valid': True,
                'uid': decoded_token.get('uid'),
                'email': decoded_token.get('email'),
                'name': decoded_token.get('name', ''),
            })
        else:
            return JsonResponse({
                'valid': False,
                'error': 'Invalid or expired token'
            }, status=401)

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return JsonResponse({
            'error': 'An error occurred during token verification'
        }, status=500)


def get_current_user(request):
    """
    Get current authenticated user information.

    Returns:
        JSON response with user data or error if not authenticated
    """
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        })
    else:
        return JsonResponse({
            'authenticated': False
        })
