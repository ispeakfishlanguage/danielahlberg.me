"""
Custom decorators for Firebase authentication in Django views.
"""
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth import login
from .firebase_auth import verify_firebase_token
import json


def firebase_auth_required(view_func):
    """
    Decorator that requires Firebase authentication via ID token.
    Expects the Firebase ID token in the Authorization header or POST data.

    Usage:
        @firebase_auth_required
        def my_view(request):
            # request.user will be set to the authenticated Firebase user
            pass
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Try to get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        id_token = None

        if auth_header.startswith('Bearer '):
            id_token = auth_header.split('Bearer ')[1]
        elif request.method == 'POST':
            # Try to get token from POST data
            try:
                if request.content_type == 'application/json':
                    data = json.loads(request.body)
                    id_token = data.get('idToken')
                else:
                    id_token = request.POST.get('idToken')
            except:
                pass

        if not id_token:
            return JsonResponse({
                'error': 'No Firebase ID token provided'
            }, status=401)

        # Verify the token
        decoded_token = verify_firebase_token(id_token)
        if not decoded_token:
            return JsonResponse({
                'error': 'Invalid or expired Firebase ID token'
            }, status=401)

        # Authenticate user with Django
        from django.contrib.auth import authenticate
        user = authenticate(request, firebase_token=id_token)

        if user:
            login(request, user)
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({
                'error': 'Authentication failed'
            }, status=401)

    return wrapper
