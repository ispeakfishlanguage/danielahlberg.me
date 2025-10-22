import os
from pathlib import Path

# Load .env file for local development
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

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

# Middleware - WhiteNoise after SecurityMiddleware for Cloud Run
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

# Cloud Run proxy settings - CRITICAL FOR SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

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

# Database - Use PostgreSQL on Cloud Run, SQLite for local development
import dj_database_url
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    # SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cloudinary configuration
import cloudinary

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    api_key=os.environ.get('CLOUDINARY_API_KEY', ''),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', ''),
)

# Firebase configuration
from photography_config.firebase import initialize_firebase
initialize_firebase()

# Firebase Web Configuration (for client-side)
FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY', '')
FIREBASE_AUTH_DOMAIN = os.environ.get('FIREBASE_AUTH_DOMAIN', '')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', '')
FIREBASE_STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET', '')
FIREBASE_MESSAGING_SENDER_ID = os.environ.get('FIREBASE_MESSAGING_SENDER_ID', '')
FIREBASE_APP_ID = os.environ.get('FIREBASE_APP_ID', '')

# Media files configuration
if os.environ.get('USE_GCS') == 'True':
    DEFAULT_FILE_STORAGE = 'storages.backends.gcs.GoogleCloudStorage'
    GS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'danielahlberg-me-media')
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_URL = 'portfolio:login'
LOGIN_REDIRECT_URL = 'portfolio:client_gallery'
LOGOUT_REDIRECT_URL = 'portfolio:home'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000

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