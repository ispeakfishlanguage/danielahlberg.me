import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
# Generate a default key for Railway if not provided
import secrets
SECRET_KEY = env('SECRET_KEY', default=secrets.token_urlsafe(50) if 'RAILWAY_ENVIRONMENT' in os.environ else 'django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False if any([
    'RAILWAY_ENVIRONMENT' in os.environ,
    'GAE_APPLICATION' in os.environ,
    'K_SERVICE' in os.environ
]) else True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '0.0.0.0', 'www.instalacionesvml.com', 'instalacionesvml.com'])

# Add Railway and Render to allowed hosts in production
if 'RAILWAY_ENVIRONMENT' in os.environ:
    # Railway provides RAILWAY_PUBLIC_DOMAIN
    ALLOWED_HOSTS.append(os.environ.get('RAILWAY_PUBLIC_DOMAIN', ''))
    # Also add the standard Railway app domain pattern
    ALLOWED_HOSTS.extend([
        '.up.railway.app',
        '.railway.app',
        '*'  # Temporarily allow all hosts for Railway - remove after finding exact domain
    ])
if 'RENDER' in os.environ:
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))

# Add Google Cloud (App Engine / Cloud Run) to allowed hosts
if 'GAE_APPLICATION' in os.environ:
    # App Engine
    ALLOWED_HOSTS.extend([
        '.appspot.com',
        '.run.app',
        '*'  # Allow all for App Engine - restrict in production
    ])
if 'K_SERVICE' in os.environ:
    # Cloud Run
    ALLOWED_HOSTS.extend([
        '.run.app',
        '*'
    ])

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://www.instalacionesvml.com',
    'https://instalacionesvml.com',
]
if 'RAILWAY_ENVIRONMENT' in os.environ:
    CSRF_TRUSTED_ORIGINS.extend([
        'https://*.up.railway.app',
        'https://*.railway.app',
    ])
    if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
        CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN')}")

# Add Google Cloud to CSRF trusted origins
if 'GAE_APPLICATION' in os.environ or 'K_SERVICE' in os.environ:
    CSRF_TRUSTED_ORIGINS.extend([
        'https://*.appspot.com',
        'https://*.run.app',
    ])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'cloudinary_storage',
    'cloudinary',
    'portfolio',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'photography_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'portfolio.context_processors.firebase_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'photography_config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production database configuration for Render
import dj_database_url
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'))

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'portfolio.firebase_auth.FirebaseAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Stockholm'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise configuration for serving static files in production
if 'RAILWAY_ENVIRONMENT' in os.environ:
    # Use CompressedStaticFilesStorage (no manifest to avoid 500 errors)
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

WHITENOISE_ALLOW_ALL_ORIGINS = True

# Cloudinary configuration
import cloudinary

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': env('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default=''),
}

cloudinary.config(
    cloud_name=env('CLOUDINARY_CLOUD_NAME', default=''),
    api_key=env('CLOUDINARY_API_KEY', default=''),
    api_secret=env('CLOUDINARY_API_SECRET', default=''),
)

# Firebase configuration
from photography_config.firebase import initialize_firebase
initialize_firebase()

# Firebase Web Configuration (for client-side)
FIREBASE_API_KEY = env('FIREBASE_API_KEY', default='')
FIREBASE_AUTH_DOMAIN = env('FIREBASE_AUTH_DOMAIN', default='')
FIREBASE_PROJECT_ID = env('FIREBASE_PROJECT_ID', default='')
FIREBASE_STORAGE_BUCKET = env('FIREBASE_STORAGE_BUCKET', default='')
FIREBASE_MESSAGING_SENDER_ID = env('FIREBASE_MESSAGING_SENDER_ID', default='')
FIREBASE_APP_ID = env('FIREBASE_APP_ID', default='')

# Media files
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_URL = 'portfolio:login'
LOGIN_REDIRECT_URL = 'portfolio:client_gallery'
LOGOUT_REDIRECT_URL = 'portfolio:home'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Logging configuration for Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}